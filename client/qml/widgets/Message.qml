import QtQuick

Rectangle {
    id: root
    color: colors.bg2
    border.width: 0
    radius: settings.radius

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
        text: "Messaggio di prova, figo"
        font.family: "Product Sans"
        font.pixelSize: 22
        anchors.left: image.right
        anchors.leftMargin: 20
        anchors.verticalCenterOffset: 10
        anchors.verticalCenter: parent.verticalCenter
    }

    Text {
        id: user
        color: colors.text2
        text: "Nico"
        font.family: "Product Sans"
        font.pixelSize: 18
        anchors.topMargin: 5
        anchors.left: msg.left
        anchors.top: parent.top
    }

    Text {
        id: time
        color: colors.text2
        text: "15:54"
        font.family: "Product Sans"
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
