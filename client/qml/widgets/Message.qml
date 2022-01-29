import QtQuick

Rectangle {
    id: root
    height: 70
    color: colors.bg3
    border.width: 0
    radius: settings.radius

    property string _user
    property string _time
    property string _text

    Image {
        id: image
        source: "../images/default.png"
        fillMode: Image.PreserveAspectFit
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.margins: 10
        anchors.leftMargin: anchors.margins + 5
    }

    Text {
        id: msg
        color: colors.text1
        text: _text
        font.family: settings.font
        font.pixelSize: 22
        anchors.left: image.right
        anchors.leftMargin: 20
        anchors.verticalCenterOffset: 10
        anchors.verticalCenter: parent.verticalCenter
    }

    Text {
        id: user
        color: colors.text2
        text: _user
        font.family: settings.font
        font.pixelSize: 18
        anchors.topMargin: 5
        anchors.left: msg.left
        anchors.top: parent.top
    }

    Text {
        id: time
        color: colors.text2
        text: _time
        font.family: settings.font
        font.pixelSize: 12
        anchors.bottomMargin: 2
        anchors.left: user.right
        anchors.bottom: user.bottom
        anchors.leftMargin: 10
    }
}

/*##^##
Designer {
    D{i:0;autoSize:true;formeditorZoom:2;height:70;width:730}D{i:1}D{i:2}D{i:3}D{i:4}
}
##^##*/
