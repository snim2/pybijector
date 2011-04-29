#!/usr/bin/env python

"""
Bijective editor for python-csp / threaded Python code.

Current features:
 * Folding mode.
 * Word wrap.
 * Visible whitespace.
 * Code autocompletion (Ctrl+Space).
 * Increase / decrease font size.
 * Automatic annotations for lint reports.
 * Interactive Python interpreter.

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

from PyQt4 import Qt

from bijector_main import Ui_MainWindow
from lint import Lint, PyLintIterator, CSPLintIterator
from interpreter import Interpreter
from styling import StyleMixin

import os
import syntax # Basic syntax highlighting where QScintilla would be overkill.

__author__ = 'Sarah Mount <s.mount@wlv.ac.uk>'
__date__ = 'April 2011'

# pylint: disable=W0231
# pylint: disable=W0613
# pylint: disable=W0511

# TODO: Replace.
# TODO: Interactive Python debugger.
# TODO: Interactive python-csp debugger.
# FIXME: get_editor() sometimes returns wrong editor.

class MainWindow(Qt.QMainWindow, Ui_MainWindow, StyleMixin):
    """Creates the Main Window of the application using the main 
    window design in the gui.bijector_main module.
    """
    MAX_RECENT_FILES = 10
    CSPLINT = '/usr/local/bin/csplint'
    PYLINT = '/usr/bin/pylint'
    PYTHON = '/usr/bin/python'
    PDB = '/usr/bin/pdb'
    CSPDB = '/usr/local/bin/cspdb'
    
    # Editor slots contains names of SLOTs from the QScintilla editor
    # widgets. We take SIGNALs from the MainWindow object and pass
    # them to slots in whichever editor pane is currently active.
    EDITOR_SLOTS = ['cut', 'copy', 'paste', 'undo', 'redo', 'selectAll',
                    'foldAll', 'clearFolds', 'zoomIn', 'zoomOut',
                    'autoCompleteFromAll']
    
    def __init__(self, parent=None):
        Qt.QMainWindow.__init__(self)
        self.setupUi(self)
        self.setup_styling()
        self.setup_icons()
        self.app_name = 'PyBijector'
        self.setWindowTitle(self.app_name)
        self.action_Close_File.setDisabled(True)
        # FIXME: Use Qt resources instead of static filenames.
        self.setWindowIcon(Qt.QIcon('images/pythoncsp-logo.png'))
        self.userdir = os.path.expanduser('~')
        self.filename = Qt.QString('')
        self.searchString = None # Used in search / replace        
        # Setup styling for editor panes.
        self.setup_editor(self.threadEdit)
        self.setup_editor(self.cspEdit)
        # Set checkable actions.
        self.action_Debugger_Toolbar_View.setChecked(True)
        self.debug_toolbar_view()
        self.action_Toggle_Console_Window.setChecked(False)
        self.consoleTabs.hide()
        self.action_Folding_Mode_Source.setChecked(True)
        self.toggle_folding_mode()
        self.action_Whitespace_Visible_Source.setChecked(True)
        self.toggle_whitespace_visible()
        self.action_Word_Wrap_Source.setChecked(True)
        self.toggle_word_wrap()
        # Apply basic syntax highlighting to consoles.
        self.highlight_python = syntax.PythonHighlighter(self.pythonConsole.document())
        self.highlight_thread = syntax.PythonHighlighter(self.threadConsole.document())
        self.highlight_csp = syntax.PythonHighlighter(self.cspConsole.document())
        # Populate recent file list.
        self.recent_file_acts = None
        self.update_recent_file_actions()
        # Shortcuts without menu items
        self.connect(Qt.QShortcut(Qt.QKeySequence("Ctrl+Space"), self), 
                     Qt.SIGNAL('activated()'),
                     self.autoCompleteFromAll)
        # Set up linting.
        self.csplint = Lint(MainWindow.CSPLINT, ['-p'], self.cspEdit,
                            CSPLintIterator, self.message)
        self.pylint = Lint(MainWindow.PYLINT, ['-f', 'text', '-r', 'n'],
                           self.threadEdit, PyLintIterator, self.message)
        # Set up interpreters and debuggers.
        self.csp_interp = Interpreter(MainWindow.PYTHON, self.cspConsole)
        self.thread_interp = Interpreter(MainWindow.PYTHON, self.threadConsole)
        self.python_console = Interpreter(MainWindow.PYTHON, self.pythonConsole,
                                          line_edit=self.pythonLineEdit)
        self.python_console.start_interactive(['-B', '-i', '-u', '-'])
        self.pythonConsole.moveCursor(Qt.QTextCursor.End)
        # Start with focus on the left hand pane.
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
        self.setWindowTitle(name)

        settings = Qt.QSettings(self.app_name, self.app_name)
        files = settings.value('recentFileList')
        if files is None:
            files = [name]
        elif name:
            files.insert(0, name)
            files = list(set(files)) # Remove duplicates.
            del files[MainWindow.MAX_RECENT_FILES:]

        settings.setValue('recentFileList', files)
        self.update_recent_file_actions()
        return

    #
    # Route SLOTS from this object to the currently active editor.
    #

    def __getattr__(self, name):
        if name in MainWindow.EDITOR_SLOTS:
            return getattr(self.get_editor(), name)
        else:
            return object.__getattribute__(self, name)

    #
    # File menu actions.
    #
    
    def new_file(self):
        self.get_editor().clear()
        self.set_filename('')
        self.message('New file started')
        self.get_editor().setModified(False)
        self.action_Close_File.setDisabled(False)
        return
    
    def load_file(self, editor=None, filename=None):
        if filename is None:
            fn = Qt.QFileDialog.getOpenFileName(self, 'Open File', self.userdir)
            if fn.isEmpty():
                self.message('Loading aborted')
                return
            filename = str(fn)

        if editor is None:
            editor = self.get_editor()

        try:
            with open(filename, 'r') as f: 
                editor.clear()
                for line in f:
                    editor.append(line)
        except Exception, e:
            self.message('Could not open file %s.' % filename)
            return

        editor.setModified(False)
        self.set_filename(filename)
        self.message('Loaded document %s' % (self.filename))
        self.action_Close_File.setDisabled(False)
        self.run_lint(editor)
        return

    def open_recent_file(self):
        action = self.sender()
        if action:
            self.load_file(filename=action.data())

    def clear_recent_files(self):
        """Clear list of recent files.
        """
        settings = Qt.QSettings(self.app_name, self.app_name)
        settings.setValue('recentFileList', [])
        self.update_recent_file_actions()
        return
    
    def save_file(self, editor=None):
        if self.filename.isEmpty():
            self.save_as_file()
            return

        if editor is None:
            editor = self.get_editor()

        try:
            f = open(str(self.filename),'w+')
            f.write(str(editor.text()))
            f.close()
        except Exception, e:
            self.message('Could not write to %s' % self.filename)
            return

        editor.setModified(False)
        self.message('File %s saved' % self.filename)
        self.action_Close_File.setDisabled(False)

        # Auto-convert between concurrency models.
        if editor is self.threadEdit:
            self.to_csp()
        else:
            self.to_threads()

        # Run appropriate lint.
        self.run_lint(editor)
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
            rc = Qt.QMessageBox.information(self, self.app_name,
                                            'The document has been changed since the last save.',
                                            'Save Now', 'Cancel', 'Leave Anyway', 0, 1)
            if rc == 0:
                self.save_file()
            elif rc == 1:
                return

        self.get_editor().clear()
        old_filename = self.filename
        self.set_filename('')
        self.setWindowTitle(self.app_name)
        self.action_Close_File.setDisabled(True)
        self.message('Closed %s.' % old_filename)
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
        if self.searchString is None:
            self.find()
        elif not self.get_editor().findNext():
            Qt.QMessageBox.information(self, self.app_name,
                                       ('No more occurances of ' +
                                        self.searchString +
                                        ' found in document.'))
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
        if ok: # Only act if the user pressed 'ok'.
            editor.setCursorPosition(line_number - 1, 0)
            self.message('At line %d.' % line_number)
        return
    
    #
    # Source menu actions.
    #

    def toggle_folding_mode(self):
        if self.action_Folding_Mode_Source.isChecked():
            self.get_editor().setFolding(StyleMixin.FOLDING_ON)
        else:
            self.get_editor().setFolding(StyleMixin.FOLDING_OFF)
        return

    def clear_all_folds(self):
        self.get_editor().clearFolds()
        return

    def indent_selection(self):
        editor = self.get_editor()
        if editor.hasSelectedText():
            lineFrom, indexFrom, lineTo, indexTo = self.get_current_selection(editor)
            for line in xrange(lineFrom, lineTo + 1):
                editor.indent(line)
        else:
            line, index = editor.getCursorPosition()
            editor.indent(line)
        return

    def unindent_selection(self):
        editor = self.get_editor()
        if editor.hasSelectedText():
            lineFrom, indexFrom, lineTo, indexTo = self.get_current_selection(editor)
            for line in xrange(lineFrom, lineTo + 1):
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
        """Run code in the CSP editor pane and display output in a console.
        """
        self.cspConsole.clear()
        if not self.action_Toggle_Console_Window.isChecked():
            self.action_Toggle_Console_Window.setChecked(True)
            self.toggle_console()
        self.consoleTabs.setCurrentIndex(2)
        self.csp_interp.start(self.filename, [])
        return

    def run_threads(self):
        """Run code in the thread editor pane and display output in a console.
        """
        self.threadConsole.clear()
        if not self.action_Toggle_Console_Window.isChecked():
            self.action_Toggle_Console_Window.setChecked(True)
            self.toggle_console()
        self.consoleTabs.setCurrentIndex(1)
        self.thread_interp.start(self.filename, [])
        return

    #
    # Debug menu.
    #
    
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

    def set_breakpoint(self):
        # WRITEME
        return

    def print_stacktrace(self):
        # WRITEME
        return

    def debug_step(self):
        # WRITEME
        return
    
    def debug_next(self):
        # WRITEME
        return
    
    def debug_return(self):
        # WRITEME
        return
    
    def debug_continue(self):
        # WRITEME
        return
    
    def debug_jump(self):
        # WRITEME
        return
    
    def debug_args(self):
        # WRITEME
        return
    
    def debug_eval(self):
        # WRITEME
        return

    def debug_until(self):
        # WRITEME
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
    # View menu actions.
    #

    def debug_toolbar_view(self):
        if self.action_Debugger_Toolbar_View.isChecked():
            self.debugToolBar.show()
        else:
            self.debugToolBar.hide()
        return
    
    def toggle_console(self):
        if self.action_Toggle_Console_Window.isChecked():
            self.consoleTabs.show()
            self.consoleTabs.setCurrentWidget(self.pythonConsole)
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

    #
    # Help menu actions.
    #
    
    def about(self):
        Qt.QMessageBox.about(self, self.app_name,
                             """%s translates between threaded Python code and CSP. 

