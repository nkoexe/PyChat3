#!/usr/bin/env python3
from socket import socket, timeout
from time import sleep
from requests import get, exceptions
from threading import Thread
from os import mkdir, chdir, remove, system
from base64 import b64decode
from PySide6.QtCore import Signal, Slot, QObject
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtGui import QGuiApplication
from shutil import unpack_archive
import sys
from os.path import join, exists, expanduser
from subprocess import call


print(" ╔════════════════════════════════════════════════════════════════════════════════════╗")
print(" ║                                  >> BENVENUTO! <<                                  ║")
print(" ╠════════════════════════════════════════════════════════════════════════════════════╣")
print(" ║                  Grazie per aver scelto di installare quest'app.                   ║")
print(" ║             Se hai un qualsiasi dubbio o curiosità, hai trovato un bug             ║")
print(" ║            o vuoi semplicamente passare a salutare, scrivimi su Discord!           ║")
print(" ║                                     neeco#7533                                     ║")
print(" ╠════════════════════════════════════════════════════════════════════════════════════╣")
print(" ║ Assicurati di essere connesso a Internet.                                          ║")
print(" ║ Non chiudere questa finestra fino a quando l'installazione non sarà completata.    ║")
print(" ╠════════════════════════════════════════════════════════════════════════════════════╣")
print(" ║ Premi <Invio> per continuare.                                                      ║")
input(" ╚════════════════════════════════════════════════════════════════════════════════════╝\n")

if not exists('C:/Windows/Fonts/Product Sans Regular.ttf'):
    print(" ╔═══════════════════════════════════════════════════════════════════════════════════════════════════════╗")
    print(" ║                                        * Attenzione *                                                 ║")
    print(" ╠═══════════════════════════════════════════════════════════════════════════════════════════════════════╣")
    print(' ║ Questa applicazione utilizza il font "Product Sans", che non è preinstallato nel sistema.             ║')
    print(' ║ Per una migliore esperienza è consigliato di installarlo manualmente, dato che questo programma       ║')
    print(' ║ non è ancora in grado di farlo automaticamente.                                                       ║')
    print(' ║ Il file può essere trovato nella cartella "' +
          join(expanduser('~'), '.PyChat', 'fonts."').ljust(59) + '║')
    input(" ╚═══════════════════════════════════════════════════════════════════════════════════════════════════════╝\n")

# todo: check for missing modules


qml = b'''import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material

Window {
    id: win
    width: 500
    height: 300
    visible: true
    color: "#00000000"
    flags: Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint

    Material.theme: Material.Dark
    Material.accent: "#d61c6f"

    function setLabel (s) {
        subtitle.text = s
    }
    function setLoading (v) {
        progressBar.visible = v
    }

    MouseArea {
        id: mousearea
        anchors.fill: parent

        property int previousX
        property int previousY

        onPressed: {
            previousX = mouseX
            previousY = mouseY
        }

        onMouseXChanged: {
            win.setX(win.x + mouseX - previousX)
        }

        onMouseYChanged: {
            win.setY(win.y + mouseY - previousY)
        }

        Rectangle {
            id: root
            color: "#222"
            border.width: 0
            radius: 5
            anchors.fill: parent

            Button {
                id: closebutton
                width: 50
                height: 40
                text: "\u00d7"
                anchors.right: parent.right
                anchors.top: parent.top
                font.family: "Arial"
                font.pointSize: 18
                hoverEnabled: true

                background: Rectangle {
                    color: "transparent"
                    border.width: 0
                    anchors.fill: parent
                    clip: true

                    Rectangle {
                        x: -5
                        width: parent.width + 5
                        height: parent.height + 5
                        radius: 5
                        border.width: 0
                        color: closebutton.pressed ? "#d80073" : (closebutton.hovered ? "#09ffffff" : "transparent")
                    }
                }

                onReleased: {
                    backend._exit(1)
                    win.close()
                }
            }

            Text {
                id: title
                color: '#eee'
                text: "PyChat v0.0"
                anchors.top: parent.top
                verticalAlignment: Text.AlignVCenter
                font.bold: true
                anchors.topMargin: win.height/3
                anchors.horizontalCenter: parent.horizontalCenter
                horizontalAlignment: Text.AlignHCenter
                font.family: 'Product Sans'
                font.pixelSize: 30
            }

            Text {
                id: subtitle
                color: '#eee'
                text: "Connessione al server ..."
                anchors.top: title.bottom
                verticalAlignment: Text.AlignVCenter
                anchors.topMargin: win.height/10
                horizontalAlignment: Text.AlignHCenter
                anchors.horizontalCenter: parent.horizontalCenter
                font.family: 'Product Sans'
                font.pixelSize: 15
            }

            ProgressBar {
                id: progressBar
                height: 12
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                indeterminate: true
            }
        }
    }
}
'''


