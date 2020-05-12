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

import QtQuick 2.11
import QtQuick.Controls 2.4
import QtQuick.Layouts 1.11

import CodeReview 1.0
import Widgets 1.0 as Widgets
import UserInterface 1.0 as Ui

ApplicationWindow {
    id: application_window

    /*******************************************************
     *
     * API
     *
     */

     property var shortcuts: null

    function close_application(close) {
        console.info('Close application')
        show_message(qsTr('Close ...'))
        if (!close)
            Qt.quit()
        // else
        //    close.accepted = false
    }

    function clear_message() {
        footer_tool_bar.message = ''
    }

    function show_message(message) {
        footer_tool_bar.message = message
    }

    /*******************************************************
     *
     *
     */

    title: qsTr('Code Review') // Fixme: ???
    visible: true
    width: 1000
    height: 500

    Component.onCompleted: {
        console.info('ApplicationWindow.onCompleted')
        application.show_message.connect(on_message)
        application.show_error.connect(on_error)
        application_window.showMaximized()

        // Fixme: prevent crash when opening option dialog
        //   RuntimeError: wrapped C/C++ object of type Shortcut has been deleted
        let _shortcuts = application_settings.shortcuts
        shortcuts = {} // []
        /* for (var shortcut in _shortcuts) */
        /*     console.info('shortcut', shortcut) */
        for (var i = 0; i < _shortcuts.length; i++) {
            var shortcut = _shortcuts[i]
            shortcuts[shortcut.name] = shortcut
            // shortcuts.push(shortcut)
        }
    }

    function on_message(message) {
        error_message_dialog.open_with_message(message)
    }

    function on_error(message, backtrace) {
        var text = message + '\n' + backtrace
        error_message_dialog.open_with_message(text)
    }

    /*******************************************************
     *
     * Slots
     *
     */

    onClosing: close_application(close)

    /*******************************************************
     *
     * Dialogs
     *
     */

    Widgets.AboutDialog {
        id: about_dialog
        title: qsTr('About Code Review')
        about_message: application.about_message // qsTr('...')
    }

    Widgets.ErrorMessageDialog {
        id: error_message_dialog
        title: qsTr('An error occurred in Code Review')
    }

    Ui.OptionsDialog {
        id: options_dialog
    }

    /*******************************************************
     *
     * Actions
     *
     */

    Ui.Actions {
        id: actions
    }

    /*******************************************************
     *
     * Menu
     *
     */

    // Fixme: use native menu ???
    menuBar: Ui.MenuBar {
        id: menu_bar
        about_dialog: about_dialog
        options_dialog: options_dialog
    }

    /*******************************************************
     *
     * Header
     *
     */

    /* header: Ui.HeaderToolBar { */
    /*     id: header_tool_bar */
    /*     actions: actions */
    /* } */

    /*******************************************************
     *
     * Items
     *
     */

    /*******************************************************
     *
     * Footer
     *
     */

    footer: Ui.FooterToolBar {
        id: footer_tool_bar
    }
}
