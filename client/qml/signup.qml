import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import Qt.labs.platform
import Qt5Compat.GraphicalEffects


Window {
    id: win
    title: "PyChat Signup"
    width: 500
    height: 700
    visible: true
    color: "#00000000"
    flags: Qt.FramelessWindowHint | Qt.Window


    Material.theme: Material.Dark
    Material.accent: colors.primary


    Rectangle {
        id: root
        color: colors.bg2
        border.width: 0
        radius: 5
        anchors.fill: parent

        MouseArea {
            id: mousearea

            property int previousX
            property int previousY
            height: 50
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top

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

            Text {
                id: title
                color: colors.text1
                text: "PyChat - Signup"
                anchors.left: parent.left
                anchors.top: parent.top
                anchors.leftMargin: 25
                anchors.topMargin: 18
                font.bold: true
                font.family: settings.font
                font.pixelSize: 24
            }

            Button {
                id: closebutton
                height: parent.height
                width: height+10
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
                    win.close()
                }
            }
        }

        Image {
            id: image
            width: 100
            height: 100
            anchors.top: mousearea.bottom
            source: "images/default.png"
            anchors.topMargin: 45
            anchors.horizontalCenter: parent.horizontalCenter
            fillMode: Image.PreserveAspectFit

            ColorOverlay {
                source: image
                color: colors.icons
                antialiasing: true
                anchors.fill: image
            }
        }

        TextField {
            id: username
            width: win.width/1.5
            font.pointSize: 14
            anchors.top: image.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.topMargin: 30
            placeholderText: "Username"
        }

        TextField {
            id: password
            width: win.width/1.5
            font.pointSize: 14
            anchors.top: username.bottom
            anchors.topMargin: 20
            anchors.horizontalCenter: parent.horizontalCenter
            placeholderText: "Password"
            echoMode: "Password"
        }

        MouseArea {
            id: col1
            width: 100
            height: width
            anchors.left: parent.left
            anchors.top: password.bottom
            anchors.leftMargin: 110
            anchors.topMargin: 50
            hoverEnabled: true

            onClicked: {
                console.log('col1')
            }

            onHoveredChanged: {
                if (containsMouse) {
                    color1.color = 'white'
                }
            }

            Rectangle {
                id: color1
                color: "#d43398"
                border.width: 0
                radius: col1.width/2
                anchors.fill: parent
            }
        }

        MouseArea {
            id: col2
            width: col1.width
            height: col1.width
            anchors.right: parent.right
            anchors.top: password.bottom
            anchors.rightMargin: col1.anchors.leftMargin
            anchors.topMargin: col1.anchors.topMargin

            onClicked: {
                console.log('col2')
            }

            Rectangle {
                id: color2
                color: "#3760b4"
                border.width: 0
                radius: col1.width/2
                anchors.fill: parent
            }
        }

        Button {
            id: signup
            width: win.width/1.5
            text: "Signup"
            font.pointSize: 12
            anchors.top: password.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.topMargin: 235

            onReleased: {
                if (username.text && password.text) {
                    progressBar.visible = true
                    let code = backend.submitSignup(image.source, username.text, password.text, color1.color, color2.color)
                    if (code === -1) {
                        console.log("username taken")
                    }
                    progressBar.visible = false
                }
            }
        }

        LinearGradient {
            width: win.width/1.5
            height: 3
            anchors.top: signup.bottom
            anchors.horizontalCenter: parent.horizontalCenter

            gradient: Gradient {
                orientation: Gradient.Horizontal
                GradientStop { position: 0; color: color1.color }
                GradientStop { position: 1; color: color2.color }
            }
        }

        ProgressBar {
            id: progressBar
            visible: false
            height: 12
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            indeterminate: true
        }
    }
}



/*##^##
Designer {
    D{i:0;formeditorZoom:1.66}D{i:3}D{i:4}D{i:2}D{i:8}D{i:7}D{i:9}D{i:10}D{i:12}D{i:11}
D{i:14}D{i:13}D{i:15}D{i:16}D{i:20}D{i:1}
}
##^##*/
