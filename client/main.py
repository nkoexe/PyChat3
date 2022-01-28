#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from base64 import b64encode, b64decode
from configparser import ConfigParser
from hashlib import sha256
from json import loads
from os.path import exists, dirname, join
from os import chdir, fspath, name as osname
from pathlib import Path
from time import time
from requests import get, exceptions
from socket import socket, timeout
from threading import Thread

from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import Signal, Slot, QObject
from simplejson import dumps


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


class WindowBackend(QObject):
    openMain = Signal()
    openLoading = Signal()
    openLogin = Signal()
    openSignup = Signal()

    setStatus = Signal(str)
    exitCode = Signal(int)

    switchTheme = Signal()

    def __init__(self):
        super(WindowBackend, self).__init__()

        # Init QT
        self.app = QGuiApplication()
        self.engine = QQmlApplicationEngine()

        # Set app icon
        self.app.setWindowIcon(QIcon(join('qml', 'images', 'appicon.png')))
        if osname == 'nt':
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                u'nicoinc.pychat.3')

        # Connect frontend to backend
        self.engine.rootContext().setContextProperty('backend', self)

        self.openMain.connect(self._openMain)
        self.openLoading.connect(self._openLoading)
        self.openLogin.connect(self._openLogin)
        self.openSignup.connect(self._openSignup)

    def loadSettings(self, theme=None, settings=None):
        'Load color theme and settings into frontend'
        if theme:
            self.engine.rootContext().setContextProperty('colors', theme)
        if settings:
            self.engine.rootContext().setContextProperty('settings', settings)

    def _switchThemeTEMP(self):
        'temp funcion, change color scheme'
        themes = CONFIG.sections()
        themes.remove('settings')
        themes.remove('data')
        current = CONFIG.get('settings', 'theme')
        index = themes.index(current) + 1
        if index >= len(themes):
            index = 0
        theme = themes[index]
        CONFIG.set('settings', 'theme', theme)
        self.loadSettings(
            CONFIG._sections[theme], CONFIG._sections['settings'])

    def _openMain(self):
        # Open main application
        self.engine.load(
            join(dirname(__file__), 'qml', 'main.qml'))
        self.root = self.engine.rootObjects()[-1]

        self.switchTheme.connect(self._switchThemeTEMP)

    def _openLoading(self):
        # Open loading splash screen
        self.engine.load(
            join(dirname(__file__), 'qml', 'loading.qml'))
        self.root = self.engine.rootObjects()[-1]

        self.setStatus.connect(self.root.setLabel)
        self.exitCode.connect(self.root.exitCode)

    def _openLogin(self):
        # Open login window
        self.engine.load(
            join(dirname(__file__), 'qml', 'login.qml'))
        self.root = self.engine.rootObjects()[-1]

        self.exitCode.connect(self.root.exitCode)

    def _openSignup(self):
        # Open signup window
        self.engine.load(
            join(dirname(__file__), 'qml', 'signup.qml'))
        self.root = self.engine.rootObjects()[-1]

        self.exitCode.connect(self.root.exitCode)

    def exec(self):
        # Start the application
        self.app.exec()

    @Slot(str, str)
    def send(self, msgtype, msg):
        # Send chat message
        return connection.sendMessage(msgtype, msg)

    @Slot()
    def close(self):
        # Send chat message
        return connection.close()

    @Slot(str, str, result=int)
    def submitLogin(self, username, password):
        # Submit login info
        return connection.submitLogin(username, sha256(password.encode()).hexdigest())

    @Slot(str, str, str, str, str, result=int)
    def submitSignup(self, imgpath, username, password, col1, col2):
        # Submit signup info
        return connection.submitSignup(imgpath, username, sha256(password.encode()).hexdigest(), col1, col2)


