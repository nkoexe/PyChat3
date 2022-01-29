import QtQuick
import Qt5Compat.GraphicalEffects

Rectangle {
    id: root

    property string icon
    property string basecolor
    property string iconcolor: colors.icons
    property string hovercolor
    property string clickcolor: colors.primary
    property int iconmargin: 8

    color: basecolor

    function onclick () {}

    MouseArea {
        id: mouseArea
        anchors.fill: parent

        onPressed: {
            root.color = clickcolor
        }

        onReleased: {
            onclick()
            root.color = basecolor
        }

        Image {
            id: image
            visible: false
            anchors.fill: parent
            anchors.margins: iconmargin
            source: "../images/" + icon
            fillMode: Image.PreserveAspectFit
        }

        ColorOverlay {
            source: image
            color: iconcolor
            antialiasing: true
            anchors.fill: image
        }
    }
}

/*##^##
Designer {
    D{i:0;autoSize:true;formeditorZoom:10;height:30;width:30}
}
##^##*/
