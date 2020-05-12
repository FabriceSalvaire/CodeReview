/***************************************************************************************************
 *
 *  CodeReview - A Code Review GUI
 *  Copyright (C) 2019 Fabrice Salvaire
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as
 *  published by the Free Software Foundation, either version 3 of the
 *  License, or (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 *
 ***************************************************************************************************/

import QtQml 2.2
import QtQuick 2.11
import QtQuick.Controls 2.4

import CodeReview 1.0

MenuBar {
    id: root

    /*******************************************************
     *
     * API
     *
     */

    property var about_dialog
    property var options_dialog
    // application_window.close_application()

    /******************************************************/

    Action {
        id: toggle_menu_bar_action
        shortcut: 'm'
        onTriggered: visible = !visible
    }

    /******************************************************/

    Menu {
        title: qsTr('File')

        // onClosed: xxx.forceActiveFocus()

        MenuSeparator { }

        MenuItem {
            icon.name: 'settings-black'
            text: "Options"
            onTriggered: options_dialog.open()
        }

        MenuSeparator { }

        Action {
            text: qsTr('Quit')
            onTriggered: close_application()
        }
    }

    Menu {
        title: qsTr('Help')

        Action {
            text: qsTr('Documentation')
            onTriggered: Qt.openUrlExternally(application.application_url)
        }

        Action {
            text: qsTr('About')
            onTriggered: about_dialog.open()
        }
    }
}
