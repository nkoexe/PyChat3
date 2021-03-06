import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "components"
import "widgets"

/*
TODO:
- Pulsante maximize deve ripristinare forma originale quando premuto 2a volta
  * Creare variabile per salvare stato, poi applicare i valori quando premuto (Animazione?)
- mouseArea lungo i bordi e angoli per ridimensionare finestra

*/



Window {
    id: win
    width: 1000
    height: 600
    visible: true
    color: "#00000000"
    minimumHeight: 100
    minimumWidth: 300
    title: "PyChat"
    flags: Qt.FramelessWindowHint | Qt.Window


    onClosing: {
        backend.close()
    }


    function setTitle (s) {
        win.title = s
        title.text = s
    }

    function setStatus (s) {
        status.text = s
    }

    function createMessage(user, time, text) {
        var comp = Qt.createComponent("widgets/Message.qml")
        var sprite = comp.createObject(chatlayout, {_user:user, _time:time, _text:text})
        sprite.Layout.fillWidth = true

        // Fixme: trovare altro modo per allineare in basso i messaggi 
        spacer.Layout.preferredHeight = spacer.Layout.preferredHeight - sprite.height - settings.margins
    }


    Rectangle {
        id: root
        color: colors.bg1
        border.width: 0
        anchors.fill: parent

        Rectangle {
            id: chatbar
            color: colors.bg1
            border.width: 0
            anchors.top: titlebar.bottom
            anchors.bottom: statusbar.top
            anchors.left: usersbar.right
            anchors.right: parent.right

            Rectangle {
                id: currentuserbar
                height: 50
                color: colors.bg2
                border.width: 0
                radius: settings.radius
                anchors.top: parent.top
                anchors.rightMargin: settings.margins
                anchors.leftMargin: settings.margins
                anchors.topMargin: settings.margins
                anchors.left: parent.left
                anchors.right: parent.right

                CustomButton {
                    id: themebutton
                    width: height
                    radius: width/2
                    icon: 'reload.png'
                    basecolor: colors.bg2
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    anchors.topMargin: 4
                    anchors.bottomMargin: 4
                    anchors.rightMargin: 10

                    function onclick () {
                        backend.switchTheme()
                    }
                }
            }

            Rectangle {
                id: entrybar
                height: 60
                color: colors.bg2
                border.width: 0
                radius: settings.radius
                anchors.bottom: parent.bottom
                anchors.rightMargin: settings.margins
                anchors.leftMargin: settings.margins
                anchors.bottomMargin: settings.margins
                anchors.left: parent.left
                anchors.right: parent.right

                CustomButton {
                    id: sendbutton
                    basecolor: parent.color
                    icon: 'send.png'
                    iconcolor: colors.icons
                    clickcolor: colors.primary
                    iconmargin: 12
                    height: parent.height
                    width: height
                    anchors.right: parent.right
                    anchors.rightMargin: 10
                    anchors.verticalCenter: parent.verticalCenter

                    function onclick () {
                        console.log(entry.text)
                    }
                }

                Rectangle {
                    height: parent.height/1.5
                    color: colors.bg1
                    radius: height/2
                    anchors.left: parent.left
                    anchors.right: sendbutton.left
                    anchors.leftMargin: 10
                    anchors.rightMargin: 10
                    anchors.verticalCenter: parent.verticalCenter

                    TextInput {
                        id: entry
                        focus: true
                        color: colors.text1
                        selectByMouse: true
                        selectionColor: colors.primary
                        selectedTextColor: colors.text1
                        verticalAlignment: Text.AlignVCenter
                        anchors.fill: parent
                        anchors.margins: 5
                        anchors.leftMargin: 20
                        font.family: settings.font
                        font.pointSize: 16

                        onAccepted: {
                            backend.send('msg', text)
                            entry.clear()
                        }
                    }
                }
            }

            ScrollView {
                id: chatscrollview
                anchors.top: currentuserbar.bottom
                // anchors.topMargin: chatlayout.height
                anchors.bottom: entrybar.top
                anchors.bottomMargin: settings.margins
                anchors.left: parent.left
                anchors.right: parent.right

                Shortcut {
                    sequence: "Esc"
                    onActivated: {
                        let comp = Qt.createComponent("widgets/Message.qml")
                        let sprite = comp.createObject(chatlayout, {height: 70})
                        sprite.Layout.fillWidth = true
                    }
                }

                ColumnLayout {
                    id: chatlayout
                    anchors.fill: parent
                    anchors.leftMargin: settings.margins
                    anchors.rightMargin: settings.margins
                    spacing: settings.margins
                    
                    Item {
                        id: spacer
                        Layout.fillWidth: true
                        Layout.preferredHeight: chatscrollview.height
                        Rectangle { anchors.fill: parent; color: '#ffaaaa'}
                    }
                }
            }
        }

        Rectangle {
            id: usersbar
            width: 237
            color: colors.bg2
            border.width: 0
            radius: settings.radius
            anchors.bottom: statusbar.top
            anchors.leftMargin: settings.margins
            anchors.bottomMargin: settings.margins
            anchors.topMargin: settings.margins
            anchors.left: parent.left
            anchors.top: titlebar.bottom

            Rectangle {
                id: myuserbar
                height: currentuserbar.height
                color: colors.primary
                border.width: 0
                radius: settings.radius
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.right: parent.right
            }

            ScrollView {
                id: userscrollview
                anchors.right: parent.right
                anchors.left: parent.left
                anchors.bottom: parent.bottom
                anchors.top: myuserbar.bottom

                ColumnLayout {
                    id: userlayout
                    anchors.fill: parent
                    anchors.margins: settings.margins
                    spacing: settings.margins

                    User {
                        Layout.fillWidth: true
                    }
                }
            }
        }

        Rectangle {
            id: statusbar
            height: 20
            color: colors.titlebar
            border.width: 0
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom

            Text {
                id: status
                color: colors.text1
                text: "Connesso"
                anchors.left: parent.left
                anchors.leftMargin: 10
                anchors.verticalCenter: parent.verticalCenter
                font.family: settings.font
                font.pixelSize: 12
            }
        }

        Rectangle {
            id: titlebar
            height: 25
            color: colors.titlebar
            border.width: 0
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right

            CustomButton {
                id: titlebarlogo
                basecolor: colors.titlebar
                icon: "appicon.png"
                iconcolor: colors.icons
                clickcolor: colors.primary
                iconmargin: 6
                width: height
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.bottom: parent.bottom

                function onclick () {}
            }

            CustomButton {
                id: closebutton
                basecolor: colors.titlebar
                icon: "close.png"
                iconcolor: colors.icons
                clickcolor: "#eb4034"
                width: height
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.right: parent.right

                function onclick () {
                    win.close()
                }
            }

            CustomButton {
                id: maximizebutton
                basecolor: colors.titlebar
                icon: "square.png"
                iconcolor: colors.icons
                clickcolor: "#43bf30"
                width: height
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.right: closebutton.left

                function onclick () {
                    if (win.Maximized)
                        win.showNormal()
                    else
                        win.showMaximized()
                }
            }

            CustomButton {
                id: hidebutton
                basecolor: colors.titlebar
                icon: "hide.png"
                iconcolor: colors.icons
                clickcolor: "#e6ad3c"
                width: height
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.right: maximizebutton.left

                function onclick () {
                    win.showMinimized()
                }
            }

            Text {
                id: title
                color: colors.text1
                text: "PyChat v0.0"
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter
                font.family: settings.font
                font.pixelSize: 12
            }

            MouseArea {
                id: titlebarmousearea
                anchors.left: titlebarlogo.right
                anchors.right: hidebutton.left
                anchors.top: parent.top
                anchors.bottom: parent.bottom

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


                onDoubleClicked: {
                    if (win.Maximized)
                        win.showNormal()
                    else
                        win.showMaximized()
                }
            }
        }
    }
}

/*##^##
Designer {
    D{i:0;formeditorZoom:1.25}D{i:4}D{i:3}D{i:6}D{i:8}D{i:7}D{i:5}D{i:10}D{i:12}D{i:13}
D{i:11}D{i:9}D{i:2}D{i:15}D{i:18}D{i:17}D{i:16}D{i:14}D{i:20}D{i:19}D{i:22}D{i:23}
D{i:24}D{i:25}D{i:26}D{i:27}D{i:21}D{i:1}
}
##^##*/
