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

" Find in files viewer implementation "

from PyQt4.QtCore       import Qt, SIGNAL, QSize, QTimer, QStringList
from PyQt4.QtGui        import QToolBar, QCursor, QBrush, \
                               QHBoxLayout, QWidget, QAction, \
                               QSizePolicy, QLabel, \
                               QSizePolicy, QFrame, \
                               QTreeWidget, QApplication, \
                               QTreeWidgetItem, QHeaderView, QToolTip, \
                               QPalette, QColor, QFont, QVBoxLayout
from utils.pixmapcache  import PixmapCache
from utils.globals      import GlobalData
from itemdelegates      import NoOutlineHeightDelegate
from utils.fileutils    import getFileIcon, detectFileType


cellHeight = 20     # default
screenWidth = 600   # default

class Tooltip( QFrame ):
    " Custom tooltip "

    def __init__( self ):
        QFrame.__init__( self )

        # Avoid the border around the window
        self.setWindowFlags( Qt.SplashScreen )

        # Make the frame nice looking
        self.setFrameShape( QFrame.StyledPanel )
        self.setLineWidth( 2 )

        self.info = None
        self.location = None
        self.__createLayout()

        # The item the tooltip is for
        self.item = None

        # The timer which shows the tooltip. The timer is controlled from
        # outside of the class.
        self.tooltipTimer = QTimer( self )
        self.tooltipTimer.setSingleShot( True )
        self.connect( self.tooltipTimer, SIGNAL( 'timeout()' ),
                      self.__onTimer )

        self.startPosition = None
        return

    def __createLayout( self ):
        " Creates the tooltip layout "
        verticalLayout = QVBoxLayout( self )
        font = QFont( "Monospace", 12 )
        self.info = QLabel()
        self.info.setAutoFillBackground( True )
        self.info.setFont( font )
        self.info.setFrameShape( QFrame.StyledPanel )
        verticalLayout.addWidget( self.info )
        verticalLayout.setMargin( 0 )
        self.location = QLabel()
        verticalLayout.addWidget( self.location )
        return

    def setText( self, text ):
        " Sets the tooltip text "
        self.info.setText( text )
        return

    def setLocation( self, text ):
        " Sets the file name and line at the bottom "
        self.location.setText( text )
        return

    def setModified( self, status ):
        " Sets the required tooltip background "
        palette = self.info.palette()
        if status:
            # Reddish
            palette.setColor( QPalette.Background, QColor( 255, 227, 227 ) )
        else:
            # Blueish
            palette.setColor( QPalette.Background, QColor( 224, 236, 255 ) )
        self.info.setPalette( palette )
        return

    def setItem( self, item ):
        " Sets the item the tooltip is shown for "
        self.item = item
        return

    def __getTooltipPos( self ):
        " Calculates the tooltip position - above the row "
        pos = QCursor.pos()
        if pos.x() + self.sizeHint().width() >= screenWidth:
            pos.setX( screenWidth - self.sizeHint().width() - 2 )
        pos.setY( pos.y() - cellHeight - 1 - self.sizeHint().height() )
        return pos

    def __onTimer( self ):
        " Triggered by the show tooltip timer "
        currentPos = QCursor.pos()
        if abs( currentPos.x() - self.startPosition.x() ) <= 3 and \
           abs( currentPos.y() - self.startPosition.y() ) <= 3:
            # No movement since last time, show the tooltip
            self.show()
            return

        # There item has not been changed, but the position within it was
        # So restart the timer, but for shorter
        self.startPosition = currentPos
        self.tooltipTimer.start( 250 )
        return

    def startShowTimer( self ):
        " Memorizes the cursor position and starts the timer "
        self.tooltipTimer.stop()
        self.startPosition = QCursor.pos()
        self.tooltipTimer.start( 500 )  # 0.5 sec
        return

    def show( self ):
        " Shows the tooltip at the proper position "
        QToolTip.hideText()
        QApplication.processEvents()
        self.move( self.__getTooltipPos() )
        QFrame.show( self )
        return


# Global tooltip instance
searchTooltip = Tooltip()

def hideSearchTooltip():
    " Hides both the standard and search tooltips "
    searchTooltip.tooltipTimer.stop()
    searchTooltip.hide()
    QToolTip.hideText()
    QApplication.processEvents()
    return


