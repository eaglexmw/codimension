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

from texttabwidget import TextTabWidget


class QuickHelpWidget( TextTabWidget ):
    """ Quick help screen """

    def __init__( self, parent = None ):

        TextTabWidget.__init__( self, parent )
        #pixmapPath = os.path.dirname( os.path.abspath( sys.argv[0] ) ) + \
        #             os.path.sep + 'pixmaps' + os.path.sep
        #logoPath = pixmapPath + 'logo.png'

        self.setHTML(
"""
<html>
<div>

    <h2 align="center">Keyboard Shortcut Reference</h2>

    <h3>Tools</h3>
    <p align="center">
      <table border="0" cellspacing="1"
             cellpadding="4" width="95%" align="center">
        <tr>
          <td width="15%" bgcolor="#E9E9F3">Ctrl+L</td>
          <td width="35%" bgcolor="#F6F4E4">Pylint for a file</td>
          <td width="15%" bgcolor="#E9E9F3">Ctrl+K</td>
          <td width="35%" bgcolor="#F6F4E4">Pymetrics for a file</td>
        </tr>
        <tr>
          <td bgcolor="#E9E9F3">Alt+Shift+S</td>
          <td bgcolor="#F6F4E4">Search a name</td>
          <td bgcolor="#E9E9F3">Alt+Shift+O</td>
          <td bgcolor="#F6F4E4">Search a file</td>
        </tr>
        <tr>
          <td bgcolor="#E9E9F3">Ctrl+I</td>
          <td bgcolor="#F6F4E4">Open import / select import to open</td>
          <td bgcolor="#E9E9F3"></td>
          <td bgcolor="#F6F4E4"></td>
        </tr>
      </table>
    </p>

    <br>
    <h3>IDE</h3>
    <p align="center">
      <table border="0" cellspacing="1"
             cellpadding="4" width="95%" align="center">
        <tr>
          <td width="15%" bgcolor="#E9E9F3">Ctrl+N</td>
          <td width="35%" bgcolor="#F6F4E4">New file</td>
          <td width="15%" bgcolor="#E9E9F3">F11</td>
          <td width="35%" bgcolor="#F6F4E4">Shrink sidebars</td>
        </tr>
        <tr>
          <td bgcolor="#E9E9F3">Alt+PgUp or Down</td>
          <td bgcolor="#F6F4E4">Forward or back in editing history</td>
          <td bgcolor="#E9E9F3">Ctrl+PgUp or Down</td>
          <td bgcolor="#F6F4E4">Previous or next tab</td>
        </tr>
        <tr>
          <td bgcolor="#E9E9F3">Ctrl+TAB</td>
          <td bgcolor="#F6F4E4">Switching between two recent tabs</td>
          <td bgcolor="#E9E9F3">Ctrl+Shift+F</td>
          <td bgcolor="#F6F4E4">Search in files</td>
        </tr>
      </table>
    </p>

    <br>
    <h3>Editor</h3>
    <p align="center">
      <table border="0" cellspacing="1"
             cellpadding="4" width="95%" align="center">
        <tr>
          <td width="15%" bgcolor="#E9E9F3">Ctrl+Up or Down</td>
          <td width="35%" bgcolor="#F6F4E4">Scrolling up or down without changing cursor position</td>
          <td width="15%" bgcolor="#E9E9F3">Alt+Up or Down</td>
          <td width="35%" bgcolor="#F6F4E4">Move cursor one paragraph up or down</td>
        </tr>
        <tr>
          <td bgcolor="#E9E9F3">Alt+Left or Right</td>
          <td bgcolor="#F6F4E4">Move cursor word part left or right</td>
          <td bgcolor="#E9E9F3">Ctrl+Shift+Up or Down</td>
          <td bgcolor="#F6F4E4">Select till the beginning or end of a paragraph</td>
        </tr>
        <tr>
          <td bgcolor="#E9E9F3">Ctrl+Shift+T/M/B</td>
          <td bgcolor="#F6F4E4">Jump to the first position of the first visible line/line in a middle of the visible text/last visible line</td>
          <td bgcolor="#E9E9F3">Ctrl+Z or Ctrl+Y</td>
          <td bgcolor="#F6F4E4">Undo or Redo</td>
        </tr>
        <tr>
          <td bgcolor="#E9E9F3">Shift+Del</td>
          <td bgcolor="#F6F4E4">Copy to buffer and delete selected text (if so) or current line</td>
          <td bgcolor="#E9E9F3">Ctrl+= or -</td>
          <td bgcolor="#F6F4E4">Zoom in or out</td>
        </tr>
        <tr>
          <td bgcolor="#E9E9F3">Ctrl+0</td>
          <td bgcolor="#F6F4E4">Reset zoom</td>
          <td bgcolor="#E9E9F3">Ctrl+G</td>
          <td bgcolor="#F6F4E4">Goto line</td>
        </tr>
        <tr>
          <td bgcolor="#E9E9F3">Ctrl+F</td>
          <td bgcolor="#F6F4E4">Initiate incremental search in buffer</td>
          <td bgcolor="#E9E9F3">Ctrl+R</td>
          <td bgcolor="#F6F4E4">Replace in buffer</td>
        </tr>
        <tr>
          <td bgcolor="#E9E9F3">F3 or Shift+F3</td>
          <td bgcolor="#F6F4E4">Search next or previous</td>
          <td bgcolor="#E9E9F3">Ctrl+'</td>
          <td bgcolor="#F6F4E4">Highlight current word and iterate over matches</td>
        </tr>
        <tr>
          <td bgcolor="#E9E9F3">Ctrl+, or .</td>
          <td bgcolor="#F6F4E4">Move to the previous or next highlighted word</td>
          <td bgcolor="#E9E9F3">Ctrl+M</td>
          <td bgcolor="#F6F4E4">Comment or uncomment a line or selected lines</td>
        </tr>
        <tr>
          <td bgcolor="#E9E9F3">Ctrl+Space, TAB</td>
          <td bgcolor="#F6F4E4">Code completion</td>
          <td bgcolor="#E9E9F3">Ctrl+F1</td>
          <td bgcolor="#F6F4E4">Context help</td>
        </tr>
        <tr>
          <td bgcolor="#E9E9F3">Ctrl+back slash</td>
          <td bgcolor="#F6F4E4">Goto definition</td>
          <td bgcolor="#E9E9F3">Ctrl+F3</td>
          <td bgcolor="#F6F4E4">Initiate search of the current word or selection without showing find dialog</td>
        </tr>
        <tr>
          <td bgcolor="#E9E9F3">Ctrl+]</td>
          <td bgcolor="#F6F4E4">Find occurrences of the current word</td>
          <td bgcolor="#E9E9F3">Alt+U</td>
          <td bgcolor="#F6F4E4">Jump to the beginning of the current function or class</td>
        </tr>
        <tr>
          <td bgcolor="#E9E9F3">Ctrl+forward slash</td>
          <td bgcolor="#F6F4E4">Show or hide a calltip</td>
          <td bgcolor="#E9E9F3">Alt+Shift+cursor keys</td>
          <td bgcolor="#F6F4E4">Rectangular selection</td>
        </tr>
        <tr>
          <td bgcolor="#E9E9F3">Ctrl+mouse selection</td>
          <td bgcolor="#F6F4E4">Rectangular selection</td>
          <td bgcolor="#E9E9F3">Ctrl+B</td>
          <td bgcolor="#F6F4E4">Highlight the current text cursor context in the outline browser without moving the focus</td>
        </tr>
        <tr>
          <td bgcolor="#E9E9F3">F12</td>
          <td bgcolor="#F6F4E4">Make the cursor line the first visible</td>
          <td bgcolor="#E9E9F3"></td>
          <td bgcolor="#F6F4E4"></td>
        </tr>
      </table>
    </p>

    <br>
    <h3>Debugger</h3>
    <p align="center">
      <table border="0" cellspacing="1"
             cellpadding="4" width="95%" align="center">
        <tr>
          <td width="15%" bgcolor="#E9E9F3">Shift+F5</td>
          <td width="35%" bgcolor="#F6F4E4">Start debugging the project main script with saved settings</td>
          <td width="15%" bgcolor="#E9E9F3">F5</td>
          <td width="35%" bgcolor="#F6F4E4">Start debugging the current tab script with saved settings</td>
        </tr>
        <tr>
          <td bgcolor="#E9E9F3">Ctrl+Shift+F5</td>
          <td bgcolor="#F6F4E4">Edit debugger settings and start debugging the project main script</td>
          <td bgcolor="#E9E9F3">Ctrl+F5</td>
          <td bgcolor="#F6F4E4">Edit debugger settings and start debugging the current tab script</td>
        </tr>
        <tr>
          <td bgcolor="#E9E9F3">Ctrl+F10</td>
          <td bgcolor="#F6F4E4">Stop the debugging session and kill the i/o console</td>
          <td bgcolor="#E9E9F3">F10</td>
          <td bgcolor="#F6F4E4">Stop the debugging session and keep the i/o console</td>
        </tr>
        <tr>
          <td bgcolor="#E9E9F3">F4</td>
          <td bgcolor="#F6F4E4">Restart the debugging session</td>
          <td bgcolor="#E9E9F3">F6</td>
          <td bgcolor="#F6F4E4">Continue</td>
        </tr>
        <tr>
          <td bgcolor="#E9E9F3">F7</td>
          <td bgcolor="#F6F4E4">Step in</td>
          <td bgcolor="#E9E9F3">F8</td>
          <td bgcolor="#F6F4E4">Step over</td>
        </tr>
        <tr>
          <td bgcolor="#E9E9F3">F9</td>
          <td bgcolor="#F6F4E4">Step out</td>
          <td bgcolor="#E9E9F3">Shift+F6</td>
          <td bgcolor="#F6F4E4">Run to cursor</td>
        </tr>
        <tr>
          <td bgcolor="#E9E9F3">Ctrl+W</td>
          <td bgcolor="#F6F4E4">Show the current debugger line</td>
          <td bgcolor="#E9E9F3"></td>
          <td bgcolor="#F6F4E4"></td>
        </tr>
      </table>
    </p>

    <br>
    <p align="justify">
        The industry common keys are not shown above. Please refer to
        <a href="http://satsky.spb.ru/codimension/keyBindingsEng.php">
           http://satsky.spb.ru/codimension/keyBindingsEng.php</a> for the complete list of
           bindings.
    </p>

</div>
</body>
</html>
""" )

        self.setFileName( "" )
        self.setShortName( "Quick help" )
        return

    def setFocus( self ):
        " Sets the focus to the nested html displaying editor "
        TextTabWidget.setFocus( self )
        return

