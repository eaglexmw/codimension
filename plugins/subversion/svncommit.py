#
# -*- coding: utf-8 -*-
#
# codimension - graphics python two-way code editor and analyzer
# Copyright (C) 2010  Sergey Satskiy sergey.satskiy@gmail.com
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

""" Does SVN commit """

import os.path
import pysvn
import logging
from svncommitdlg import SVNPluginCommitDialog
from svnindicators import ( IND_ADDED, IND_DELETED, IND_MERGED,
                            IND_MODIFIED_LR, IND_MODIFIED_L,
                            IND_REPLACED, IND_CONFLICTED, IND_IGNORED )
from PyQt4.QtGui import QDialog, QApplication, QCursor
from PyQt4.QtCore import Qt


COMMIT_ALLOW_STATUSES = [ IND_ADDED, IND_DELETED, IND_MERGED, IND_MODIFIED_LR,
                          IND_MODIFIED_L, IND_REPLACED, IND_CONFLICTED ]
IGNORE_STATUSES = [ IND_IGNORED ]


def doSVNCommit( plugin, client, path ):
    " Performs SVN commit "

    # The path could be a single file (buffer or project browser) or
    # a directory

    if path.endswith( os.path.sep ):
        # This is a directory. Path lists should be built.
        statuses = plugin.getLocalStatus( path, pysvn.depth.infinity )
        if type( statuses ) != list:
            logging.error( "Error checking local SVN statuses for " + path )
            return

        pathsToCommit = []
        pathsToIgnore = []
        for item in statuses:
            if item[ 1 ] in COMMIT_ALLOW_STATUSES:
                pathsToCommit.append( item )
            elif item[ 1 ] in IGNORE_STATUSES + [ plugin.NOT_UNDER_VCS ]:
                pathsToIgnore.append( item )

        if not pathsToCommit:
            logging.info( "No paths to commit for " + path )
            return
    else:
        # This is a single file
        status = plugin.getLocalStatus( path )
        if status not in COMMIT_ALLOW_STATUSES:
            logging.error( "Cannot commit " + path +
                           " due to unexpected SVN status" )
            return
        pathsToCommit = [ (path, status), ]
        pathsToIgnore = []

    dlg = SVNPluginCommitDialog( pathsToCommit, pathsToIgnore )
    res = dlg.exec_()

    if res == QDialog.Accepted:
        if len( dlg.commitPaths ) == 0:
            return
        dlg.commitPaths.sort()

        QApplication.setOverrideCursor( QCursor( Qt.WaitCursor ) )
        try:
            message = "Committing:"
            for path in dlg.commitPaths:
                message += "\n    " + path
            logging.info( message )

            def getLogMessage( msg = dlg.commitMessage ):
                return True, msg
            client.callback_get_log_message = getLogMessage

            revision = client.checkin( dlg.commitPaths,
                                       log_message = dlg.commitMessage,
                                       recurse = False )
            logging.info( "Committed revision " + str( revision.number ) )
            for path in dlg.commitPaths:
                plugin.notifyPathChanged( path )
        except pysvn.ClientError, exc:
            message = exc.args[ 0 ]
            logging.error( message )
        except Exception, exc:
            logging.error( str( exc ) )
        except:
            logging.error( "Unknown error" )
        QApplication.restoreOverrideCursor()

    return

