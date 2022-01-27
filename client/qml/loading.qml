import QtQuick
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
    Material.accent: colors.highlight


    function setLabel (s) {
        subtitle.text = s
    }

    function exitCode (v) {
        if (v === 0) {
            win.close()
        } else if (v === 1) {
            subtitle.text = "Offline  -  Server non attivo"
        } else if (v === 2) {
            subtitle.text = "Offline  -  Nessuna connessione a Internet"
        } else if (v === 3) {
            subtitle.text = "Offline  -  Nessuna risposta dal Server"
        }
        progressBar.visible = false
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
            color: colors.bg2
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
                        color: closebutton.pressed ? colors.highlight : (closebutton.hovered ? "#09ffffff" : "transparent")
                    }
                }

                onReleased: {
                    win.close()
                }
            }

            Text {
                id: title
                color: colors.text1
                text: "PyChat v0.0"
                anchors.top: parent.top
                verticalAlignment: Text.AlignVCenter
                font.bold: true
                anchors.topMargin: win.height/3
                anchors.horizontalCenter: parent.horizontalCenter
                horizontalAlignment: Text.AlignHCenter
                font.family: settings.font
                font.pixelSize: 30
            }

            Text {
                id: subtitle
                color: colors.text1
                text: "Connessione al server ..."
                anchors.top: title.bottom
                verticalAlignment: Text.AlignVCenter
                anchors.topMargin: win.height/10
                horizontalAlignment: Text.AlignHCenter
                anchors.horizontalCenter: parent.horizontalCenter
                font.family: settings.font
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

/*##^##
Designer {
    D{i:0;formeditorZoom:1.5}D{i:3}D{i:6}D{i:7}D{i:8}D{i:2}D{i:1}
}
##^##*/