class MatchTableItem( QTreeWidgetItem ):
    " Match item "

    def __init__( self, items, tooltip ):
        QTreeWidgetItem.__init__( self, items )
        self.__intColumn = 0
        self.__tooltip = tooltip
        self.__fileModified = False

        # Memorize the screen width
        global screenWidth
        screenSize = GlobalData().application.desktop().screenGeometry()
        screenWidth = screenSize.width()
        return

    def __lt__( self, other ):
        " Integer or string custom sorting "
        sortColumn = self.treeWidget().sortColumn()
        if sortColumn == self.__intColumn:
            return int( self.text( sortColumn ) ) < \
                   int( other.text( sortColumn ) )
        return self.text( sortColumn ) < other.text( sortColumn )

    def setModified( self, status ):
        " Sets the modified flag "
        self.__fileModified = status
        return

    def __updateTooltipProperties( self ):
        " Updates all the tooltip properties "
        searchTooltip.setItem( self )
        searchTooltip.setModified( self.__fileModified )
        searchTooltip.setText( self.__tooltip )

        fileName = str( self.parent().data( 0, Qt.DisplayRole ).toString() )
        lineNumber = str( self.data( 0, Qt.DisplayRole ).toString() )
        searchTooltip.setLocation( " " + fileName + ":" + lineNumber )
        return

    def itemEntered( self ):
        " Triggered when mouse cursor entered the match "
        if self.__tooltip == "":
            return

        if searchTooltip.isVisible():
            hideSearchTooltip()
            self.__updateTooltipProperties()
            searchTooltip.show()
        else:
            searchTooltip.startShowTimer()
            self.__updateTooltipProperties()
        return


class MatchTableFileItem( QTreeWidgetItem ):
    " Match file item "

    def __init__( self, items, uuid ):
        QTreeWidgetItem.__init__( self, items )
        self.uuid = uuid
        return


class FindResultsTreeWidget( QTreeWidget ):
    """ Tree widget derivation to intercept the fact that the mouse cursor
        left the widget """

    def __init__( self, parent = None ):
        QTreeWidget.__init__( self, parent )
        return

    def leaveEvent( self, event ):
        " Triggered when the cursor leaves the find results tree "
        hideSearchTooltip()
        QTreeWidget.leaveEvent( self, event )
        return

    def onBufferModified( self, fileName, uuid ):
        " Triggered when a buffer is modified "
        index = self.topLevelItemCount() - 1
        while index >= 0:
            item = self.topLevelItem( index )
            if item.uuid == uuid or \
               str( item.data( 0, Qt.DisplayRole ).toString() ) == fileName:
                # The buffer for this item has been modified
                brush = QBrush( QColor( 255, 227, 227 ) )
                item.setBackground( 0, brush )
                item.setBackground( 1, brush )
                childIndex = item.childCount() - 1
                while childIndex >= 0:
                    childItem = item.child( childIndex )
                    childItem.setModified( True )
                    if searchTooltip.item == childItem:
                        searchTooltip.setModified( True )
                    childIndex -= 1
            index -= 1
        return



