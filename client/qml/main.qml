import QtQuick
import QtQuick.Controls
import "components"


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


    Item {
        id: config
        property string fontfamily: "Product Sans"
        property color iconcolor: "#eeeeee"
        property color textcolor: "#eeeeee"
        property color basecolor: "#212121"
        property color highlight: "#44c7c3"


        property double shift1: -.05
        property double shift2: -.01
        property double shift3: +.02
        property color bg1: Qt.rgba(basecolor.r+shift1, basecolor.g+shift1, basecolor.b+shift1, 255)   // titlebar, statusbar
        property color bg2: Qt.rgba(basecolor.r+shift2, basecolor.g+shift2, basecolor.b+shift2, 255)   //
        property color bg3: Qt.rgba(basecolor.r+shift3, basecolor.g+shift3, basecolor.b+shift3, 255)   //
    }


    function setTitle (s) {
        win.title = s
        title.text = s
    }

    function setStatus (s) {
        status.text = s
    }


    Rectangle {
        id: root
        color: config.basecolor
        border.width: 0
        anchors.fill: parent

        Rectangle {
            id: titlebar
            height: 25
            color: config.bg1
            border.width: 0
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right

            CustomButton {
                id: titlebarlogo
                color: parent.color
                icon: "appicon.png"
                iconcolor: config.iconcolor
                clickcolor: config.highlight
                iconmargin: 6
                width: height
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.bottom: parent.bottom

                function onclick () {}
            }

            CustomButton {
                id: closebutton
                color: parent.color
                icon: "close.png"
                iconcolor: config.iconcolor
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
                color: parent.color
                icon: "square.png"
                iconcolor: config.iconcolor
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
                color: parent.color
                icon: "hide.png"
                iconcolor: config.iconcolor
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
                color: config.textcolor
                text: "PyChat v0.0"
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter
                font.family: config.fontfamily
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

        Rectangle {
            id: statusbar
            height: 20
            color: config.bg1
            border.width: 0
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom

            Text {
                id: status
                color: config.textcolor
                text: "Connesso"
                anchors.left: parent.left
                anchors.leftMargin: 10
                anchors.verticalCenter: parent.verticalCenter
                font.family: config.fontfamily
                font.pixelSize: 12
            }
        }

        Rectangle {
            id: chatbar
            color: config.basecolor
            border.width: 0
            anchors.top: titlebar.bottom
            anchors.bottom: statusbar.top
            anchors.left: usersbar.right
            anchors.right: parent.right

            Rectangle {
                id: currentuserbar
                height: 50
                color: config.bg3
                border.width: 0
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.right: parent.right
            }

            Rectangle {
                id: entrybar
                height: 60
                color: config.bg2
                border.width: 0
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                anchors.right: parent.right

                CustomButton {
                    id: sendbutton
                    color: parent.color
                    icon: 'send.png'
                    iconcolor: config.iconcolor
                    clickcolor: config.highlight
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
                    color: config.basecolor
                    radius: height/2
                    anchors.left: parent.left
                    anchors.right: sendbutton.left
                    anchors.leftMargin: 10
                    anchors.rightMargin: 10
                    anchors.verticalCenter: parent.verticalCenter

                    TextInput {
                        id: entry
                        focus: true
                        color: config.textcolor
                        selectionColor: "#fbb790"
                        selectedTextColor: config.textcolor
                        verticalAlignment: Text.AlignVCenter
                        anchors.fill: parent
                        anchors.margins: 5
                        anchors.leftMargin: 20
                        font.family: config.fontfamily
                        font.pointSize: 16
                    }
                }
            }

            ScrollView {
                id: chatscrollview
                anchors.top: currentuserbar.bottom
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                anchors.right: parent.right
            }
        }

        Rectangle {
            id: usersbar
            width: 237
            color: config.bg2
            border.width: 0
            anchors.bottom: statusbar.top
            anchors.left: parent.left
            anchors.top: titlebar.bottom

            Rectangle {
                id: myuserbar
                height: 50
                color: config.basecolor
                border.width: 0
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.right: parent.right
            }
        }
    }
}
