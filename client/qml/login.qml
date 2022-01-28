import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material


Window {
    id: win
    title: "PyChat Login"
    width: 500
    height: 450
    visible: true
    color: "#00000000"
    flags: Qt.FramelessWindowHint | Qt.Window


    Material.theme: Material.Dark
    Material.accent: colors.highlight


    function exitCode (v) {
        console.log('loading closed')
        if (v === 0) {
            win.close()
        }
    }

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
                text: "PyChat - Login"
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
                        color: closebutton.pressed ? colors.highlight : (closebutton.hovered ? "#09ffffff" : "transparent")
                    }
                }

                onReleased: {
                    win.close()
                }
            }
        }

        TextField {
            id: username
            width: parent.width/1.5
            font.pointSize: 14
            anchors.top: mousearea.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.topMargin: 60
            placeholderText: "Username"
        }

        TextField {
            id: password
            width: parent.width/1.5
            font.pointSize: 14
            anchors.top: username.bottom
            anchors.topMargin: 20
            anchors.horizontalCenter: parent.horizontalCenter
            placeholderText: "Password"
            echoMode: "Password"
        }

        Button {
            id: login
            width: parent.width/1.5
            text: "Login"
            font.pointSize: 12
            anchors.top: password.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.topMargin: 25

            onReleased: {
                if (username.text && password.text) {
                    progressBar.visible = true
                    let code = backend.submitLogin(username.text, password.text)
                    if (code === -1) {
                        console.log("nope :/")
                    }
                    progressBar.visible = false
                }
            }
        }

        Text {
            id: nonhaiacc
            text: "Non hai un account?"
            color: colors.text1
            anchors.top: login.bottom
            anchors.horizontalCenterOffset: -40
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.topMargin: 35
            font.family: settings.font
            font.pixelSize: 12
        }

        Button {
            id: button
            text: "Registrati"
            anchors.verticalCenter: nonhaiacc.verticalCenter
            anchors.left: nonhaiacc.right
            anchors.verticalCenterOffset: -2
            anchors.leftMargin: 10

            onReleased: {
                backend.openSignup()
                win.close()
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