class ConnectionBackend:
    def __init__(self):
        self.sock = socket(2, 1)

    def send(self, msg):
        'Encode & send to server bytes or str'

        if isinstance(msg, str):
            msg = msg.encode()
        msg = b64encode(msg)
        msg = f'{ntoa(len(msg))}'.encode() + msg
        self.sock.send(msg)

    def recieve(self, bytes=False):
        'Recieve & decode data from server, leave bytes or not'

        msg = b64decode(self.sock.recv(aton(self.sock.recv(4).decode())))
        if not bytes:
            msg = msg.decode()
        return msg

    def sendMessage(self, msgtype, msg):
        'Send chat message to server'
        msg = {msgtype: {
            'from': self.MY_ID,
            't': time(),
            'content': msg
        }}
        self.send(dumps(msg))

    def connectServer(self):
        'Connects to the server & returns code'

        self.sock.settimeout(4)

        try:
            self.sock.connect(('localhost', 24839))
            # Recieve latest version code
            self.serverVersion = self.sock.recv(BUF).decode()
            res = 0
        except ConnectionRefusedError:
            res = 1
        except exceptions.ConnectionError:
            res = 2
        except timeout:
            res = 3

        self.sock.settimeout(None)

        return res

    def standardConnect(self):
        'User is logged in, start main application'

        window.openLoading.emit()
        code = self.connectServer()

        # Error in connection
        if code != 0:
            return window.exitCode.emit(code)

        self.VERSION = CONFIG.get('data', 'version')
        self.MY_ID, MY_HASH = CONFIG.get('data', 'login').split('g')

        # Local and server version do not match, update app
        if self.VERSION != self.serverVersion:
            self.sock.send(b'}}}z')
            window.setStatus.emit('Aggiornando il Software ...')
            open('qml.zip', 'wb').write(self.recieve(bytes=True))
            open('main.py', 'wb').write(self.recieve(bytes=True))

            window.setStatus.emit('Estraendo i dati ...')

            from shutil import unpack_archive
            from os import remove, system
            unpack_archive('qml.zip', 'qml', 'zip')
            remove('qml.zip')
            print('update: ', system('py main.py'))

        else:
            # Up to date, send login
            self.sock.send(ntoa(int(self.MY_ID)).encode())
            self.send(MY_HASH)

            # Invalid login, open login page
            if self.sock.recv(1) != b'k':
                return print('login invalid')

            window.exitCode.emit(0)
            window.openMain.emit()

            # Start main reciever loop
            self.mainReciever()

    def submitLogin(self, username, password):
        'Send login information to server'
        code = self.connectServer()
        if code != 0:
            return code
        self.sock.send(b'}}}y')
        self.send(username + '×' + password)
        self.MY_ID = self.recieve()
        if self.MY_ID == 'nope':
            # Login invalid
            self.sock.close()
            self.sock = socket()
            return -1
        else:
            CONFIG.set('data', 'version', self.serverVersion)
            CONFIG.set('data', 'login', self.MY_ID+'g'+password)
            # Todo: remove, add to close event
            CONFIG.write(open('config.ini', 'w'))

            window.exitCode.emit(0)
            window.openMain.emit()
            self.mainReciever()

    def submitSignup(self, imgpath, username, password, col1, col2):
        code = self.connectServer()
        if code != 0:
            return code
        self.sock.send(b'}}}x')

        self.send(username)
        if self.sock.recv(1) == b'n':
            self.sock.close()
            self.sock = socket()
            return -1

        self.send(open(join('qml', imgpath), 'rb').read())
        self.send(password + '×' + col1 + '×' + col2)
        self.MY_ID = self.recieve()

        CONFIG.set('data', 'version', self.serverVersion)
        CONFIG.set('data', 'login', self.MY_ID+'g'+password)
        # Todo: don't write now, add to close event
        CONFIG.write(open('config.ini', 'w'))

        window.root.deleteLater()
        window.openMain.emit()
        self.mainReciever()

    def mainReciever(self):
        self.USERS = loads(self.recieve())

        while True:
            print(self.recieve())

    def close(self):
        self.send(dumps({'event': {'from': self.MY_ID, 'type': 'close'}}))


def loadSettings():
    theme = CONFIG.get('settings', 'theme')

    # Todo: add checking beforehand
    window.loadSettings(CONFIG._sections[theme], CONFIG._sections['settings'])


if __name__ == '__main__':
    chdir(dirname(__file__))

    window = WindowBackend()
    connection = ConnectionBackend()

    CONFIG = ConfigParser()
    CONFIG.read('config.ini')
    loadSettings()

    if CONFIG.get('data', 'login'):
        Thread(target=connection.standardConnect, daemon=True).start()
    else:
        window.openLogin.emit()

    BUF = 1024

    window.exec()
