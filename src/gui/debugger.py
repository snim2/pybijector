#!/usr/bin/env python

"""
Run an external debugger, and parse its output.

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

__author__ = 'Sarah Mount <s.mount@wlv.ac.uk>'
__credits__ = 'http://diotavelli.net/PyQtWiki/Capturing_Output_from_a_Process'
__date__ = 'April 2011'

# pylint: disable=W0511

class Debugger(Qt.QWidget):

    def __init__(self, debugger, console, line_edit=None, prompt=None): 
        Qt.QWidget.__init__(self)
        self.process = Qt.QProcess()
        self.debugger = debugger
        self.prompt = prompt
        # Input / output
        self.line_edit = line_edit
        self.console = console
        self.process.setReadChannel(Qt.QProcess.StandardOutput)
        # Merge STDOUT and STDERR.
        self.process.setProcessChannelMode(Qt.QProcess.MergedChannels)
        # Store text from STDOUT.
        self.output = None
        # Start cursor in right place. Important when the running
        # process start with some output (e.g. debugger REPLs).
        self.console.moveCursor(Qt.QTextCursor.End)
        # Signals and slots
        self.connect(self.process, Qt.SIGNAL("finished(int)"), self.finished)
        self.connect(self.process, Qt.SIGNAL("readyReadStandardOutput()"), self.readOutput)
        if self.line_edit is not None:
            self.connect(self.line_edit, Qt.SIGNAL('returnPressed()'), self.input)
        self.connect(self, Qt.SIGNAL('results()'), self.append)
        return
        
    def start(self, filename, args):
        """Start the running process asynchronously.
        """
        interp_args = args + [filename]
        self.process.start(self.debugger, interp_args)
        return

    def start_interactive(self, args):
        """Start a long running interactive process which we expect to
        take input from the user.
        """
        self.process.start(self.debugger, args)
        self.process.waitForStarted(-1)
        return

    def finished(self, exit_status):
        """SLOT called when the process has finished.
        """
        self.readOutput()
        return

    def readOutput(self):
        """Called when STDOUT is ready to be read.
        """
        self.output = self.process.readAllStandardOutput()
        self.emit(Qt.SIGNAL("results()"))
        return
    
    def write(self, data):
        """Write data to the STDIN of a running process.
        """
        self.process.write(str(data) + '\n')
        self.process.waitForBytesWritten(-1)
        return

    def terminate(self):
        """Kill this process.
        """
        self.process.kill()
        return

    def append(self, text=None):
        """Append text to the visible console.
        """
        self.console.moveCursor(Qt.QTextCursor.End)
        if text is None:
            self.console.insertPlainText(str(self.output))
        else:
            self.console.insertPlainText(str(text))
        self.console.ensureCursorVisible()
        return

    def input(self):
        """Take input form the line editor and send it to the running process.
        Ensure it is displayed on the visible console.
        """
        code = self.line_edit.text()
        if self.prompt:
            self.append(self.prompt + code + '\n')
        else:
            self.append(code + '\n')
        self.write(code)
        self.line_edit.clear()
        return

    def debug_remove_all_breakpoints(self):
#        self.get_editor().markerDeleteAll(MainWindow.BREAK_MARKER_NUM)
        return
    
    def debug_set_breakpoint(self):
        # WRITEME
        return

    def debug_print_stacktrace(self):
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

class PdbDebugger(Debugger):

    def __init__(self, debugger, console, line_edit=None, prompt=None):
        Debugger.__init__(self, debugger, console, line_edit=None, prompt=None)
        return

    def __str__(self):
        return 'PDB interface'
