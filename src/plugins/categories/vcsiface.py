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

" Version control system plugin interface "


from yapsy.IPlugin import IPlugin


class VersionControlSystemInterface( IPlugin ):
    """ Version control system plugin interface """

    def __init__( self ):
        """ The plugin class is instantiated with no arguments """
        IPlugin.__init__( self )
        return

    def getInterfaceVersion( self ):
        """ Do not override this method. Codimension uses it
            to detect the protocol version conformance. """
        return "1.0.0"


    # Member functions below could or should be implemented by a plugin.
    # See docstrings for the detailed description.

    @staticmethod
    def isIDEVersionCompatible( ideVersion ):
        """ Codimension makes this call before activating a plugin.
            The passed ideVersion is a string representing
            the current IDE version.
            True should be returned if the plugin is compatible with the IDE.
        """
        raise Exception( "isIDEVersionCompatible() must be overridden" )

    @staticmethod
    def getVCSName():
        """ Should provide the specific version control name, e.g. SVN """
        raise Exception( "getVCSName() must be overridden" )

    def activate( self ):
        """ The plugin may override the method to do specific
            plugin activation handling.
            Note: if overriden do not forget to call the
                  base class activate() """
        IPlugin.activate( self )
        return

    def deactivate( self ):
        """ The plugin may override the method to do specific
            plugin deactivation handling.
            Note: if overriden do not forget to call the
                  base class deactivate() """
        IPlugin.deactivate( self )
        return

    def setEnvironment( self, ideSettings, ideGlobalData ):
        """ Codimension calls this method after the activate() call and
            before any other non-static methods.

            ideSettings - reference to the IDE Settings singleton
                          see codimension/src/utils/settings.py
            ideGlobalData - reference to the IDE global settings
                            see codimension/src/utils/globals.py

            No return value is expected
        """
        return

    def populateMainMenu( self, parentMenu ):
        raise Exception( "populateMainMenu() must be overridden" )

    def populateFileContextMenu( self, parentMenu ):
        raise Exception( "populateFileContextMenu() must be overridden" )

    def populateDirectoryContextMenu( self, parentMenu ):
        raise Exception( "populateDirectoryContextMenu() must be overridden" )

    def populateBufferContextMenu( self, parentMenu ):
        raise Exception( "populateBufferContextMenu() must be overridden" )

    def isUnderVCS( self, path ):
        """ 'path' is an absolute path to a directory or to a file.
            Return value must be True if the given path is under the
            revision control system type, or False otherwise. """
        raise Exception( "isUnderVCS() must be overridden" )

    def isChangedLocally( self, path, recursively = False ):
        raise Exception( "isChangedLocally() must be overridden" )

    def isChangedRemotely( self, path, recursively = False ):
        raise Exception( "isChangedRemotely() must be overridden" )

    def getInfo( self, path, recursively = False ):
        raise Exception( "getInfo() must be overridden" )

    def getRepositoryVersion( self, path, revision = None ):
        """ Should provide the content of the file at path from the VCS.
            If revision is not specified then it must be the latest version """
        raise Exception( "getRepositoryVersion() must be overridden" )

