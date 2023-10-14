import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Page{
    id: page
    Connections{
        target: backend


        // emited signal after pressing DOWNLOAD while downloading
        // brings a js object with the keys "eta", "elapsed" and  "speed"
        function onSignalCurrentProgressAudio(info){
            //speedLabel.text = info
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

    ColumnLayout{
        id: downloadContainer
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter

        Text{
            text: qsTr("LINK:")
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


        DownloadButton{
            id: dButton
            text: qsTr("Download")
            onClicked: {
                const opts = {"ext":'mp3'}
                backend.download(textField.text, true, opts)
            }
        }

    }

    Rectangle{
        id: progressContainer
        width: page.width * 0.90
        visible: backend?.running?true:false
        anchors.top: downloadContainer.bottom
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
