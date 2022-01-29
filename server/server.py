#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from base64 import b64decode, b64encode
from copy import deepcopy
from json import dump, dumps, load, loads
from os import chdir, remove
from os.path import dirname, join
from shutil import make_archive
from socket import socket
from threading import Thread


def send(cli, msg):
    if isinstance(msg, str):
        msg = msg.encode()
    m = b64encode(msg)
    m = f'{ntoa(len(m))}'.encode() + m
    cli.send(m)


def recieve(cli, bytes=False):
    msg = b64decode(cli.recv(aton(cli.recv(4).decode())))
    if not bytes:
        msg = msg.decode()
    return msg


# encoding num to 4 lett ascii - max 74805200
def ntoa(n):
    c4 = n % 93 + 33
    c3 = n // 93 % 93 + 33
    c2 = n // 93**2 % 93 + 33
    c1 = n // 93**3 % 93 + 33

    return ''.join(map(chr, (c1, c2, c3, c4)))


# decoding 4 letter ascii to num
def aton(a):
    c1, c2, c3, c4 = [i-33 for i in map(ord, list(a))]

    return c1*93**3 + c2*93**2 + c3*93 + c4


def newuser(imgdata, username, passw, col1, col2):
    userid = 1
    for u in USERS:
        if int(u) != userid:
            break
        userid += 1

    userid = str(userid)

    open(f'images/{userid}.png', 'wb').write(imgdata)
    USERS[userid] = {'name': username,
                     'hash': passw,
                     'col1': col1,
                     'col2': col2,
                     'customstatus': ''}
    dump(USERS, open('users.json', 'w'), indent=2, sort_keys=True)

    return userid


def handle_client(cli, cli_id):
    USERS[cli_id]['online'] = True
    USERS_TO_SEND = deepcopy(USERS)
    for u in USERS_TO_SEND:
        del USERS_TO_SEND[u]['hash']

    send(cli, dumps(USERS_TO_SEND))

    while True:
        msg = loads(recieve(cli))

        if 'event' in msg:
            if msg['event']['type'] == 'close':
                USERS[msg['event']['from']]['online'] = False
                # Send update to online users
                break

        elif 'update' in msg:
            pass

        else:
            print(msg)


if __name__ == '__main__':
    chdir(dirname(__file__))
    VERSION = open('data/version', 'r').read()
    USERS = load(open('users.json', 'r'))
    for u in USERS:
        USERS[u]['online'] = False

    server = socket(2, 1)
    server.bind(('0.0.0.0', 24839))
    server.listen()

    while True:
        client, client_address = server.accept()

        client.send(VERSION.encode())  # send version
        client_id = str(aton(client.recv(4).decode()))  # recieve id or code

        # 74805200: update version
        # 74805199: servercmd script
        # 74805198: first download
        # 74805197: download update
        # 74805196: login
        # 74805195: registering
        # other: users

        if client_id == '74805200':
            VERSION = client.recv(1024).decode()
            print(VERSION)
            # send notification to active users

        elif client_id == '74805199':
            print('servercmd')

        # todo: mandare manualmente i file (senza main.pyproj)
        elif client_id == '74805198':
            make_archive('../client/qml', 'zip', '../client/qml')
            send(client, open('../client/qml.zip', 'rb').read())
            remove('../client/qml.zip')
            send(client, open('../client/main.py', 'rb').read())
            send(client, open('../client/config.ini', 'rb').read())

        elif client_id == '74805197':
            make_archive('../client/qml', 'zip', '../client/qml')
            send(client, open('../client/qml.zip', 'rb').read())
            remove('../client/qml.zip')
            send(client, open('../client/main.py', 'rb').read())

        elif client_id == '74805196':
            usr, passw = recieve(client).split('×')

            for u in USERS:
                if USERS[u]['name'].lower() == usr.lower() and USERS[u]['hash'] == passw:
                    send(client, u)
                    Thread(target=handle_client, args=(
                        client, u), daemon=True).start()
                    break
            else:
                print('login invalid')
                send(client, 'nope')
                client.close()

        elif client_id == '74805195':
            username = recieve(client)
            taken = False
            for u in USERS:
                if USERS[u]['name'] == username:
                    taken = True
                    break

            if taken:
                client.send(b'n')
                continue

            client.send(b'k')
            client_id = newuser(recieve(client, bytes=True),
                                username, *recieve(client).split('×'))
            send(client, client_id)
            Thread(target=handle_client, args=(
                client, client_id), daemon=True).start()

        elif client_id not in USERS:
            recieve(client)
            client.send(b'n')

        else:
            if USERS[client_id]['hash'] == recieve(client):
                client.send(b'k')
                Thread(target=handle_client, args=(
                    client, client_id), daemon=True).start()

            else:
                client.send(b'n')
