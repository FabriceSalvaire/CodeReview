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

import QtQml.Models 2.2
import QtQuick 2.11
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.11

import CodeReview 1.0
import Widgets 1.0 as Widgets

Widgets.CentredDialog {
    id: dialog
    implicitWidth: 800
    implicitHeight: 400

    standardButtons: Dialog.Ok | Dialog.Cancel

    // onAccepted:
    // onRejected:

    /******************************************************/

    header: TabBar {
        id: tab_bar

        TabButton {
            text: qsTr("General")
	}

        TabButton {
            text: qsTr("Shortcuts")
        }
    }

    StackLayout {
        anchors.fill: parent
        currentIndex: tab_bar.currentIndex

        Item {
            id: shortcut_list_view_container

            ListView {
                id: shortcut_list_view
                anchors.fill: parent
                clip: true

                //! model: application_settings.shortcuts

                delegate: Widgets.ShortcutRow {
                    width: parent.width
                    shortcut: modelData
                }
            }
        }
    }
}
