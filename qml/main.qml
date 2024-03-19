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

    Connections{
        target: language_mana
    }

    MenuBar {
        id: menuBar

        ActionGroup {
                id: langeActions
        }

        Menu {
            font.pixelSize: 12
            title: qsTr("📄")

            Action {
                id: act1
                text: qsTr("en")
                checkable: true
                ActionGroup.group: langeActions
                checked: true
                onTriggered: {
                    console.log("ACTUALIZANDO")
                    backend.update()
                    act1.checked = true
                    language_mana.update_language("en")

                }
            }

            Action {
                id: act2
                text: qsTr("es")
                checkable: true
                ActionGroup.group: langeActions
                onTriggered: {
                    console.log("ACTUALIZANDO")
                    backend.update()
                    act2.checked = true
                    language_mana.update_language("es")
                }
            }
            MenuSeparator { }
            Action {
                text: language_mana.current_lang.exit
                onTriggered: {
                    Qt.quit()
                }
            }
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
            text: language_mana.current_lang.tab1
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


