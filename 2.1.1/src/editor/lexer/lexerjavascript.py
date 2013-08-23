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
# $Id: lexerjavascript.py 18 2011-01-16 21:24:10Z sergey.satskiy@gmail.com $
#

#
# The file was taken from eric 4.4.3 and adopted for codimension.
# Original copyright:
# Copyright (c) 2007 - 2010 Detlev Offenbach <detlev@die-offenbachs.de>
#



""" JavaScript lexer implementation """

from PyQt4.Qsci     import QsciLexerJavaScript
from PyQt4.QtCore   import QString
from lexer          import Lexer


class LexerJavaScript( QsciLexerJavaScript, Lexer ):
    """ Adds lexer dependant methods to the QScintilla's version """

    def __init__( self, parent = None ):

        QsciLexerJavaScript.__init__( self, parent )
        Lexer.__init__( self )

        self.commentString = QString( "//" )
        self.streamCommentString = { 'start' : QString( '/* ' ),
                                     'end'   : QString( ' */' ) }
        self.boxCommentString = { 'start'  : QString( '/* ' ),
                                  'middle' : QString( ' * ' ),
                                  'end'    : QString( ' */' ) }
        return

    def initProperties( self ):
        """ Initializes the lexer properties """

        self.setFoldComments( 1 )
        self.setFoldPreprocessor( 0 )
        self.setFoldAtElse( 0 )

        indentStyle = 0
        # indentStyle |= QsciScintilla.AiOpening
        # indentStyle |= QsciScintilla.AiClosing
        self.setAutoIndentStyle( indentStyle )

        self.setFoldCompact( 1 )
        return

    def isCommentStyle( self, style ):
        """ Checks if a style is a comment one """

        return style in [ QsciLexerJavaScript.Comment,
                          QsciLexerJavaScript.CommentDoc,
                          QsciLexerJavaScript.CommentLine,
                          QsciLexerJavaScript.CommentLineDoc ]

    def isStringStyle( self, style ):
        """ Checks if a style is a string one """

        return style in [ QsciLexerJavaScript.DoubleQuotedString,
                          QsciLexerJavaScript.SingleQuotedString,
                          QsciLexerJavaScript.UnclosedString,
                          QsciLexerJavaScript.VerbatimString ]

