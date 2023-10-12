import QtQuick
import QtQuick.Window
import QtQuick.Controls.Material 2.3
import QtQuick.Controls 6.3
import QtQuick.Layouts 6.3
import QtQuick.Dialogs

Window {
    id: window
    width: 640
    height: 480
    visible: true
    color: "#1f2126"
    title: qsTr("YT DOWNLOADER")
    Material.theme: Material.Dark
    Material.accent: Material.Orange

    Connections{
        target: backend


        function onSignalErrorOcurred(message){
            //window.disableDownloadState()
            errorDialog.errorMessage = message
            errorDialog.open()
        }

    }

    MenuBar {
        id: menuBar

        Menu {
            font.pixelSize: 12
            title: qsTr("📄")

            Action {
                text: qsTr("Actualizar YT-DLP")
                onTriggered: {
                    console.log("ACTUALIZANDO")
                    backend.update()
                }
            }
            MenuSeparator { }
            Action { text: qsTr("Salir") }
        }
        anchors.left: parent.left
        anchors.right: parent.right
    }

    Dialog {
        id: errorDialog
        modal: true
        title: qsTr("Error")
        width: 200
        anchors.centerIn: parent
        property string errorMessage
        Text {
            id: errorName
            anchors.centerIn: parent
            text: errorDialog.errorMessage
            color: "#FFCC66"
        }
        standardButtons: Dialog.Ok
    }


    TabBar{
        id: tabBar
        anchors.top: menuBar.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        //currentIndex: tabsDisplayer.currentIndex

        TabButton{
            text: qsTr("Easy mode")
        }

        TabButton{
            text: qsTr("Mp3")
        }

    }


    StackLayout{
        id: tabsDisplayer
        y: 78
        height: 394
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: tabBar.bottom
        currentIndex: tabBar.currentIndex
        EasyTab{

        }

        Mp3Tab{

        }
    }

}


