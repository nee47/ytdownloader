import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Page{
    id: page

    ColumnLayout{
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
            text: qsTr("Download")
        }

    }
}

/*##^##
Designer {
    D{i:0;autoSize:true;height:480;width:640}
}
##^##*/
