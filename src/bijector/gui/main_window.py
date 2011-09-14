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
 * Settings saved between sessions.

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

from PyQt4 import Qt, QtCore
from PyQt4 import uic

Ui_MainWindow, base_class = uic.loadUiType('bijector_main.ui')

from basics import uniq 
from find_replace import FindReplaceDialog
from history import HistoryEventFilter
from interpreter import Interpreter, PdbDebugger
from lint import Lint, PyLintIterator, CSPLintIterator
from settings import SettingsManager, SettingsDialog
from styling import StyleMixin


import os
import syntax # Basic syntax highlighting where QScintilla would be overkill.

__author__ = 'Sarah Mount <s.mount@wlv.ac.uk>'
__date__ = 'April 2011'

# pylint: disable=W0201
# pylint: disable=W0231
# pylint: disable=W0613
# pylint: disable=W0511

# TODO: Make use of cspdb.
# FIXME: get_editor() sometimes returns wrong editor.
# TODO: Add arguments to all settings in the settings dialog.


class MainWindow(Qt.QMainWindow, Ui_MainWindow, StyleMixin):
    """Creates the Main Window of the application using the main 
    window design in the gui.bijector_main module.
    """
    MAX_RECENT_FILES = 20
    
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
        # Manage settings.
        self.settings = SettingsManager(__author__, self.app_name)
        self.load_settings()
        # Set up GUI.
        self.setWindowTitle(self.app_name)
        self.action_Close_File.setDisabled(True)
        # FIXME: Use Qt resources instead of static filenames.
        self.setWindowIcon(Qt.QIcon('images/pythoncsp-logo.png'))
        self.userdir = os.path.expanduser('~')
        self.filename = Qt.QString('')
        # Search / replace
        self.find_dialog = None
        self.searchString = None
        # Printer
        self.printer = Qt.QPrinter()
        # Setup styling for editor panes.
        self.setup_editor(self.threadEdit)
        self.setup_editor(self.cspEdit)
        # Set checkable actions from settings.
        self.checkables = {
            self.action_Debugger_Toolbar_View : self.toggle_toolbar_view,
            self.action_Toggle_Console_Window : self.toggle_console,
            self.action_Folding_Mode_Source : self.toggle_folding_mode,
            self.action_Whitespace_Visible_Source : self.toggle_whitespace_visible,
            self.action_Word_Wrap_Source : self.toggle_word_wrap
            }
        for checkable in self.checkables:
            is_checked = self.settings.get_value(checkable.objectName())
            checkable.setChecked(is_checked == 'True')
            self.checkables[checkable]()
        # Apply basic syntax highlighting to consoles.
        self.highlight_python = syntax.PythonHighlighter(self.pythonConsole.document())
        self.highlight_thread = syntax.PythonHighlighter(self.threadConsole.document())
        self.highlight_csp = syntax.PythonHighlighter(self.cspConsole.document())
        # Populate recent file list.
        self.recent_file_acts = None
        self.update_recent_file_actions()
        # Shortcuts without menu items
        self.connect(Qt.QShortcut(Qt.QKeySequence("Ctrl+Space"), self), 
                     Qt.SIGNAL('activated()'), self.autoCompleteFromAll)
        # Set up linting.
        self.csplint = Lint(self.csplint_exec, [], self.cspEdit,
                            CSPLintIterator, self.message)
        self.pylint  = Lint(self.pylint_exec, [],
                            self.threadEdit, PyLintIterator, self.message)
        # Set up interpreters and history managers for their input widgets.
        self.history_python = HistoryEventFilter(self.pythonLineEdit, self.settings)
        self.history_thread = HistoryEventFilter(self.threadLineEdit, self.settings)
        self.history_csp    = HistoryEventFilter(self.cspLineEdit, self.settings)
        self.python_console = Interpreter(self.python_exec, ['-B', '-i', '-u', '-'],
                                          console=self.pythonConsole,
                                          line_edit=self.pythonLineEdit,
                                          settings=self.settings,
                                          history=self.history_python)
        self.thread_interp  = Interpreter(self.python_exec, [],
                                          console=self.threadConsole,
                                          line_edit=self.threadLineEdit,
                                          prompt='> ', settings=self.settings,
                                          history=self.history_thread)
        self.csp_interp     = Interpreter(self.python_exec, [],
                                          console=self.cspConsole,
                                          line_edit=self.cspLineEdit,
                                          prompt='> ', settings=self.settings,
                                          history=self.history_csp)
        self.python_console.start()
        # Set up debuggers.
        self.pdb_thread = PdbDebugger(self.pdb_exec, [],
                                      console=self.threadConsole,
                                      line_edit=self.threadLineEdit)
        self.pdb_csp    = PdbDebugger(self.pdb_exec, [],
                                      console=self.cspConsole,
                                      line_edit=self.cspLineEdit)
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

    def get_active_debugger(self):
        """Return the currently active debugger, or None if none is running.
        """
        if self.pdb_thread.is_running():
            return self.pdb_thread
        elif self.pdb_csp.is_running():
            return self.pdb_csp
        return None
    
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
        files = self.settings.get_value('recentFileList')
        if files is None:
            files = [name]
        elif name:
            files.insert(0, name)
            files = uniq(files) # Remove duplicates.
            del files[MainWindow.MAX_RECENT_FILES:]
        self.settings.set_value('recentFileList', files)
        self.update_recent_file_actions()
        return

    #
    # Route SLOTS from this object to the currently active editor.
    #

    def __getattr__(self, name):
        if name in MainWindow.EDITOR_SLOTS:
            return getattr(self.get_editor(), name)
        elif name.startswith('debug_'):
            return getattr(self.get_active_debugger(), name)
        else:
            return object.__getattribute__(self, name)

    #
    # File menu actions.
    #
    
    def new_file(self):
        self.get_editor().clear()
        self.set_filename('')
        self.get_editor().setModified(False)
        self.action_Close_File.setDisabled(False)
        self.message('New file started')
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
        return

    def clear_recent_files(self):
        """Clear list of recent files.
        """
        self.settings.set_value('recentFileList', [])
        self.update_recent_file_actions()
        self.message('Cleared list of recent files.')
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
        # Based on an example from the PyQt4 wiki.
        Margin = 10
        pageNo = 1
        print_dialog = Qt.QPrintDialog(self.printer, self)
        if (print_dialog.exec_() != Qt.QDialog.Accepted):
            self.message('Printing aborted.')
            return
        self.message('Printing %s' % self.filename)
        p = Qt.QPainter()
        p.begin(self.printer)
        p.setFont(self.get_editor().font())
        yPos = 0
        fm = p.fontMetrics()
        width = self.printer.metric(Qt.QPaintDevice.PdmWidth)
        height = self.printer.metric(Qt.QPaintDevice.PdmHeight)
        for i in xrange(self.get_editor().lines()):
            if Margin + yPos > height - Margin:
                pageNo = pageNo + 1
                self.message('Printing (page %d)...' % (pageNo))
                self.printer.newPage()
                yPos = 0
            p.drawText(Margin, Margin + yPos, width, fm.lineSpacing(),
                       QtCore.Qt.TextExpandTabs | QtCore.Qt.TextWordWrap,
                       self.get_editor().text(i))
            yPos = yPos + fm.lineSpacing()
        p.end()
        self.message('Printing completed')
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
    # Edit menu actions.
    #

    def settings_dialog(self):
        """Open the settings dialog and save settings.
        These are all currently file paths for external programs.
        
        """
        settings_dialog = SettingsDialog(self, self.settings)
        settings_dialog.exec_()
        self.load_settings()
        if settings_dialog.result() == Qt.QDialog.Rejected:
            return
        msg = 'Please restart %s for your changes to take effect.' % self.app_name
        self.message('Settings saved.')
        Qt.QMessageBox.information(self, self.app_name, msg)
        return

    def load_settings(self):
        self.python_exec  = str(self.settings.get_value('python')) or ''
        self.pdb_exec     = str(self.settings.get_value('pdb')) or ''
        self.pylint_exec  = str(self.settings.get_value('pylint')) or ''
        self.cspdb_exec   = str(self.settings.get_value('cspdb')) or ''
        self.csplint_exec = str(self.settings.get_value('csplint')) or ''
        self.message('Loaded settings.')
        return

    #
    # Search menu actions.
    #

    def find(self):
        """Simple dialog for finding text.
        """
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
            msg = 'No more occurances of %s in document.' % self.searchString
            Qt.QMessageBox.information(self, self.app_name, msg)
        return
    
    def replace(self):
        """Start the find / replace dialog modelessly.
        """
        if self.find_dialog is None:
            self.find_dialog = FindReplaceDialog(self, editor=self.get_editor())
        else:
            self.find_dialog.editor = self.get_editor()
        self.find_dialog.show()
        self.find_dialog.activateWindow()
        return
    
    def goto_line(self):
        """Goto a specific line in the current editor.
        """
        editor = self.get_editor()
        lineno, ok = Qt.QInputDialog.getInt(self, self.app_name, 'Line number:',
                                            # value, min, max, step
                                            editor.getCursorPosition()[0]+1, 1, editor.lines(), 1)
        if ok: # Only act if the user pressed 'ok'.
            editor.setCursorPosition(lineno - 1, 0)
            self.message('At line %d.' % lineno)
        return
    
    #
    # Source menu actions.
    #

    def toggle_folding_mode(self):
        if self.action_Folding_Mode_Source.isChecked():
            self.get_editor().setFolding(StyleMixin.FOLDING_ON)
            self.message('Folding mode on.')
        else:
            self.get_editor().setFolding(StyleMixin.FOLDING_OFF)
            self.message('Folding mode off.')
        return

    def clear_all_folds(self):
        self.get_editor().clearFolds()
        self.message('All folds cleared.')
        return

    def indent_selection(self):
        editor = self.get_editor()
        if editor.hasSelectedText():
            lineFrom, _, lineTo, _ = self.get_current_selection(editor)
            for line in xrange(lineFrom, lineTo + 1):
                editor.indent(line)
            self.message('Selected text indented.')
        else:
            line = editor.getCursorPosition()[0]
            editor.indent(line)
            self.message('Line %d indented.' % line)
        return

    def unindent_selection(self):
        editor = self.get_editor()
        if editor.hasSelectedText():
            lineFrom, _, lineTo, _ = self.get_current_selection(editor)
            for line in xrange(lineFrom, lineTo + 1):
                editor.unindent(line)
            self.message('Selected text unindented.')
        else:
            line = editor.getCursorPosition()[0]
            editor.unindent(line)
            self.message('Line %d unindented.' % line)
        return

    def toggle_word_wrap(self):
        if self.action_Word_Wrap_Source.isChecked():
            self.get_editor().setWrapMode(1)
            self.message('Word wrap on.')
        else:
            self.get_editor().setWrapMode(0)
            self.message('Word wrap off.')
        return

    def toggle_whitespace_visible(self):
        if self.action_Whitespace_Visible_Source.isChecked():
            self.get_editor().setWhitespaceVisibility(1)
            self.message('Whitespace made visible.')
        else:
            self.get_editor().setWhitespaceVisibility(0)
            self.message('Whitespace made invisible.')
        return

    #
    # Run menu actions.
    #

    def run_csp(self):
        """Run code in the CSP editor pane and display output in a console.
        """
        self.cspConsole.clear()
        self.focus_csp_console()
        self.csp_interp.start([self.filename])
        self.message('Running %s.' % self.filename)
        return

    def run_threads(self):
        """Run code in the thread editor pane and display output in a console.
        """
        self.threadConsole.clear()
        self.focus_thread_console()
        self.thread_interp.start([self.filename])
        self.message('Running %s.' % self.filename)
        return

    def abort_thread_console(self):
        """Terminate currently running interpreter or debugger for threaded code.
        """
        self.thread_interp.terminate()
        self.pdb_thread.terminate()
        self.message('Any running programs aborted.')
        return

    def abort_csp_console(self):
        """Terminate currently running interpreter or debugger for csp code.
        """
        self.csp_interp.terminate()
        self.pdb_csp.terminate()
        self.message('Any running programs aborted.')
        return

    #
    # Debug menu.
    #

    def remove_all_breakpoints(self):
        self.get_editor().markerDeleteAll(MainWindow.BREAK_MARKER_NUM)
        debug = self.get_active_debugger()
        if debug:
            debug.remove_all_breakpoints()        
        self.message('Breakpoints removed.')
        return

    def get_breakpoints(self, editor=None):
        """Return a list of locations of breakpoint markers.
        """
        if editor is None:
            editor = self.get_editor()
        breakpoints = []
        bp, temp = -1, 0
        while not temp < bp and temp != -1:
            temp = editor.markerFindNext(bp + 1, 1 << 1)
            if temp + 1 > 0: breakpoints.append(temp + 1)
            bp = temp
        return breakpoints

    def run_debug_csp(self):
        breakpoints = self.get_breakpoints(self.cspEdit)
        self.cspConsole.clear()
        self.focus_csp_console()
        self.pdb_csp.start(['-B', '-i', '-u', '-m', 'pdb', str(self.filename)])
        for breakpoint in breakpoints:
            self.debug_set_breakpoint(breakpoint)
        self.message('Debugging %s.' % self.filename)
        return

    def run_debug_threads(self):
        breakpoints = self.get_breakpoints(self.threadEdit)
        self.threadConsole.clear()
        self.focus_thread_console()
        self.pdb_thread.start(['-B', '-i', '-u', '-m', 'pdb', str(self.filename)])
        for breakpoint in breakpoints:
            self.debug_set_breakpoint(breakpoint)        
        self.message('Debugging %s.' % self.filename)
        return

    def debug_set_breakpoint(self, lineno=None):
        debug = self.get_active_debugger()
        if debug is None:
            return
        if lineno is None:
            editor = self.get_editor()
            lineno, ok = Qt.QInputDialog.getInt(self, self.app_name, 'Line number:',
                                                # value, min, max, step
                                                editor.getCursorPosition()[0]+1, 1, editor.lines(), 1)
            if ok:
                debug.set_breakpoint(lineno)
        else:
            debug.set_breakpoint(lineno)
        return

    def debug_remove_breakpoint(self, lineno=None):
        debug = self.get_active_debugger()
        if debug is None:
            return
        if lineno is None:
            editor = self.get_editor()
            lineno, ok = Qt.QInputDialog.getInt(self, self.app_name,
                                                'Set breakpoint at line number:',
                                                # value, min, max, step
                                                editor.getCursorPosition()[0]+1, 1, editor.lines(), 1)
            if ok:
                debug.remove_breakpoint(lineno)
        else:
            debug.remove_breakpoint(lineno)
        return
    
    def debug_print_stacktrace(self):
        debug = self.get_active_debugger()
        if debug:
            debug.print_stacktrace()
        return

    def debug_step(self):
        debug = self.get_active_debugger()
        if debug:
            debug.step()
        return
    
    def debug_next(self):
        debug = self.get_active_debugger()
        if debug:
            debug.next()
        return
    
    def debug_return(self):
        debug = self.get_active_debugger()
        if debug:
            debug.return_()
        return
    
    def debug_continue(self):
        debug = self.get_active_debugger()
        if debug:
            debug.continue_()
        return
    
    def debug_jump(self):
        debug = self.get_active_debugger()
        if debug is None:
            return
        editor = self.get_editor()
        lineno, ok = Qt.QInputDialog.getInt(self, self.app_name, 'Jump to line number:',
                                            editor.getCursorPosition()[0]+1, 1, editor.lines(), 1)
        if ok:
            debug.jump(lineno)
        return
    
    def debug_args(self):
        debug = self.get_active_debugger()
        if debug:
            debug.args_()
        return
    
    def debug_eval(self):
        debug = self.get_active_debugger()
        if debug is None:
            return
        expr, ok = Qt.QInputDialog.getText(self, self.app_name,
                                           'Expression to evaluate:',
                                           Qt.QLineEdit.Normal)
        if ok and not expr.isEmpty():
            debug.eval(str(expr))
        return

    def debug_until(self):
        debug = self.get_active_debugger()
        if debug:
            debug.until()
        return
    
    #
    # View menu actions.
    #

    def toggle_toolbar_view(self):
        """Show or hide the debugger toolbar.
        """
        if self.action_Debugger_Toolbar_View.isChecked():
            self.debugToolBar.show()
        else:
            self.debugToolBar.hide()
        return
    
    def toggle_console(self):
        if self.action_Toggle_Console_Window.isChecked():
            self.consoleTabs.show()
        else:
            self.consoleTabs.hide()
        return

    def change_focus(self, widget, isConsole, index):
        """Change the current focus to one of the text entry widgets.
        """
        if not isConsole:
            if not widget.isVisible():
                widget.show()
            widget.setFocus()
            return
        if not self.action_Toggle_Console_Window.isChecked():
            self.action_Toggle_Console_Window.setChecked(True)
            self.toggle_console()
        self.consoleTabs.setCurrentIndex(index)
        widget.setFocus()
        return    
    
    def focus_threads(self):
        self.change_focus(self.threadEdit, False, None)
        return

    def focus_csp(self):
        self.change_focus(self.cspEdit, False, None)
        return
    
    def focus_console(self):
        self.change_focus(self.pythonLineEdit, True, 0)
        return

    def focus_interpreter(self):
        self.change_focus(self.pythonLineEdit, True, 0)
        return

    def focus_thread_console(self):
        self.change_focus(self.threadLineEdit, True, 1)
        return

    def focus_csp_console(self):
        self.change_focus(self.cspLineEdit, True, 2)
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
    # Biject actions.
    #
    
    def to_csp(self):
        # WRITEME
        print 'to_csp'
        self.message('Converted %s to CSP code.' % self.filename)
        return

    def to_threads(self):
        # WRITEME
        print 'to_threads'
        self.message('Converted %s to threaded code.' % self.filename)
        return

    #
    # Slots without menu signals.
    #

    def on_margin_clicked(self, margin, lineno, modifiers):
        """Toggle marker for the line the margin was clicked on.
        Used as a placeholder for a breakpoint.
        """
        if self.get_editor().markersAtLine(lineno) != 0:
            self.get_editor().markerDelete(lineno, MainWindow.BREAK_MARKER_NUM)
            self.debug_remove_breakpoint(lineno)
        else:
            self.get_editor().markerAdd(lineno, MainWindow.BREAK_MARKER_NUM)
            self.debug_set_breakpoint(lineno)
        return

    def get_current_selection(self, editor=None):
        """Rerurns currently selected text in currently active editor.
        """
        if editor is None:
            editor = self.get_editor()
        lineFrom, indexFrom, lineTo, indexTo = editor.getSelection()
        return lineFrom, indexFrom, lineTo, indexTo

    def update_recent_file_actions(self):
        """Update actions related to recent file list.
        """
        files = self.settings.get_value('recentFileList')
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
            text = "&%d %s" % (i + 1, self.stripped_name(files[i]))
            self.recent_file_acts[i].setText(text)
            self.recent_file_acts[i].setData(files[i])
            self.recent_file_acts[i].setVisible(True)
        for j in range(numRecentFiles, MainWindow.MAX_RECENT_FILES):
            self.recent_file_acts[j].setVisible(False)
        return

    def stripped_name(self, fullFileName):
        return Qt.QFileInfo(fullFileName).fileName()

    def run_lint(self, editor):
        """Run an external static checker and display results as annotations.
        """
        if editor == self.cspEdit:
            self.csplint.start(['-p', self.filename])
        else:
            self.pylint.start(['-f', 'text', '-r', 'n', self.filename])
        return

    def clean_up(self):
        """Called before exiting the application.
        Save settings, terminate all running processes.
        """
        # Save history stored in line edit widgets.
        for console in [self.python_console, self.thread_interp, self.csp_interp]:
            console.save_history()
        # Save checkables.
        for check in self.checkables:
            self.settings.set_value(check.objectName(), str(check.isChecked()))
        # Close running processes.
        for proc in [self.python_console, self.thread_interp, self.csp_interp,
                     self.pdb_thread, self.pdb_csp, self.pylint, self.csplint]:
            proc.terminate()
        return

    def closeEvent(self, event):
        """SLOT called on closing the application.
        Saves any settings, closes all resources before exit.
        """
        if self.threadEdit.isModified() or self.cspEdit.isModified():
            msg = 'Would you like to save your changes before leaving %s? ' % self.app_name
            reply = Qt.QMessageBox.question(self, self.app_name, msg,
                                            Qt.QMessageBox.Save, Qt.QMessageBox.Discard, Qt.QMessageBox.Cancel)
            if reply == Qt.QMessageBox.Save:
                self.save_file()
                self.clean_up()
                event.accept()
            elif reply == Qt.QMessageBox.Discard:
                self.clean_up()
                event.accept()
            elif reply == Qt.QMessageBox.Cancel:
                event.ignore()
        else:
            self.clean_up()
            event.accept()
        return
