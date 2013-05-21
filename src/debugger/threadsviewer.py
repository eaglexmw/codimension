#
# -*- coding: utf-8 -*-
#
# codimension - graphics python two-way code editor and analyzer
# Copyright (C) 2010-2012  Sergey Satskiy <sergey.satskiy@gmail.com>
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

" Thread viewer "


from PyQt4.QtCore import Qt, SIGNAL, QStringList
from PyQt4.QtGui import ( QFrame, QTreeWidget, QToolButton, QTreeWidgetItem,
                          QHeaderView, QVBoxLayout, QLabel, QWidget,
                          QAbstractItemView, QSizePolicy, QSpacerItem,
                          QHBoxLayout, QPalette )
from ui.itemdelegates import NoOutlineHeightDelegate
from utils.pixmapcache import PixmapCache
from utils.settings import Settings


class ThreadItem( QTreeWidgetItem ):
    " Single thread item data structure "

    def __init__( self, tid, name, state ):
        QTreeWidgetItem.__init__( self,
                QStringList() << "" << name << state << str( tid ) )

        self.__isCurrent = False
        self.__setTooltip()
        return

    def __setTooltip( self ):
        " Sets the tooltip "
        tooltip = "Current: " + str( self.__isCurrent ) + "\n" \
                  "Name: " + self.getName() + "\n" \
                  "State: " + self.getState() + "\n" \
                  "TID: " + str( self.getTID() )
        for index in xrange( 4 ):
            self.setToolTip( index, tooltip )
        return

    def setCurrent( self, value ):
        """ Mark the current thread with an icon if so """
        if self.__isCurrent == value:
            return

        self.__isCurrent = value
        if value:
            self.setIcon( 0, PixmapCache().getIcon( 'currentthread.png' ) )
        else:
            self.setIcon( 0, None )
        self.__setTooltip()
        return

    def getTID( self ):
        """ Provides the thread ID """
        return int( self.text( 3 ) )

    def getName( self ):
        " Provides the thread name "
        return str( self.text( 1 ) )

    def getState( self ):
        " Provides the thread state "
        return str( self.text( 2 ) )

    def isCurrent( self ):
        " True if the project is current "
        return self.__isCurrent



