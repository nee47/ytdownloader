import QtQuick 2.9
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

        function onSignalDownload(boolValue){
            window.disableDownloadState()
            return
        }

        function onSignalCurrentProgress(current_numb){
            progressBar.value = current_numb
            return
        }

        function onSignalErrorOcurred(message){
            window.disableDownloadState()
            errorDialog.errorMessage = message
            errorDialog.open()
        }

    }

    function disableDownloadState(){
        downloadButton.enabled = true
        progressBar.disableView()
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

    ColumnLayout {
        id: columnLayout
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.topMargin: 124
        anchors.bottomMargin: 113
        anchors.rightMargin: 56
        anchors.leftMargin: 82
        spacing: 15

        Text {
            id: text1
            text: qsTr("INGRESA EL LINK")
            font.pixelSize: 17
            horizontalAlignment: Text.AlignHCenter
            Layout.rowSpan: 1
            Layout.preferredHeight: 35
            Layout.preferredWidth: 142
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            color: "#eb4465"
        }
        TextField{
            id: textField
            placeholderText: qsTr("ejemplo: https://youtube.com")
            placeholderTextColor: "#808080"
            color: "white"
            horizontalAlignment: "AlignHCenter"
            selectByMouse: true
            Layout.fillHeight: false
            Layout.preferredHeight: 44
            Layout.preferredWidth: 400
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
        }

        RowLayout {
            id: rowLayout
            spacing: 21
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Text {
                id: text2
                text: qsTr("Calidad")
                font.pixelSize: 15
                color: "#eb4465"
                horizontalAlignment: Text.AlignRight
                Layout.preferredWidth: 58
            }
            ComboBox {
                id: comboBox
                rightPadding: 15
                font.pointSize: 12
                currentIndex: 2
                Layout.preferredHeight: 47
                Layout.preferredWidth: 87
                model: ["720p", "1080p", "2k"]
            }
            Button {
                id: buttonTargetPath
                text: qsTr("Carpeta Destino")
                Layout.preferredWidth: 143
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                Layout.preferredHeight: 47
                onClicked: {
                    openFile.open()
                }
            }
            FolderDialog{
                id: openFile
                onAccepted: {
                    backend.getFolderPath(selectedFolder)
                }
            }

        }

        Button {
            id: downloadButton
            text: qsTr("Descargar")
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Layout.preferredHeight: 54
            Layout.preferredWidth: 217

            onClicked: {
                progressBar.visible = true
                downloadButton.enabled = false
                backend.download(comboBox.currentText, textField.text)
            }
        }

        ProgressBar{
            id: progressBar
            from: 0
            to: 100
            visible: false
            value: 0
            Layout.preferredHeight: 20
            Layout.fillWidth: true
            function enableView(){
                progressBar.visible = true

            }

            function disableView(){
                progressBar.visible = false
                progressBar.value = 0
            }

        }

    }
}