class WindowBackend(QObject):
    setLabel = Signal(str)
    setLoading = Signal(bool)
    exitCode = Signal(int)

    def __init__(self):
        super(WindowBackend, self).__init__()

        self.app = QGuiApplication()
        self.engine = QQmlApplicationEngine()
        self.engine.rootContext().setContextProperty('backend', self)
        self.engine.loadData(qml)
        self.root = self.engine.rootObjects()[0]

        self.setLabel.connect(self.root.setLabel)
        self.setLoading.connect(self.root.setLoading)
        self.exitCode.connect(self._exit)

    @Slot(int)
    def _exit(self, code):
        if code == 0:
            self.root.deleteLater()
            call([sys.executable, 'main.py'])
            return
        elif code == 1:
            # cleanup ?
            return self.root.deleteLater()
        elif code == 2:
            msg = 'Offline  -  Server non attivo'
        elif code == 3:
            msg = 'Offline  -  Nessuna connessione a Internet'
        elif code == 4:
            msg = 'Offline  -  Nessuna risposta dal Server'

        self.setLabel.emit(msg)
        self.setLoading.emit(False)

    def exec(self):
        self.app.exec()


def recieve():
    size = aton(sock.recv(4).decode())
    p = sock.recv(size)
    return b64decode(p)


def aton(a):
    c1, c2, c3, c4 = [i-33 for i in map(ord, list(a))]

    return c1*93**3 + c2*93**2 + c3*93 + c4


def connect():
    global sock

    sock = socket(2, 1)
    sock.settimeout(5)
    try:
        sock.connect(('localhost', 24839))
    except ConnectionRefusedError:
        return window._exit(2)
    except exceptions.ConnectionError:
        return window._exit(3)
    except timeout:
        return window._exit(4)
    sock.settimeout(None)

    sock.recv(128)
    sock.send(b'}}}{')
    sleep(.3)
    window.setLabel.emit('Scaricando i dati ...')

    if not exists(PATH):
        mkdir(PATH)
    chdir(PATH)

    sleep(.5)
    open('qml.zip', 'wb').write(recieve())
    open('main.py', 'wb').write(recieve())
    open('config.ini', 'wb').write(recieve())

    window.setLabel.emit('Estraendo i dati ...')
    sleep(.3)
    unpack_archive('qml.zip', 'qml', 'zip')
    remove('qml.zip')

    # TODO: install Fonts

    if sys.platform == 'win32':
        from win32com.client import Dispatch
        for i in [join(expanduser('~'), 'Desktop', 'PyChat.lnk'), join(expanduser('~'), 'AppData\Roaming\Microsoft\Windows\Start Menu\Programs', 'PyChat.lnk')]:
            shortcut = Dispatch('WScript.Shell').CreateShortCut(i)
            shortcut.Targetpath = join(PATH, 'main.py')
            shortcut.WorkingDirectory = PATH
            shortcut.IconLocation = join(PATH, 'qml', 'images', 'appicon.ico')
            shortcut.save()
    elif sys.platform.startswith('linux'):
        open(join(expanduser('~'), 'Desktop', 'PyChat.desktop'), 'w').write(f'''[Desktop Entry]
Name=PyChat3
Icon={join(PATH, 'qml', 'images', 'appicon.ico')}
Exec={sys.executable} {join(PATH, 'main.py')}
Terminal=true
Type=Application''')
        call(['chmod', '+x', join(expanduser('~'), 'Desktop', 'PyChat.desktop')])

    window.setLabel.emit('Fatto')
    print('syscall installer:', system('py main.py'))


PATH = join(expanduser('~'), '.PyChat3')

if __name__ == '__main__':
    window = WindowBackend()
    Thread(target=connect).start()
    window.exec()
