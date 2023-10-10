import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

Page{
    id: page

    ColumnLayout {
        id: columnLayout
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter


        spacing: 17

        Text {
            id: text1
            text: qsTr("LINK")
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
            Menu {
                id: myMenu
                Action {
                    text: "pegar"
                    onTriggered: {
                        console.log("PEGADO")
                        textField.paste()
                    }
                }
            }

            placeholderText: qsTr("ejemplo: https://youtube.com")
            placeholderTextColor: "#808080"
            color: "white"
            horizontalAlignment: "AlignHCenter"
            selectByMouse: true
            Layout.fillHeight: false
            Layout.preferredHeight: 44
            Layout.preferredWidth: 400
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

            onReleased: (e)=>{
                if (e.button === Qt.RightButton)
                    myMenu.popup()
            }
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

        Rectangle{
            border.color: "#eb4465"
            color: "transparent"
            Layout.preferredHeight: 120
            Layout.preferredWidth: 300
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            radius: 3

            Text {
                id: infoText
                font.pixelSize: 12
                horizontalAlignment: Text.AlignHCenter
                anchors.fill: parent
                Layout.rowSpan: 1
                color: "#fff"
                wrapMode: Text.Wrap

            }
            visible: false

        }

        Button {
            id: downloadButton
            text: qsTr("Descargar")
            Layout.fillWidth: false
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Layout.preferredHeight: 54
            Layout.preferredWidth: 217

            onClicked: {
                progressBar.visible = true
                downloadButton.enabled = false
                backend.download(comboBox.currentText, textField.text)
            }
        }

    }

    ProgressBar{
        id: progressBar
        from: 0
        to: 100
        visible: false
        value: 0
        anchors.top: columnLayout.bottom
        anchors.topMargin: 12
        anchors.horizontalCenter: parent.horizontalCenter
        function enableView(){
            progressBar.visible = true

        }

        function disableView(){
            progressBar.visible = false
            progressBar.value = 0
        }

    }
}

/*##^##
Designer {
    D{i:0;autoSize:true;height:480;width:640}
}
##^##*/
