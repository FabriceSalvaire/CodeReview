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

// cf. http://wiki.qt.io/Qml_Styling

// Fixme: lupdate
pragma Singleton
import QtQml 2.11
import QtQuick 2.6

QtObject {

    property QtObject color: QtObject {
        // property color primary: darken('#428bca', 0.65)
        // property color success: '#5cb85c'
        // property color info:    '#5bc0de'
        // property color warning: '#f0ad4e'
        // property color danger:  '#d9534f'

        property color primary: '#007bff'
        property color success: '#28a745'
        property color info:    '#17a2b8'
        property color warning: '#ffc107'
        property color danger:  '#dc3545'

        property color orange: '#e67e22'

        // "#5cb85c" hsv 120 128 184
        // "#f0ad4e" hsv 35 172 240
    }

    property QtObject font_size: QtObject {
        property int tiny:   8
        property int small: 10
        property int base:  12
        property int large: 18
        property int huge:  20
    }

    property QtObject spacing: QtObject {
        property int xs:     1
        property int small:  5
        property int base:  10
        property int large: 20
        property int huge:  30

        property int xs_horizontal:     1
        property int small_horizontal:  5
        property int base_horizontal:  10
        property int large_horizontal: 20

        property int xs_vertical:       1
        property int small_vertical:    5
        property int base_vertical:    10
        property int large_vertical:   20
    }
}
