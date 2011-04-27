#!/usr/bin/env python

"""
Bijective editor for python-csp / threaded Python code.

Current features:
 * Folding mode.
 * Word wrap.
 * Visible whitespace.
 * Code autocompletion (Ctrl+Space).

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

from bijector_main import Ui_MainWindow

import os
import syntax # Basic syntax highlighting where QScintilla would be overkill.

__author__ = 'Sarah Mount <s.mount@wlv.ac.uk>'
__date__ = 'April 2011'

# pylint: disable=W0231
# pylint: disable=W0613
# pylint: disable=W0511

# TODO: Find previous, Replace.
# TODO: Recent file list (use QSettings).
# TODO: Check that all files have been saved before closing the app.

class MainWindow(Qt.QMainWindow, Ui_MainWindow):
    """Creates the Main Window of the application using the main 
    window design in the gui.bijector_main module.
    """
    BREAK_MARKER_NUM = 1 # Marker for breakpoints.
    
    def __init__(self, parent=None):
        Qt.QMainWindow.__init__(self)
        self.setupUi(self)
        self.setup_icons()

        self.app_name = 'PyBijector'
        self.setWindowTitle(self.app_name)
        self.action_Close_File.setDisabled(True)
        # FIXME: Use Qt resources instead of static filenames.
        self.setWindowIcon(Qt.QIcon('images/pythoncsp-logo.png'))

        self.userdir = os.path.expanduser('~')
        self.filename = Qt.QString('')
        # Used in search / replace
        self.searchString = None

        # Default fonts and styles.
        self.font = Qt.QFont()
        self.font.setFamily('Courier')
        self.font.setFixedPitch(True)
        self.font.setPointSize(11)

        # Setup styling for editor panes.
        self.setup_editor(self.threadEdit)
        self.setup_editor(self.cspEdit)
        
        # Styling for lint errors.
        self.hilite = QsciStyle(-1, 'Hilite style for lint errors',
                                 Qt.QColor('#222222'), Qt.QColor('#FFFF44'),
                                 self.font)
        self.threadEdit.setAnnotationDisplay(2)
        self.cspEdit.setAnnotationDisplay(2)
        
        # By default, hide the console tabs.
        self.action_Toggle_Console_Window.setChecked(False)
        self.consoleTabs.hide()

        # Set checkable actions.
        self.action_Folding_Mode_Source.setChecked(True)
        self.toggle_folding_mode()
        self.action_Whitespace_Visible_Source.setChecked(True)
        self.toggle_whitespace_visible()
        self.action_Word_Wrap_Source.setChecked(True)
        self.toggle_word_wrap()
        
        # Apply basic syntax highlighting to consoles.
        self.highlight_thread = syntax.PythonHighlighter(self.threadConsole.document())
        self.highlight_csp = syntax.PythonHighlighter(self.cspConsole.document())

        # TEST TODO
        self.lint_error(1, 'flibble bar foo baz')
        
        # TODO Populate recent file list.
        
        # Shortcuts without menu items
        self.connect(Qt.QShortcut(Qt.QKeySequence("Ctrl+Space"), self), 
                     Qt.SIGNAL('activated()'),
                     self.autocomplete)

        # Start with the focus on the left hand editor.
        self.threadEdit.setFocus()
        return

    def get_editor(self):
        """Return the currently active editor.

        If either editor has focus, then that editor is active.
        If neither editor has focus, but one has been modified, then that
        is the currently active editor.
        If neither editor has focus and neither or both editors have been
        modified, then we (randomly) choose the editor on the left.
        """
        if self.threadEdit.hasFocus():
            return self.threadEdit
        elif self.cspEdit.hasFocus():
            return self.cspEdit
        elif self.threadEdit.isModified() and not self.cspEdit.isModified():
            return self.threadEdit
        elif self.cspEdit.isModified() and not self.threadEdit.isModified():
            return self.cspEdit
        else:
            return self.threadEdit
    
    def message(self, msg):
        """Show a message on the status bar for two seconds.
        """
        self.statusBar().showMessage(msg, msecs=2000)
        return

    def set_filename(self, name):
        # TODO: deal with threaded / csp filenames separately.
        if type(name) == str:
            self.filename = Qt.QString(name)
        else:
            self.filename = name
        self.setWindowTitle(str(name))
        return

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
        self.action_Delete_Edit.setIcon(Qt.QIcon.fromTheme('edit-delete'))
        self.action_Select_All_Edit.setIcon(Qt.QIcon.fromTheme('edit-select-all'))
        # Source menu.
        # Run menu.
        self.action_Run_CSP_Code_Run.setIcon(Qt.QIcon.fromTheme('media-playback-start'))
        self.action_Run_Threaded_Code_Run.setIcon(Qt.QIcon.fromTheme('media-playback-start'))
        # Bijector menu.
        self.action_Convert_to_CSP_Bijector.setIcon(Qt.QIcon.fromTheme('go-first'))
        self.action_Convert_to_Threads_Bijector.setIcon(Qt.QIcon.fromTheme('go-last'))
        # Window menu.
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
                            MainWindow.BREAK_MARKER_NUM)
        editor.setMarkerBackgroundColor(Qt.QColor("#0099FF"),
                                        MainWindow.BREAK_MARKER_NUM)
        editor.setMarkerForegroundColor(Qt.QColor("#000000"),
                                        MainWindow.BREAK_MARKER_NUM)
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

    #
    # File menu actions.
    #
    
    def new_file(self):
        self.get_editor().clear()
        self.set_filname('')
        self.message('New file started')
        self.get_editor().setModified(False)
        self.action_Close_File.setDisabled(False)
        return
    
    def load_file(self):
        fn = Qt.QFileDialog.getOpenFileName(self, 'Open File', self.userdir)
        if fn.isEmpty():
            self.message('Loading aborted')
            return

        fileName = str(fn)

        try:
            f = open(fileName,'r')
        except Exception, e:
            return

        self.get_editor().clear()
        for line in f:
            self.get_editor().append(line)
        f.close()

        self.get_editor().setModified(False)

        self.set_filename(fileName)

        self.message('Loaded document %s' % (self.filename))
        self.action_Close_File.setDisabled(False)
        return


    def clear_recent_files(self):
        """Clear list of recent files.
        """
        print 'Clear recent file list.'
        # WRITEME
        return
    
    def save_file(self):
        if self.filename.isEmpty():
            self.save_as_file()
            return

        try:
            f = open(str(self.filename),'w+')
        except Exception, e:
            self.message('Could not write to %s' % self.filename)
            return

        f.write(str(self.get_editor().text()))
        f.close()

        self.get_editor().setModified(False)
        self.message('File %s saved' % (self.filename))
        self.action_Close_File.setDisabled(False)

        # Auto-convert between concurrency models.
        if self.get_editor() is self.threadEdit:
            self.to_csp()
        else:
            self.to_threads()
        return

    def save_as_file(self):
        fn = Qt.QFileDialog.getSaveFileName(self, 'Save File', self.userdir)
        if not fn.isEmpty():
            self.set_filename(fn)
            self.save_file()
        else:
            self.message('Saving aborted')
        self.action_Close_File.setDisabled(False)

        # Auto-convert between concurrency models.
        if self.get_editor() is self.threadEdit:
            self.to_csp()
        else:
            self.to_threads()
        return

    def print_file(self):
        Margin = 10
        pageNo = 1

        if self.printer.setup(self):
            self.message('Printing...')

            p = Qt.QPainter()
            p.begin(self.printer)
            p.setFont(self.get_editor().font())
            yPos = 0
            fm = p.fontMetrics()

            width = self.printer.metric(Qt.QPaintDevice.PdmWidth)
            height = self.printer.metric(Qt.QPaintDevice.PdmHeight)
            
            for i in range(self.get_editor().numLines):
                if Margin + yPos > height - Margin:
                    pageNo = pageNo + 1
                    self.message('Printing (page %d)...' % (pageNo))
                    self.printer.newPage()
                    yPos = 0

#                p.drawText(Margin, Margin + yPos, width, fm.lineSpacing(), Qt.TextFlag.ExpandTabs | Qt.TextFlag.WordWrap, self.get_editor().textLine(i))
                yPos = yPos + fm.lineSpacing()

            p.end()
            self.message('Printing completed')
        else:
            self.message('Printing aborted')
        return
 
    def close_file(self):
        if self.get_editor().isModified():
            rc = Qt.QMessageBox.information(self,'pyBijector',
                                            'The document has been changed since the last save.',
                                            'Save Now', 'Cancel', 'Leave Anyway', 0, 1)
            if rc == 0:
                self.save_file()
            elif rc == 1:
                return

        self.get_editor().clear()
        self.set_filename('')
        self.setWindowTitle(self.app_name)
        self.action_Close_File.setDisabled(True)
        return

    #
    # Edit menu actions.
    #

    def cut(self):
        self.get_editor().cut()
        return

    def copy(self):
        self.get_editor().copy()
        return
    
    def paste(self):
        self.get_editor().paste()
        return

    def delete(self):
        self.get_editor().delete()
        return

    def undo(self):
        self.get_editor().undo()
        return

    def redo(self):
        self.get_editor().redo()
        return

    def select_all(self):
        self.get_editor().selectAll()
        return

    #
    # Search menu actions.
    #

    def find(self):
        editor = self.get_editor()
        self.searchString, ok = Qt.QInputDialog.getText(self, self.app_name, 'Find:',
                                           Qt.QLineEdit.Normal, '')
        if ok:
            # searchString, isRegExp, isCaseSensitive, wholeWords, wrapAround
            isFound = editor.findFirst(self.searchString, False, True, True, True)
            if not isFound:
                Qt.QMessageBox.information(self, self.app_name,
                                           self.searchString + ' not found in document.')
        return
    
    def find_next(self):
        if not self.get_editor().findNext():
            Qt.QMessageBox.information(self, self.app_name,
                                       ('No more occurances of ' +
                                        self.searchString +
                                        ' found in document.'))
        return
    
    def find_previous(self):
        # WRITEME
        return
    
    def replace(self):
        # WRITEME
        return
    
    def goto_line(self):
        """Goto a specific line in the current editor.
        """
        editor = self.get_editor()
        line_number, ok = Qt.QInputDialog.getInt(self, self.app_name, 'Line number:',
                                                 # value, min, max, step
                                                 editor.getCursorPosition()[0]+1, 1, editor.lines(), 1)
        # Only act if the user pressed 'ok'.
        if ok:
            editor.setCursorPosition(line_number - 1, 0)
        return
    
    #
    # Source menu actions.
    #

    def fold_all(self):
        self.get_editor().foldAll()
        return

    def toggle_folding_mode(self):
        if self.action_Folding_Mode_Source.isChecked():
            self.get_editor().setFolding(4)
        else:
            self.get_editor().setFolding(0)
        return

    def clear_all_folds(self):
        self.get_editor().clearFolds()
        return

    def indent_selection(self):
        editor = self.get_editor()
        if editor.hasSelectedText():
            lineFrom, indexFrom, lineTo, indexTo = self.get_current_selection()
            for line in xrange(lineFrom, lineTo):
                editor.indent(line)
        else:
            line, index = editor.getCursorPosition()
            editor.indent(line)
        return

    def unindent_selection(self):
        editor = self.get_editor()
        if editor.hasSelectedText():
            lineFrom, indexFrom, lineTo, indexTo = self.get_current_selection()
            for line in xrange(lineFrom, lineTo):
                editor.unindent(line)
        else:
            line, index = editor.getCursorPosition()
            editor.unindent(line)
        return

    def toggle_word_wrap(self):
        if self.action_Word_Wrap_Source.isChecked():
            self.get_editor().setWrapMode(1)
        else:
            self.get_editor().setWrapMode(0)
        return

    def toggle_whitespace_visible(self):
        if self.action_Whitespace_Visible_Source.isChecked():
            self.get_editor().setWhitespaceVisibility(1)
        else:
            self.get_editor().setWhitespaceVisibility(0)
        return

    #
    # Run menu actions.
    #

    def run_csp(self):
        # WRITEME
        return

    def run_threads(self):
        # WRITEME
        return

    def get_breakpoints(self, editor=None):
        if editor is None:
            editor = self.get_editor()
        breakpoints = []
        bp, temp = -1, 0
        while not temp < bp and temp != -1:
            temp = editor.markerFindNext(bp + 1, 1 << 1)
            if temp + 1 > 0: breakpoints.append(temp + 1)
            bp = temp
        return breakpoints

    def remove_all_breakpoints(self):
        self.get_editor().markerDeleteAll(MainWindow.BREAK_MARKER_NUM)
        return
    
    def debug_csp(self):
        # WRITEME
        breakpoints = self.get_breakpoints(self.cspEdit)
        print breakpoints
        return

    def debug_threads(self):
        # WRITEME
        breakpoints = self.get_breakpoints(self.threadEdit)
        print breakpoints
        return
    
    #
    # Biject menu actions.
    #
    
    def to_csp(self):
        # WRITEME
        print 'to_csp'
        return

    def to_threads(self):
        # WRITEME
        print 'to_threads'
        return

    #
    # Window menu actions.
    #

    def toggle_console(self):
        if self.action_Toggle_Console_Window.isChecked():
            self.consoleTabs.show()
            self.pythonConsole.setFocus()
        else:
            self.consoleTabs.hide()
        return
    
    def focus_threads(self):
        if not self.threadEdit.isVisible():
            self.threadEdit.show()
        self.cspEdit.clearFocus()
        self.threadEdit.setFocus()
        return

    def focus_csp(self):
        if not self.cspEdit.isVisible():
            self.cspEdit.show()
        self.threadEdit.clearFocus()
        self.cspEdit.setFocus()
        return

    def focus_console(self):
        if not self.consoleTabs.isVisible():
            self.consoleTabs.show()
        self.pythonConsole.setFocus()
        return

    def zoom_in(self):
        self.cspEdit.zoomIn()
        self.threadEdit.zoomIn()
        return

    def zoom_out(self):
        self.cspEdit.zoomOut()
        self.threadEdit.zoomOut()
        return

    #
    # Help menu actions.
    #
    
    def about(self):
        Qt.QMessageBox.about(self, self.app_name,
                             """pyBijector translates between threaded Python code and CSP.

Please see the python-csp tutorial for more details:
http://code.google.com/p/python-csp/wiki/Tutorial
""")

    #
    # Slots without menu signals.
    #

    def autocomplete(self):
        self.get_editor().autoCompleteFromAll()
        return

    def on_margin_clicked(self, nmargin, nline, modifiers):
        # Toggle marker for the line the margin was clicked on
        if self.get_editor().markersAtLine(nline) != 0:
            self.get_editor().markerDelete(nline, MainWindow.BREAK_MARKER_NUM)
        else:
            self.get_editor().markerAdd(nline, MainWindow.BREAK_MARKER_NUM)

    def get_current_selection(self):
        lineFrom, indexFrom, lineTo, indexTo = self.get_editor().getSelection()
        return lineFrom, indexFrom, lineTo, indexTo

    def lint_error(self, linenum, msg):
        self.get_editor().annotate(linenum - 1, msg, self.hilite)
        return

    def clear_all_lint_errors(self):
        self.get_editor().clearAnnotations(-1)
        return

    def clear_lint_error(self, linenum):
        self.get_editor().clearAnnotations(linenum - 1)
        return

