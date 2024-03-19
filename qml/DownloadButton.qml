import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Button {
    Connections{
        target: language_mana
    }
    text: language_mana.current_lang.download
    Layout.fillWidth: false
    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
    Layout.preferredHeight: 54
    Layout.preferredWidth: 217

}
