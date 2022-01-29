import QtQuick

Rectangle {
    id: root
    height: 80
    color: colors.bg3
    border.width: 0
    radius: settings.radius

    Image {
        id: image
        source: "../images/default.png"
        fillMode: Image.PreserveAspectFit
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.margins: 20
        anchors.leftMargin: anchors.margins + 5
    }

    Text {
        id: user
        color: colors.text1
        text: "Nico"
        font.family: "Product Sans"
        font.pixelSize: 24
        font.bold: true
        anchors.left: image.right
        anchors.leftMargin: 15
        anchors.verticalCenterOffset: -10
        anchors.verticalCenter: parent.verticalCenter
    }

    Text {
        id: status
        color: colors.text2
        text: "Online"
        font.family: "Product Sans"
        font.pixelSize: 12
        anchors.leftMargin: 3
        font.italic: true
        anchors.topMargin: 2
        anchors.left: user.left
        anchors.top: user.bottom
    }
}

/*##^##
Designer {
    D{i:0;formeditorZoom:3;height:80}D{i:1}D{i:2}D{i:3}
}
##^##*/
