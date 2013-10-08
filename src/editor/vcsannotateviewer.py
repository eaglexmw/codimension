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

" Annotated VCS viewer implementation "


from texteditor import TextEditor
import os.path
from PyQt4.QtCore import Qt, SIGNAL, QSize, QPoint
from PyQt4.QtGui import ( QToolBar, QFont, QFontMetrics, QHBoxLayout, QWidget,
                          QAction, QSizePolicy, QToolTip )
from PyQt4.Qsci import QsciScintilla
from ui.mainwindowtabwidgetbase import MainWindowTabWidgetBase
from utils.fileutils import ( detectFileType, getFileLanguage, DesignerFileType,
                              UnknownFileType, PythonFileType, Python3FileType,
                              LinguistFileType )
from utils.pixmapcache import PixmapCache
from utils.globals import GlobalData
from utils.settings import Settings
from utils.importutils import ( getImportsList, getImportsInLine, resolveImport,
                                getImportedNameDefinitionLine, resolveImports )
from ui.importlist import ImportListWidget
from ui.linecounter import LineCounterDialog
from utils.encoding import decode
from autocomplete.bufferutils import isImportLine
from PyQt4.Qsci import QsciStyle



class VCSAnnotateViewer( TextEditor ):

    LINENUM_MARGIN = 0      # Matches the text editor
    REVISION_MARGIN = 1     # Introduced here
    FOLDING_MARGIN = 2      # Matches the text editor
    MESSAGES_MARGIN = 3     # Matches the text editor

    def __init__( self, parent ):
        self.__maxLength = None

        TextEditor.__init__( self, parent, None )
        self.__revisionTooltipShown = False
        self.__initAlterRevisionMarker()
        self._updateDwellingTime()
        return

    def __initAlterRevisionMarker( self ):
        skin = GlobalData().skin
        self.__alterMarker = self.markerDefine( QsciScintilla.Background )
        self.setMarkerBackgroundColor( skin.revisionAlterPaper,
                                       self.__alterMarker )
        return

    def setAnnotatedContent( self, shortName, text, lineRevisions, revisionInfo ):
        " Sets the content "
        self.__lineRevisions = lineRevisions
        self.__revisionInfo = revisionInfo

        fileType = self.parent().getFileType()
        if fileType in [ DesignerFileType, LinguistFileType ]:
            # special treatment for Qt-Linguist and Qt-Designer files
            self.encoding = 'latin-1'
        else:
            text, self.encoding = decode( text )

        self.detectEolString( text )
        self.setText( text )
        self.bindLexer( shortName, fileType )

        self.setModified( False )
        self.setReadOnly( True )

        self.__initAnnotateMargins()
        self.__setRevisionText()
        return

    def __setRevisionText( self ):
        " Sets the revision margin text "
        for revNumber in self.__revisionInfo:
            author = self.__revisionInfo[ revNumber ][ 'author' ]
            if '@' in author:
                # Most probably this is an e-mail address. Leave just name.
                self.__revisionInfo[ revNumber ][ 'shortAuthor' ] = author.split( '@' )[ 0 ]
            else:
                self.__revisionInfo[ revNumber ][ 'shortAuthor' ] = author

        skin = GlobalData().skin
        revisionMarginFont = QFont( skin.lineNumFont )
        revisionMarginFont.setItalic( True )
        style = QsciStyle( -1, "Revision margin style",
                           skin.revisionMarginColor,
                           skin.revisionMarginPaper, revisionMarginFont )

        lineNumber = 0
        self.__maxLength = -1

        # Altering line background support
        currentRevision = -1
        needMarker = True

        for lineRevision in self.__lineRevisions:
            marginText = " " + ":".join( [ str( lineRevision ),
                    self.__revisionInfo[ lineRevision ][ 'shortAuthor' ] ] )
            textLength = len( marginText )
            if textLength > self.__maxLength:
                self.__maxLength = textLength
            self.setMarginText( lineNumber, marginText, style )

            # Set the line background if needed
            if lineRevision != currentRevision:
                currentRevision = lineRevision
                needMarker = not needMarker
            if needMarker:
                self.markerAdd( lineNumber, self.__alterMarker )

            lineNumber += 1

        self.setRevisionMarginWidth()
        return

    def detectRevisionMarginWidth( self ):
        """ Caculates the margin width depending on
            the margin font and the current zoom """
        skin = GlobalData().skin
        font = QFont( skin.lineNumFont )
        font.setPointSize( font.pointSize() + self.getZoom() )
        fontMetrics = QFontMetrics( font, self )
        return fontMetrics.width( 'W' * self.__maxLength ) + 3

    def setRevisionMarginWidth( self ):
        " Called when zooming is done to keep the width wide enough "
        if self.__maxLength:
            self.setMarginWidth( self.REVISION_MARGIN,
                                 self.detectRevisionMarginWidth() )
        else:
            self.setMarginWidth( self.REVISION_MARGIN, 0 )
        return

    def __initAnnotateMargins( self ):
        " Initializes the editor margins "
        self.setMarginType( self.REVISION_MARGIN, self.TextMargin )
        self.setMarginMarkerMask( self.REVISION_MARGIN, 0 )

        # Together with overriding _marginClicked(...) this
        # prevents selecting a line when the margin is clicked.
        self.setMarginSensitivity( self.REVISION_MARGIN, True )
        return

    def _marginClicked( self, margin, line, modifiers ):
        return

    def __getRevisionMarginTooltip( self, lineNumber ):
        " lineNumber is zero based "
        revisionNumber = self.__lineRevisions[ lineNumber ]
        if not revisionNumber in self.__revisionInfo:
            return None

        tooltip = "Revision: " + \
                    str( revisionNumber ) + "\n" \
                  "Author: " + \
                    self.__revisionInfo[ revisionNumber ][ 'author' ] + "\n" \
                  "Date: " + \
                    str( self.__revisionInfo[ revisionNumber ][ 'date' ] )
        comment = self.__revisionInfo[ revisionNumber ][ 'message' ]
        if comment:
            tooltip += "\nComment: " + comment
        return tooltip

    def _updateDwellingTime( self ):
        " There is always something to show "
        self.SendScintilla( self.SCI_SETMOUSEDWELLTIME, 250 )
        return

    def _onDwellStart( self, position, x, y ):
        " Triggered when mouse started to dwell "
        if not self.underMouse():
            return

        marginNumber = self._marginNumber( x )
        if marginNumber == self.REVISION_MARGIN:
            self.__showRevisionTooltip( position, x, y )
            return

        TextEditor._onDwellStart( self, position, x, y )
        return

    def __showRevisionTooltip( self, position, x, y ):
        # Calculate the line
        pos = self.SendScintilla( self.SCI_POSITIONFROMPOINT, x, y )
        line, posInLine = self.lineIndexFromPosition( pos )

        tooltip = self.__getRevisionMarginTooltip( line )
        if not tooltip:
            return

        QToolTip.showText( self.mapToGlobal( QPoint( x, y ) ), tooltip )
        self.__revisionTooltipShown = True
        return

    def _onDwellEnd( self, position, x, y ):
        " Triggered when mouse ended to dwell "
        if self.__revisionTooltipShown:
            self.__revisionTooltipShown = False
            QToolTip.hideText()
        return

    def setLineNumMarginWidth( self ):
        TextEditor.setLineNumMarginWidth( self )
        self.setRevisionMarginWidth()
        return



