import QtQuick 2.9
import QtQuick.Controls 2.5

Rectangle{
    Column{
        id: column
        width: parent.width/2
        height: parent.height
        spacing: 0
        padding: 0
        anchors.horizontalCenter: parent.horizontalCenter
        Rectangle{
            id: rectangle
            width: 94
            height: 60

            TextArea{
                id: txtt
                text: qsTr("probando")
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.right: parent.right
            }

            Button{
                width: 56
                height: 30
                text: "hola"
                anchors.top: txtt.bottom
            }
        }

        Rectangle {
            id: rectangle1
            width: parent.width
            height: 60

            TextArea {
                id: txtt1
                text: qsTr("probando")
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
            }

            Button {
                width: parent.width
                height: 30
                text: "hola"
                anchors.top: txtt1.bottom
            }

        }


    }

}
