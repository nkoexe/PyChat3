from base64 import b64encode, b64decode
from configparser import ConfigParser
from hashlib import sha256
from json import loads
from os.path import exists, dirname, join
from os import chdir, fspath, name as osname
from pathlib import Path
from requests import get, exceptions
from socket import socket, timeout
from threading import Thread

from PySide6.QtGui import QGuiApplication, QIcon
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
    openSignup = Signal()

    setStatus = Signal(str)
    exitCode = Signal(int)

    switchTheme = Signal()

    def __init__(self):
        super(WindowBackend, self).__init__()

        self.app = QGuiApplication()
        self.engine = QQmlApplicationEngine()

        self.app.setWindowIcon(QIcon(join('qml', 'images', 'appicon.png')))
        if osname == 'nt':
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                u'nicoinc.pychat.3')

        self.engine.rootContext().setContextProperty('backend', self)

        self.openMain.connect(self._openMain)
        self.openLoading.connect(self._openLoading)
        self.openLogin.connect(self._openLogin)
        self.openSignup.connect(self._openSignup)

    def loadSettings(self, theme=None, settings=None):
        if theme:
            self.engine.rootContext().setContextProperty('colors', theme)
        if settings:
            self.engine.rootContext().setContextProperty('settings', settings)

    def _switchThemeTEMP(self):
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
        self.engine.load(
            join(dirname(__file__), 'qml', 'main.qml'))
        self.root = self.engine.rootObjects()[-1]

        self.switchTheme.connect(self._switchThemeTEMP)

    def _openLoading(self):
        self.engine.load(
            join(dirname(__file__), 'qml', 'loading.qml'))
        self.root = self.engine.rootObjects()[-1]

        self.setStatus.connect(self.root.setLabel)
        self.exitCode.connect(self.root.exitCode)

    def _openLogin(self):
        self.engine.load(
            join(dirname(__file__), 'qml', 'login.qml'))
        self.root = self.engine.rootObjects()[-1]

    def _openSignup(self):
        self.engine.load(
            join(dirname(__file__), 'qml', 'signup.qml'))
        self.root = self.engine.rootObjects()[-1]

    def exec(self):
        self.app.exec()

    @Slot(str, str, result=int)
    def submitLogin(self, username, password):
        return connection.submitLogin(username, sha256(password.encode()).hexdigest())

    @Slot(str, str, str, str, str, result=int)
    def submitSignup(self, imgpath, username, password, col1, col2):
        return connection.submitSignup(imgpath, username, sha256(password.encode()).hexdigest(), col1, col2)


class ConnectionBackend:
    def __init__(self):
        self.sock = socket(2, 1)
        self.connected = False

    def send(self, msg):
        if isinstance(msg, str):
            msg = msg.encode()
        msg = b64encode(msg)
        msg = f'{ntoa(len(msg))}'.encode() + msg
        self.sock.send(msg)

    def recieve(self, bytes=False):
        msg = b64decode(self.sock.recv(aton(self.sock.recv(4).decode())))
        if not bytes:
            msg = msg.decode()
        return msg

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

        # UPDATE
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
            return -1
        else:
            CONFIG.set('data', 'version', self.serverVersion)
            CONFIG.set('data', 'login', self.MY_ID+'g'+password)
            # Todo: remove, add to close event
            CONFIG.write(open('config.ini', 'w'))

            window.root.deleteLater()
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