Please see the python-csp tutorial for more details:
http://code.google.com/p/python-csp/wiki/Tutorial
""" % self.app_name)

    #
    # Slots without menu signals.
    #

    def on_margin_clicked(self, nmargin, nline, modifiers):
        # Toggle marker for the line the margin was clicked on
        if self.get_editor().markersAtLine(nline) != 0:
            self.get_editor().markerDelete(nline, MainWindow.BREAK_MARKER_NUM)
        else:
            self.get_editor().markerAdd(nline, MainWindow.BREAK_MARKER_NUM)

    def get_current_selection(self, editor=None):
        if editor is None:
            editor = self.get_editor()
        lineFrom, indexFrom, lineTo, indexTo = editor.getSelection()
        return lineFrom, indexFrom, lineTo, indexTo


    def update_recent_file_actions(self):
        settings = Qt.QSettings(self.app_name, self.app_name)
        files = settings.value('recentFileList')
        if files is None:
            return
        
        numRecentFiles = min(len(files), MainWindow.MAX_RECENT_FILES)

        if self.recent_file_acts is None:
            self.recent_file_acts = []
            for i in xrange(MainWindow.MAX_RECENT_FILES):
                self.recent_file_acts.append(Qt.QAction(self,
                                                        visible=False,
                                                        triggered=self.open_recent_file))
                self.menu_Recent_Files.addAction(self.recent_file_acts[i])
        for i in xrange(numRecentFiles):
            text = "&%d %s" % (i + 1, self.strippedName(files[i]))
            self.recent_file_acts[i].setText(text)
            self.recent_file_acts[i].setData(files[i])
            self.recent_file_acts[i].setVisible(True)
        for j in range(numRecentFiles, MainWindow.MAX_RECENT_FILES):
            self.recent_file_acts[j].setVisible(False)
        return

    def strippedName(self, fullFileName):
        return Qt.QFileInfo(fullFileName).fileName()

    def run_lint(self, editor):
        if editor == self.cspEdit:
            self.csplint.start(self.filename)
        else:
            self.pylint.start(self.filename)
        return

    def closeEvent(self, event):
        if self.threadEdit.isModified() or self.cspEdit.isModified():
            quit_msg = 'Would you like to save your changes before leaving ' + self.app_name + '?'
            reply = Qt.QMessageBox.question(self, self.app_name, quit_msg,
                                            Qt.QMessageBox.Save, Qt.QMessageBox.Discard, Qt.QMessageBox.Cancel)

            if reply == Qt.QMessageBox.Save:
                self.save_file()
                self.python_console.terminate()
                event.accept()
            elif reply == Qt.QMessageBox.Discard:
                self.python_console.terminate()
                event.accept()
            elif reply == Qt.QMessageBox.Cancel:
                event.ignore()
        else:
            self.python_console.terminate()
            event.accept()
        return