class ThreadsViewer( QWidget ):
    " Implements the threads viewer for a debugger "

    def __init__( self, debugger, parent = None ):
        QWidget.__init__( self, parent )

        self.__debugger = debugger
        self.__createLayout()

        if Settings().showThreadViewer == False:
            self.__onShowHide( True )
        return

    def __createLayout( self ):
        " Creates the widget layout "

        verticalLayout = QVBoxLayout( self )
        verticalLayout.setContentsMargins( 0, 0, 0, 0 )
        verticalLayout.setSpacing( 0 )

        self.headerFrame = QFrame()
        self.headerFrame.setFrameStyle( QFrame.StyledPanel )
        self.headerFrame.setAutoFillBackground( True )
        headerPalette = self.headerFrame.palette()
        headerBackground = headerPalette.color( QPalette.Background )
        headerBackground.setRgb( min( headerBackground.red() + 30, 255 ),
                                 min( headerBackground.green() + 30, 255 ),
                                 min( headerBackground.blue() + 30, 255 ) )
        headerPalette.setColor( QPalette.Background, headerBackground )
        self.headerFrame.setPalette( headerPalette )
        self.headerFrame.setFixedHeight( 24 )

        self.__threadsLabel = QLabel( "Threads" )

        expandingSpacer = QSpacerItem( 10, 10, QSizePolicy.Expanding )
        fixedSpacer = QSpacerItem( 3, 3 )

        self.__showHideButton = QToolButton()
        self.__showHideButton.setAutoRaise( True )
        self.__showHideButton.setIcon( PixmapCache().getIcon( 'less.png' ) )
        self.__showHideButton.setFixedSize( 20, 20 )
        self.__showHideButton.setToolTip( "Hide threads list" )
        self.__showHideButton.setFocusPolicy( Qt.NoFocus )
        self.connect( self.__showHideButton, SIGNAL( 'clicked()' ),
                      self.__onShowHide )

        headerLayout = QHBoxLayout()
        headerLayout.setContentsMargins( 0, 0, 0, 0 )
        headerLayout.addSpacerItem( fixedSpacer )
        headerLayout.addWidget( self.__threadsLabel )
        headerLayout.addSpacerItem( expandingSpacer )
        headerLayout.addWidget( self.__showHideButton )
        self.headerFrame.setLayout( headerLayout )

        self.__threadsList = QTreeWidget()
        self.__threadsList.setSortingEnabled( False )
        # I might not need that because of two reasons:
        # - the window has no focus
        # - the window has custom current indicator
        # self.__threadsList.setAlternatingRowColors( True )
        self.__threadsList.setRootIsDecorated( False )
        self.__threadsList.setItemsExpandable( False )
        self.__threadsList.setUniformRowHeights( True )
        self.__threadsList.setSelectionMode( QAbstractItemView.NoSelection )
        self.__threadsList.setSelectionBehavior( QAbstractItemView.SelectRows )
        self.__threadsList.setItemDelegate( NoOutlineHeightDelegate( 4 ) )
        self.__threadsList.setFocusPolicy( Qt.NoFocus )

        self.connect( self.__threadsList,
                      SIGNAL( "itemClicked(QTreeWidgetItem*,int)" ),
                      self.__onThreadClicked )

        headerLabels = QStringList() << "" << "Name" << "State" << "TID"
        self.__threadsList.setHeaderLabels( headerLabels )

        verticalLayout.addWidget( self.headerFrame )
        verticalLayout.addWidget( self.__threadsList )
        return

    def __onShowHide( self, startup = False ):
        " Triggered when show/hide button is clicked "
        if startup or self.__threadsList.isVisible():
            self.__threadsList.setVisible( False )
            self.__showHideButton.setIcon( PixmapCache().getIcon( 'more.png' ) )
            self.__showHideButton.setToolTip( "Show threads list" )

            self.__minH = self.minimumHeight()
            self.__maxH = self.maximumHeight()

            self.setMinimumHeight( self.headerFrame.height() )
            self.setMaximumHeight( self.headerFrame.height() )

            Settings().showThreadViewer = False
        else:
            self.__threadsList.setVisible( True )
            self.__showHideButton.setIcon( PixmapCache().getIcon( 'less.png' ) )
            self.__showHideButton.setToolTip( "Hide threads list" )

            self.setMinimumHeight( self.__minH )
            self.setMaximumHeight( self.__maxH )

            Settings().showThreadViewer = True
        return

    def __resizeColumns( self ):
        " Resize the files list columns "
        self.__threadsList.header().setStretchLastSection( True )
        self.__threadsList.header().resizeSections(
                                    QHeaderView.ResizeToContents )
        self.__threadsList.header().resizeSection( 0, 22 )
        self.__threadsList.header().setResizeMode( 0, QHeaderView.Fixed )
        return

    def clear( self ):
        " Clears the content "
        self.__threadsList.clear()
        self.__threadsLabel.setText( "Threads" )
        return

    def populate( self, currentThreadID, threadList ):
        " Populates the thread list from the client "
        self.clear()
        for thread in threadList:
            if thread[ 'broken' ]:
                state = "Waiting at breakpoint"
            else:
                state = "Running"
            item = ThreadItem( thread[ 'id' ], thread[ 'name' ], state )
            if thread[ 'id' ] == currentThreadID:
                item.setCurrent( True )
            self.__threadsList.addTopLevelItem( item )

        self.__resizeColumns()
        self.__threadsLabel.setText( "Threads (total: " +
                                     str( len( threadList ) ) + ")" )
        return

    def switchControl( self, isInIDE ):
        " Switches the UI depending where the control flow is "
        self.__threadsList.setEnabled( isInIDE )
        return

    def __onThreadClicked( self, item, column ):
        " Triggered when a thread is clicked "
        if item.isCurrent():
            return

        for index in xrange( self.__threadsList.topLevelItemCount() ):
            listItem = self.__threadsList.topLevelItem( index )
            if listItem.isCurrent():
                listItem.setCurrent( False )
                break
        item.setCurrent( True )

        self.__debugger.remoteSetThread( item.getTID() )
        return

