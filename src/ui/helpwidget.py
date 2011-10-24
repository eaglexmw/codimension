#
# -*- coding: utf-8 -*-
#
# codimension - graphics python two-way code editor and analyzer
# Copyright (C) 2010  Sergey Satskiy <sergey.satskiy@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# $Id$
#

""" Quick help screen """


import os.path
import sys
from htmltabwidget  import HTMLTabWidget


class QuickHelpWidget( HTMLTabWidget ):
    """ Quick help screen """

    def __init__( self, parent = None ):

        HTMLTabWidget.__init__( self, parent )
        pixmapPath = os.path.dirname( os.path.abspath( sys.argv[0] ) ) + \
                     os.path.sep + 'pixmaps' + os.path.sep
        logoPath = pixmapPath + 'logo.png'

        self.setHTML( \
"""
<html>
<body bgcolor="#ffffe6">

    <h2 align="left" style="color: #666">Keyboard Shortcut Reference</h2>

    <h3 style="color: #666">Tools</h3>
    <p align="center">
      <table border="1" cellspacing="0"
             cellpadding="1" width="95%" align="center">
        <tr>
          <td>Ctrl+L</td>
          <td>Pylint for a file</td>
          <td>Ctrl+K</td>
          <td>Pymetrics for a file</td>
        </tr>
      </table>
    </p>

    <h3 style="color: #666">IDE</h3>
    <p align="center">
      <table border="1" cellspacing="0"
             cellpadding="1" width="95%" align="center">
        <tr>
          <td>Ctrl+T</td>
          <td>New tab</td>
          <td>F11</td>
          <td>Shrink sidebars</td>
        </tr>
        <tr>
          <td>Alt+PgUp/Down</td>
          <td>Forward/back in editing history</td>
          <td>Ctrl+PgUp/Down</td>
          <td>Next/previous tab</td>
        </tr>
        <tr>
          <td>Ctrl+TAB</td>
          <td>Switching between two recent tabs</td>
          <td>Alt+Shift+S</td>
          <td>Search a name</td>
        </tr>
        <tr>
          <td>Alt+Shift+O</td>
          <td>Search a file</td>
          <td>Ctrl+Shift+F</td>
          <td>Search in files</td>
        </tr>
      </table>
    </p>

    <h3 style="color: #666">Editor</h3>
    <p align="center">
      <table border="1" cellspacing="0"
             cellpadding="1" width="95%" align="center">
        <tr>
          <td>Ctrl+Up/Down</td>
          <td>Scrolling up/down without changing cursor position</td>
          <td>Alt+Up/Down</td>
          <td>Move cursor one paragraph up/down</td>
        </tr>
        <tr>
          <td>Alt+Left/Right</td>
          <td>Move cursor word part left/right</td>
          <td>Alt+Shift+Up/Down</td>
          <td>Select till the beginning/end of a paragraph</td>
        </tr>
        <tr>
          <td>Alt+Shift+Left/Right</td>
          <td>Select word part</td>
          <td>Ctrl+Z/Ctrl+Shift+Z</td>
          <td>Undo/Redo</td>
        </tr>
        <tr>
          <td>Shift+Del</td>
          <td>Copy to buffer and delete selected text (if so) or current line</td>
          <td>Ctrl++/-</td>
          <td>Zoom in/out</td>
        </tr>
        <tr>
          <td>Ctrl+0</td>
          <td>Reset zoom</td>
          <td>Ctrl+G</td>
          <td>Goto line</td>
        </tr>
        <tr>
          <td>Ctrl+F</td>
          <td>Incremental search in buffer</td>
          <td>Ctrl+R</td>
          <td>Replace in buffer</td>
        </tr>
        <tr>
          <td>F3/Shift+F3</td>
          <td>Search next/previous</td>
          <td>Ctrl+N</td>
          <td>Highlight current word</td>
        </tr>
        <tr>
          <td>Ctrl+I</td>
          <td>Open import/select import to open</td>
          <td>Ctrl+M</td>
          <td>Comment/uncomment a line or selected lines</td>
        </tr>
      </table>
    </p>

    <p>
        The industry common hot keys are not shown above. Please refer to
        <a href="http://satsky.spb.ru/codimension/keyBindings.php">
           http://satsky.spb.ru/codimension/keyBindings.php</a> for the complete list of
           bindings.
    </p>

</body>
</html>
""" )

        self.setFileName( "" )
        self.setShortName( "Quick help" )
        return

    def setFocus( self ):
        " Sets the focus to the nested html displaying editor "
        HTMLTabWidget.setFocus( self )
        return

