#!/usr/bin/env python

"""
Styling for the MainWindow object.

Copyright (C) Sarah Mount, 2011.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from PyQt4.Qsci import QsciScintilla, QsciLexerPython, QsciStyle
from PyQt4 import Qt


__author__ = 'Sarah Mount <s.mount@wlv.ac.uk>'
__date__ = 'April 2011'


class StyleMixin(object):
    BREAK_MARKER_NUM = 1 # Marker for breakpoints.

    def setup_styling(self):
        # Default fonts and styles.
        self.font = Qt.QFont()
        self.font.setFamily('Courier')
        self.font.setFixedPitch(True)
        self.font.setPointSize(11)

        self.lint_font = Qt.QFont()
        self.lint_font.setFamily('Courier')
        self.lint_font.setFixedPitch(True)
        self.lint_font.setItalic(True)
        self.lint_font.setPointSize(9)

        # Styling for lint errors.
        self.info = QsciStyle(-1,
                               'Hilite style for lint info',
                               Qt.QColor('#222222'),
                               Qt.QColor('#FFFFFF'),
                               self.lint_font)
        self.warning = QsciStyle(-1,
                                  'Hilite style for lint warnings',
                                  Qt.QColor('#222222'),
                                  Qt.QColor('#FFFF44'),
                                  self.lint_font)
        self.error = QsciStyle(-1,
                                'Hilite style for lint errors',
                                Qt.QColor('#222222'),
                                Qt.QColor('#EE0000'),
                                self.lint_font)

    def setup_icons(self):
        """Add default icons (from the system theme, where possible) to actions.
        This is particularly useful for the toolbar.
        """
        # File menu.
        self.action_New_File.setIcon(Qt.QIcon.fromTheme('document-new'))
        self.action_Open_File.setIcon(Qt.QIcon.fromTheme('document-open'))
        self.action_Save_File.setIcon(Qt.QIcon.fromTheme('document-save'))
        self.action_Save_File_As.setIcon(Qt.QIcon.fromTheme('document-save-as'))
        self.action_Print_File.setIcon(Qt.QIcon.fromTheme('document-print'))
        self.action_Close_File.setIcon(Qt.QIcon.fromTheme('window-close'))
        self.action_Quit.setIcon(Qt.QIcon.fromTheme('application-exit'))
        # Edit menu.
        self.action_Undo_Edit.setIcon(Qt.QIcon.fromTheme('edit-undo'))
        self.action_Redo_Edit.setIcon(Qt.QIcon.fromTheme('edit-redo'))
        self.action_Cut_Edit.setIcon(Qt.QIcon.fromTheme('edit-cut'))
        self.action_Copy_Edit.setIcon(Qt.QIcon.fromTheme('edit-copy'))
        self.action_Paste_Edit.setIcon(Qt.QIcon.fromTheme('edit-paste'))
        self.action_Select_All_Edit.setIcon(Qt.QIcon.fromTheme('edit-select-all'))
        # Search menu.
        self.action_Find_Search.setIcon(Qt.QIcon.fromTheme('edit-find'))
        self.action_Find_Next_Search.setIcon(Qt.QIcon.fromTheme('edit-find'))
        self.action_Replace_Search.setIcon(Qt.QIcon.fromTheme('edit-find-replace'))
        self.action_Goto_Line_Search.setIcon(Qt.QIcon.fromTheme('go-jump'))
        # Source menu. 
        self.action_Indent_Selection_Source.setIcon(Qt.QIcon.fromTheme('format-indent-more'))
        self.action_Unindent_Selection_Source.setIcon(Qt.QIcon.fromTheme('format-indent-less'))
        # View menu.
        self.action_Zoom_In_View.setIcon(Qt.QIcon.fromTheme('zoom-in'))
        self.action_Zoom_Out_View.setIcon(Qt.QIcon.fromTheme('zoom-out'))
        # Run menu.
        self.action_Run_CSP_Code_Run.setIcon(Qt.QIcon.fromTheme('media-playback-start'))
        self.action_Run_Threaded_Code_Run.setIcon(Qt.QIcon.fromTheme('media-playback-start'))
        # Bijector menu.
        self.action_Convert_to_CSP_Bijector.setIcon(Qt.QIcon.fromTheme('go-first'))
        self.action_Convert_to_Threads_Bijector.setIcon(Qt.QIcon.fromTheme('go-last'))
        # Help menu.
        self.action_About_Help.setIcon(Qt.QIcon.fromTheme('help-about'))
        return
        
    def setup_editor(self, editor):
        """Set various properties of a QScintilla widget.
        """
        # Brace matching: enable for a brace immediately before or after
        # the current position
        editor.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        # Current line visible with special background color
        editor.setCaretLineVisible(True)
        editor.setCaretLineBackgroundColor(Qt.QColor("#ffe4e4"))
        # Make the cursor visible.
        editor.ensureCursorVisible()
        # Deal with indentation.
        editor.setAutoIndent(True)
        editor.setIndentationWidth(4)
        editor.setIndentationGuides(1)
        editor.setIndentationsUseTabs(0)
        editor.setAutoCompletionThreshold(2)
        editor.setBackspaceUnindents(True)
        # Deal with margins and breakpoint markers.
        editor.setMarginSensitivity(1, True)
        editor.connect(editor,
                       Qt.SIGNAL('marginClicked(int, int, Qt::KeyboardModifiers)'), self.on_margin_clicked)
        editor.markerDefine(QsciScintilla.RightArrow,
                            StyleMixin.BREAK_MARKER_NUM)
        editor.setMarkerBackgroundColor(Qt.QColor("#0099FF"),
                                        StyleMixin.BREAK_MARKER_NUM)
        editor.setMarkerForegroundColor(Qt.QColor("#000000"),
                                        StyleMixin.BREAK_MARKER_NUM)
        editor.setFont(self.font)
        editor.setMarginsFont(self.font)
        # Mark the 79th column.
        editor.setEdgeColumn(79)
        editor.setEdgeMode(1)        
        # Margin 0 is used for line numbers.
        fontmetrics = Qt.QFontMetrics(self.font)
        editor.setMarginsFont(self.font)
        editor.setMarginWidth(0, fontmetrics.width("00000") + 6)
        editor.setMarginLineNumbers(0, True)
        editor.setMarginsBackgroundColor(Qt.QColor("#cccccc"))
        # Set Python lexer and its fonts.
        lexer = QsciLexerPython()
        lexer.setDefaultFont(self.font)
        editor.setLexer(lexer)
        editor.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, 'Courier')
        return