class FindInFilesViewer( QWidget ):
    " Find in files viewer tab widget "

    lastEntered = None

    def __init__( self, parent = None ):
        QWidget.__init__( self, parent )

        self.__reportRegexp = None
        self.__reportResults = []
        self.__reportShown = False
        self.__bufferChangeconnected = False

        # Prepare members for reuse
        self.__noneLabel = QLabel( "\nNo results available" )

        self.__noneLabel.setFrameShape( QFrame.StyledPanel )
        self.__noneLabel.setAlignment( Qt.AlignHCenter )
        self.__headerFont = self.__noneLabel.font()
        self.__headerFont.setPointSize( self.__headerFont.pointSize() + 4 )
        self.__noneLabel.setFont( self.__headerFont )

        self.__createLayout( parent )

        self.__updateButtonsStatus()
        return

    def __createLayout( self, parent ):
        " Creates the toolbar and layout "

        # Buttons
        self.printButton = QAction( PixmapCache().getIcon( 'printer.png' ),
                                    'Print', self )
        #printButton.setShortcut( 'Ctrl+' )
        self.connect( self.printButton, SIGNAL( 'triggered()' ),
                      self.__onPrint )

        self.printPreviewButton = QAction( \
                PixmapCache().getIcon( 'printpreview.png' ),
                'Print preview', self )
        #printPreviewButton.setShortcut( 'Ctrl+' )
        self.connect( self.printPreviewButton, SIGNAL( 'triggered()' ),
                      self.__onPrintPreview )

        spacer = QWidget()
        spacer.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Expanding )

        self.clearButton = QAction( \
            PixmapCache().getIcon( 'trash.png' ),
            'Clear', self )
        self.connect( self.clearButton, SIGNAL( 'triggered()' ),
                      self.__clear )

        # The toolbar
        toolbar = QToolBar( self )
        toolbar.setOrientation( Qt.Vertical )
        toolbar.setMovable( False )
        toolbar.setAllowedAreas( Qt.RightToolBarArea )
        toolbar.setIconSize( QSize( 16, 16 ) )
        toolbar.setFixedWidth( 28 )
        toolbar.setContentsMargins( 0, 0, 0, 0 )

        toolbar.addAction( self.printPreviewButton )
        toolbar.addAction( self.printButton )
        toolbar.addWidget( spacer )
        toolbar.addAction( self.clearButton )

        self.__resultsTree = FindResultsTreeWidget()
        self.__resultsTree.setAlternatingRowColors( True )
        self.__resultsTree.setRootIsDecorated( True )
        self.__resultsTree.setItemsExpandable( True )
        self.__resultsTree.setUniformRowHeights( True )
        self.__resultsTree.setItemDelegate( NoOutlineHeightDelegate( 4 ) )
        headerLabels = QStringList() << "File name / line" << "Text"
        self.__resultsTree.setHeaderLabels( headerLabels )
        self.connect( self.__resultsTree,
                      SIGNAL( "itemActivated(QTreeWidgetItem *, int)" ),
                      self.__resultActivated )
        self.__resultsTree.setMouseTracking( True )
        self.connect( self.__resultsTree,
                      SIGNAL( "itemEntered(QTreeWidgetItem *, int)" ),
                      self.__itemEntered )
        self.__resultsTree.hide()

        self.__hLayout = QHBoxLayout()
        self.__hLayout.setContentsMargins( 0, 0, 0, 0 )
        self.__hLayout.setSpacing( 0 )
        self.__hLayout.addWidget( toolbar )
        self.__hLayout.addWidget( self.__noneLabel )
        self.__hLayout.addWidget( self.__resultsTree )

        self.setLayout( self.__hLayout )
        return

    def __updateButtonsStatus( self ):
        " Updates the buttons status "
        self.printButton.setEnabled( self.__reportShown )
        self.printPreviewButton.setEnabled( self.__reportShown )
        self.clearButton.setEnabled( self.__reportShown )
        return

    def __onPrint( self ):
        " Triggered when the print button is pressed "
        pass

    def __onPrintPreview( self ):
        " triggered when the print preview button is pressed "
        pass

    def setFocus( self ):
        " Overridden setFocus "
        self.__hLayout.setFocus()
        return

    def __clear( self ):
        " Clears the content of the vertical layout "
        if not self.__reportShown:
            return

        self.__resultsTree.clear()
        self.__resultsTree.hide()
        self.__noneLabel.show()

        self.__reportRegexp = None
        self.__reportResults = []
        self.__reportShown = False
        self.__updateButtonsStatus()
        return

    def showReport( self, regexp, results ):
        " Shows the find in files results "
        self.__clear()
        self.__noneLabel.hide()

        self.__reportRegexp = regexp
        self.__reportResults = results

        # Add the complete information
        for item in results:
            if len( item.matches ) == 1:
                matchText = " (1 match)"
            else:
                matchText = " (" + str( len( item.matches ) ) + " matches)"
            columns = QStringList() << item.fileName << matchText
            fileItem = MatchTableFileItem( columns, item.bufferUUID )
            fileItem.setIcon( 0,
                              getFileIcon( detectFileType( item.fileName ) ) )
            if item.tooltip != "":
                fileItem.setToolTip( 0, item.tooltip )
            self.__resultsTree.addTopLevelItem( fileItem )

            # Matches
            for match in item.matches:
                columns = QStringList() << str( match.line ) << match.text
                matchItem = MatchTableItem( columns, match.tooltip )
                fileItem.addChild( matchItem )
            fileItem.setExpanded( True )

        # Resizing the table
        self.__resultsTree.header().resizeSections( \
                                            QHeaderView.ResizeToContents )

        # Show the complete information
        self.__resultsTree.show()

        self.__reportShown = True
        self.__updateButtonsStatus()

        # Connect the buffer change signal if not connected yet
        if not self.__bufferChangeconnected:
            self.__bufferChangeconnected = True
            mainWindow = GlobalData().mainWindow
            editorsManager = mainWindow.editorsManagerWidget.editorsManager
            self.connect( editorsManager, SIGNAL( 'bufferModified' ),
                          self.__resultsTree.onBufferModified )
        return

    def __resultActivated( self, item, column ):
        " Handles the double click (or Enter) on a match "
        if type( item ) != MatchTableItem:
            if item.isExpanded():
                print "Expanding. It was : " + str( item.isExpanded() )
#                print "item expanded"
#                item.setExpanded( False )
                self.__resultsTree.collapseItem( item )
                print "Now it is : " + str( item.isExpanded() )
            else:
#                print "item collapsed"
                print "Collapsing. It was : " + str( item.isExpanded() )
#                item.setExpanded( True )
                self.__resultsTree.expandItem( item )
                print "Now it is : " + str( item.isExpanded() )
            return

        fileName = str( item.parent().data( 0, Qt.DisplayRole ).toString() )
        lineNumber = int( item.data( 0, Qt.DisplayRole ).toString() )
        GlobalData().mainWindow.openFile( fileName, lineNumber )
        hideSearchTooltip()
        return

    def __itemEntered( self, item, column ):
        " Triggered when the mouse cursor entered a row "

        if type( item ) != MatchTableItem:
            self.lastEntered = item
            hideSearchTooltip()
            return

        # Memorize the row height for proper tooltip displaying later
        global cellHeight
        cellHeight = self.__resultsTree.visualItemRect( item ).height()

        if self.lastEntered != item:
            item.itemEntered()
            self.lastEntered = item
        return

