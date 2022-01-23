from base64 import b64encode, b64decode
from configparser import ConfigParser
from hashlib import sha256
from json import loads
from os.path import exists, dirname, join
from os import chdir, fspath
from pathlib import Path
from requests import get, exceptions
from socket import socket, timeout
from threading import Thread

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import Signal, Slot, QObject


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

    setStatus = Signal(str)
    exitCode = Signal(int)

    def __init__(self):
        super(WindowBackend, self).__init__()

        self.app = QGuiApplication()
        self.engine = QQmlApplicationEngine()
        self.engine.rootContext().setContextProperty('backend', self)

        self.openMain.connect(self._openMain)
        self.openLoading.connect(self._openLoading)
        self.openLogin.connect(self._openLogin)

    def _openMain(self):
        self.engine.load(
            join(dirname(__file__), 'qml', 'main.qml'))
        self.root = self.engine.rootObjects()[1]

    def _openLoading(self):
        self.engine.load(
            join(dirname(__file__), 'qml', 'loading.qml'))
        self.root = self.engine.rootObjects()[0]

        self.setStatus.connect(self.root.setLabel)
        self.exitCode.connect(self.root.exitCode)

    def _openLogin(self):
        self.engine.load(
            join(dirname(__file__), 'qml', 'login.qml'))
        self.root = self.engine.rootObjects()[0]

    def exec(self):
        self.app.exec()

    @Slot(str, str, result=int)
    def submitLogin(self, username, password):
        return connection.submitLogin(username, sha256(password.encode()).hexdigest())


class ConnectionBackend:
    def __init__(self):
        self.sock = socket(2, 1)
        self.connected = False

    def send(self, msg: str):
        m = b64encode(msg.encode())
        m = f'{ntoa(len(m))}'.encode() + m
        self.sock.send(m)

    def recieve(self):
        size = aton(self.sock.recv(4).decode())
        p = self.sock.recv(size)
        return b64decode(p).decode()

    def connectServer(self):
        self.sock.settimeout(4)

        try:
            self.sock.connect(('localhost', 24839))
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
        window.openLoading.emit()
        code = self.connectServer()

        if code != 0:
            return window.exitCode.emit(code)

        self.VERSION = CONFIG.get('data', 'version')
        self.MY_ID, MY_HASH = CONFIG.get('data', 'login').split('g')

        if self.VERSION != self.serverVersion:
            self.sock.send(b'}}}{')

        else:
            self.sock.send(ntoa(int(self.MY_ID)).encode())
            self.send(MY_HASH)

            if self.sock.recv(1) != b'k':
                return print('login invalid')  # go to login

            window.exitCode.emit(0)
            window.openMain.emit()

            self.mainReciever()

    def submitLogin(self, username, password):
        code = self.connectServer()
        if code != 0:
            return code
        self.sock.send(b'}}}y')
        self.send(username + '×' + password)
        self.MY_ID = self.recieve()
        if self.MY_ID == 'nope':
            self.sock.close()
            self.sock = socket()
            return 1
        else:
            CONFIG.set('data', 'version', self.serverVersion)
            CONFIG.set('data', 'login', self.MY_ID+'g'+password)
            # Todo: remove, add to close event
            CONFIG.write(open('config.ini', 'w'))
            window.root.deleteLater()
            window.openMain.emit()
            self.mainReciever()

    def mainReciever(self):
        self.USERS = loads(self.recieve())


if __name__ == '__main__':
    window = WindowBackend()
    connection = ConnectionBackend()

    chdir(dirname(__file__))
    CONFIG = ConfigParser()
    CONFIG.read('config.ini')

    if CONFIG.get('data', 'login'):
        Thread(target=connection.standardConnect, daemon=True).start()
    else:
        window.openLogin.emit()

    BUF = 1024

    window.exec()
