import QtQuick 2.15
import QtQuick.Window 2.15

Window {
    id: window
    visible: true
    title: "keylogger"
    color: "gray"
    width: 500
    height: 100
    flags:  Qt.Window
            | Qt.WindowSystemMenuHint
//            | Qt.WindowTitleHint
//            | Qt.WindowMinimizeButtonHint
//            | Qt.WindowCloseButtonHint
//            | Qt.WindowMaximizeButtonHint
            | Qt.WindowStaysOnTopHint
//            | Qt.FramelessWindowHint

    function setText(newText){
        text.text = newText
    }

    Text {
        id: text
        objectName: "text"
        text: parent.textt
        font.pixelSize: 50
        anchors.left: parent.left
        anchors.verticalCenter: parent.verticalCenter
    }
    MouseArea{
        id: iMouseArea
        property int prevX: 0
        property int prevY: 0
        anchors.fill: parent
        onPressed: {prevX=mouse.x; prevY=mouse.y}
        onPositionChanged:{
            var deltaX = mouse.x - prevX;
            iWindow.x += deltaX;
            prevX = mouse.x - deltaX;

            var deltaY = mouse.y - prevY
            iWindow.y += deltaY;
            prevY = mouse.y - deltaY;
        }
        onWheel: {
            text.font.pixelSize = text.font.pixelSize * Math.exp(wheel.angleDelta.y/1000)
            wheel.accepted = true
        }
    }
}