class VCSAnnotateViewerTabWidget( QWidget, MainWindowTabWidgetBase ):
    " VCS annotate viewer tab widget "

    def __init__( self, parent ):

        MainWindowTabWidgetBase.__init__( self )
        QWidget.__init__( self, parent )

        self.__viewer = VCSAnnotateViewer( self )
        self.__fileName = ""
        self.__shortName = ""
        self.__fileType = UnknownFileType

        self.__createLayout()
        self.__viewer.zoomTo( Settings().zoom )
        return

    def __createLayout( self ):
        " Creates the toolbar and layout "

        # Buttons
        printButton = QAction( PixmapCache().getIcon( 'printer.png' ),
                               'Print', self )
        self.connect( printButton, SIGNAL( 'triggered()' ),
                      self.__onPrint )
        printButton.setEnabled( False )
        printButton.setVisible( False )

        printPreviewButton = QAction(
                PixmapCache().getIcon( 'printpreview.png' ),
                'Print preview', self )
        self.connect( printPreviewButton, SIGNAL( 'triggered()' ),
                      self.__onPrintPreview )
        printPreviewButton.setEnabled( False )
        printPreviewButton.setVisible( False )

        spacer = QWidget()
        spacer.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Expanding )

        self.lineCounterButton = QAction(
            PixmapCache().getIcon( 'linecounter.png' ),
            'Line counter', self )
        self.connect( self.lineCounterButton, SIGNAL( 'triggered()' ),
                      self.onLineCounter )

        # Zoom buttons
        zoomInButton = QAction( PixmapCache().getIcon( 'zoomin.png' ),
                                'Zoom in (Ctrl+=)', self )
        self.connect( zoomInButton, SIGNAL( 'triggered()' ), self.onZoomIn )

        zoomOutButton = QAction( PixmapCache().getIcon( 'zoomout.png' ),
                                'Zoom out (Ctrl+-)', self )
        self.connect( zoomOutButton, SIGNAL( 'triggered()' ), self.onZoomOut )

        zoomResetButton = QAction( PixmapCache().getIcon( 'zoomreset.png' ),
                                   'Zoom reset (Ctrl+0)', self )
        self.connect( zoomResetButton, SIGNAL( 'triggered()' ),
                      self.onZoomReset )

        fixedSpacer = QWidget()
        fixedSpacer.setFixedHeight( 16 )

        # The toolbar
        toolbar = QToolBar( self )
        toolbar.setOrientation( Qt.Vertical )
        toolbar.setMovable( False )
        toolbar.setAllowedAreas( Qt.RightToolBarArea )
        toolbar.setIconSize( QSize( 16, 16 ) )
        toolbar.setFixedWidth( 28 )
        toolbar.setContentsMargins( 0, 0, 0, 0 )

        toolbar.addAction( printPreviewButton )
        toolbar.addAction( printButton )
        toolbar.addWidget( spacer )
        toolbar.addAction( zoomInButton )
        toolbar.addAction( zoomOutButton )
        toolbar.addAction( zoomResetButton )
        toolbar.addWidget( fixedSpacer )
        toolbar.addAction( self.lineCounterButton )

        self.__importsBar = ImportListWidget( self.__viewer )
        self.__importsBar.hide()

        hLayout = QHBoxLayout()
        hLayout.setContentsMargins( 0, 0, 0, 0 )
        hLayout.setSpacing( 0 )
        hLayout.addWidget( self.__viewer )
        hLayout.addWidget( toolbar )

        self.setLayout( hLayout )
        return

    def updateStatus( self ):
        " Updates the toolbar buttons status "
        if self.__fileType == UnknownFileType:
            self.__fileType = self.getFileType()
        isPythonFile = self.__fileType in [ PythonFileType, Python3FileType ]
        self.lineCounterButton.setEnabled( isPythonFile )
        return

    def onZoomReset( self ):
        " Triggered when the zoom reset button is pressed "
        if self.__viewer.zoom != 0:
            self.emit( SIGNAL( 'TextEditorZoom' ), 0 )
        return True

    def onZoomIn( self ):
        " Triggered when the zoom in button is pressed "
        if self.__viewer.zoom < 20:
            self.emit( SIGNAL( 'TextEditorZoom' ), self.__viewer.zoom + 1 )
        return True

    def onZoomOut( self ):
        " Triggered when the zoom out button is pressed "
        if self.__viewer.zoom > -10:
            self.emit( SIGNAL( 'TextEditorZoom' ), self.__viewer.zoom - 1 )
        return True

    def __onPrint( self ):
        " Triggered when the print button is pressed "
        pass

    def __onPrintPreview( self ):
        " triggered when the print preview button is pressed "
        pass

    def onLineCounter( self ):
        " Triggered when line counter button is clicked "
        LineCounterDialog( None, self.__viewer ).exec_()
        return

    def setFocus( self ):
        " Overridden setFocus "
        self.__viewer.setFocus()
        return

    def onOpenImport( self ):
        " Triggered when Ctrl+I is received "
        if self.__fileType not in [ PythonFileType, Python3FileType ]:
            return True

        # Python file, we may continue
        importLine, lineNo = isImportLine( self.__viewer )
        basePath = os.path.dirname( self.__fileName )

        if importLine:
            lineImports, importWhat = getImportsInLine( self.__viewer.text(),
                                                        lineNo + 1 )
            currentWord = str( self.__viewer.getCurrentWord( "." ) )
            if currentWord in lineImports:
                # The cursor is on some import
                path = resolveImport( basePath, currentWord )
                if path != '':
                    GlobalData().mainWindow.openFile( path, -1 )
                    return True
                GlobalData().mainWindow.showStatusBarMessage(
                        "The import '" + currentWord + "' is not resolved." )
                return True
            # We are not on a certain import.
            # Check if it is a line with exactly one import
            if len( lineImports ) == 1:
                path = resolveImport( basePath, lineImports[ 0 ] )
                if path == '':
                    GlobalData().mainWindow.showStatusBarMessage(
                        "The import '" + lineImports[ 0 ] +
                        "' is not resolved." )
                    return True
                # The import is resolved. Check where we are.
                if currentWord in importWhat:
                    # We are on a certain imported name in a resolved import
                    # So, jump to the definition line
                    line = getImportedNameDefinitionLine( path, currentWord )
                    GlobalData().mainWindow.openFile( path, line )
                    return True
                GlobalData().mainWindow.openFile( path, -1 )
                return True

            # Take all the imports in the line and resolve them.
            self.__onImportList( basePath, lineImports )
            return True

        # Here: the cursor is not on the import line. Take all the file imports
        # and resolve them
        fileImports = getImportsList( self.__viewer.text() )
        if not fileImports:
            GlobalData().mainWindow.showStatusBarMessage(
                                            "There are no imports" )
            return True
        if len( fileImports ) == 1:
            path = resolveImport( basePath, fileImports[ 0 ] )
            if path == '':
                GlobalData().mainWindow.showStatusBarMessage(
                    "The import '" + fileImports[ 0 ] + "' is not resolved." )
                return True
            GlobalData().mainWindow.openFile( path, -1 )
            return True

        self.__onImportList( basePath, fileImports )
        return True

    def __onImportList( self, basePath, imports ):
        " Works with a list of imports "

        # It has already been checked that the file is a Python one
        resolvedList = resolveImports( basePath, imports )
        if not resolvedList:
            GlobalData().mainWindow.showStatusBarMessage(
                                            "No imports are resolved" )
            return

        # Display the import selection widget
        self.__importsBar.showResolvedList( resolvedList )
        return

    def resizeEvent( self, event ):
        " Resizes the import selection dialogue if necessary "
        QWidget.resizeEvent( self, event )
        self.resizeBars()
        return

    def resizeBars( self ):
        " Resize the bars if they are shown "
        if not self.__importsBar.isHidden():
            self.__importsBar.resize()
        self.__viewer.resizeCalltip()
        return

    def onPylint( self ):
        return True
    def onPymetrics( self ):
        return True
    def onRunScript( self, action = False ):
        return True
    def onRunScriptSettings( self ):
        return True
    def onProfileScript( self, action = False ):
        return True
    def onProfileScriptSettings( self ):
        return True
    def onImportDgm( self, action = None ):
        return True
    def onImportDgmTuned( self ):
        return True
    def shouldAcceptFocus( self ):
        return True


    def setAnnotatedContent( self, shortName, text,
                                   lineRevisions, revisionInfo ):
        " Sets the content "
        self.setShortName( shortName )
        self.__viewer.setAnnotatedContent( shortName, text,
                                           lineRevisions, revisionInfo )
        return

    def writeFile( self, fileName ):
        " Writes the text to a file "
        return self.__viewer.writeFile( fileName )

    def updateModificationTime( self, fileName ):
        return

    # Mandatory interface part is below

    def getEditor( self ):
        " Provides the editor widget "
        return self.__viewer

    def isModified( self ):
        " Tells if the file is modified "
        return False

    def getRWMode( self ):
        " Tells if the file is read only "
        return "RO"

    def getFileType( self ):
        " Provides the file type "
        if self.__fileType == UnknownFileType:
            if self.__shortName:
                self.__fileType = detectFileType( self.__shortName )
        return self.__fileType

    def setFileType( self, typeToSet ):
        """ Sets the file type explicitly.
            It needs e.g. for .cgi files which can change its type """
        self.__fileType = typeToSet
        return

    def getType( self ):
        " Tells the widget type "
        return MainWindowTabWidgetBase.VCSAnnotateViewer

    def getLanguage( self ):
        " Tells the content language "
        if self.__fileType == UnknownFileType:
            self.__fileType = self.getFileType()
        if self.__fileType != UnknownFileType:
            return getFileLanguage( self.__fileType )
        return self.__viewer.getLanguage()

    def getFileName( self ):
        " Tells what file name of the widget content "
        return "N/A"

    def setFileName( self, name ):
        " Sets the file name "
        raise Exception( "Setting a file name for annotate results is not applicable" )

    def getEol( self ):
        " Tells the EOL style "
        return self.__viewer.getEolIndicator()

    def getLine( self ):
        " Tells the cursor line "
        line, pos = self.__viewer.getCursorPosition()
        return int( line )

    def getPos( self ):
        " Tells the cursor column "
        line, pos = self.__viewer.getCursorPosition()
        return int( pos )

    def getEncoding( self ):
        " Tells the content encoding "
        return self.__viewer.encoding

    def setEncoding( self, newEncoding ):
        " Sets the new editor encoding "
        self.__viewer.setEncoding( newEncoding )
        return

    def getShortName( self ):
        " Tells the display name "
        return self.__shortName

    def setShortName( self, name ):
        " Sets the display name "
        self.__shortName = name
        self.__fileType = detectFileType( name )
        return
