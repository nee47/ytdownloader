import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Button {
    text: qsTr("Download")
    Layout.fillWidth: false
    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
    Layout.preferredHeight: 54
    Layout.preferredWidth: 217
    property var downloadHandler

    onClicked:{
        downloadButton.enabled = false
        downloadHandler()
    }
}
