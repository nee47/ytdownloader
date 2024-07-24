import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

Page{
    id: page

    Connections{
        target: backend
        function onSignalDownloadFinished(boolValue){
            GlobalVars.downloadStatus = "finished"
            return
        }

        // emited signal after pressing DOWNLOAD while downloading
        // brings a js object with the keys "eta", "elapsed" and  "speed"
        function onSignalCurrentProgress(info){
            let txtElapsed = "Elapsed Time: "
            var txtSpeed =  "Speed: "
            var txtEta = "Estimated Time: "
            if (info.elapsed === GlobalVars.lastOne) return
            else GlobalVars.lastOne = info.elapsed
            //let elapsedTime = info.elapsed + ''
            elapsedLabel.text = txtElapsed + info.elapsed +'s'

            if(info.eta)
                etaLabel.text = txtEta + info.eta + 's'

            if(info.speed)
                speedLabel.text = txtSpeed + info.speed + 'MB/s'

            return
        }

        // emited signal after pressing DOWNLOAD if something failed
        function onSignalErrorOcurred(message){
            GlobalVars.downloadStatus = "error"
            errorDialog.errorMessage = message
            errorDialog.open()
        }

    }

    Connections{
        target: language_mana
    }


    ColumnLayout {
        id: columnLayout
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter

        property string quality: comboBox.currentText
        property string outputPath: openFile.currentFolder
        property string ytUrl: textField.text

        function downloadH(){
            //progressContainer.visible = true
            backend.download(ytUrl, quality)
        }

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
                        textField.paste()
                    }
                }
            }

            placeholderText: qsTr("https://youtube.com")
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
                text: language_mana.current_lang.quality
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
                text: language_mana.current_lang.target
                Layout.preferredWidth: 180
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                Layout.preferredHeight: 47
                onClicked: {
                    openFile.open()
                }
            }
            FolderDialog{
                id: openFile
                onAccepted: {
                    backend.setOutputPath(selectedFolder)
                }
            }
        }

        DownloadButton {
            id: downloadButton
            //downloadHandler: columnLayout.downloadH
            enabled: backend?.running?false:true
            onClicked: {
                const opts = {"res":comboBox.currentText}
                backend.download(textField.text, false, opts)
            }


        }

    }

    Rectangle{
        id: progressContainer
        width: page.width * 0.90
        visible: backend?.running?true:false
        anchors.top: columnLayout.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: 12

        ProgressBar{
            id: progressBar
            anchors.horizontalCenter: parent.horizontalCenter
            width: parent.width * 0.85
            anchors.top: parent.top
            anchors.topMargin: 0
            from: 0
            to: 100
            value: backend?.progress?backend.progress:0
        }

        RowLayout{
            id: downloadInfoContainer
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: progressBar.bottom
            anchors.topMargin: 4
            spacing: 10

            Label{
                id: elapsedLabel
                text: ""
                width: 60
            }
            Label{
                id: etaLabel
                text: ""
                width: 70
            }
            Label{
                id: speedLabel
                text: ""
                width: 65
            }
        }

    }
}

/*##^##
Designer {
    D{i:0;autoSize:true;height:480;width:640}
}
##^##*/
