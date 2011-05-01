#!/usr/bin/env python

"""
Run an external program.

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


class AbstractProcess(Qt.QWidget):

    def __init__(self, program, args, console=None, line_edit=None, settings=None, history=None, prompt=None):
        Qt.QWidget.__init__(self)
        self.program = program
        self.args = args
        self.console = console
        self.line_edit = line_edit
        self.settings = settings
        self.history = history
        self.prompt = prompt
        self.output = None
        self.errors = None
        # Set up external process.
        self.process = Qt.QProcess()
        # External I/O
        self.process.setReadChannel(Qt.QProcess.StandardOutput)
        self.process.setProcessChannelMode(Qt.QProcess.MergedChannels)
        # Signals / slots.
        self.connect(self.process, Qt.SIGNAL("finished(int)"), self.finished)
#        self.connect(self.process, Qt.SIGNAL("readyReadStderr()"), self.readErrors)
        if self.line_edit is not None:
            self.connect(self.line_edit, Qt.SIGNAL('returnPressed()'), self.input)
        return

    def save_history(self):
        if self.history:
            self.history.save_history()
        return
    
    def start(self, args=None):
        """Start external program  asynchronously.
        """
        self.output = None
        self.errors = None
        if args is None:
            args = self.args
        self.process.start(self.program, args)
        self.process.waitForStarted(-1)
        return

    def is_running(self):
        """Return True if the current process is running and False otherwise.
        """
        return self.process.state() == Qt.QProcess.Running 

    def terminate(self):
        """Kill this process.
        """
        if self.is_running():
            self.process.kill()
            self.process.waitForFinished()
        return

    def finished(self, exit_status):
        """SLOT called on completion of lint process.
        """
        self.readOutput()
        return

    def readOutput(self):
        """Read STDOUT of lint process.
        """
        self.output = self.process.readAllStandardOutput()
        self.emit(Qt.SIGNAL("results()"))
        return
    
    def readErrors(self):
        """Read STDERR of lint process.
        Only used for debugging.
        """
        self.errors = self.process.readLineStderr()
        return

    def write(self, data):
        """Write data to the STDIN of a running process.
        """
        if not self.is_running():
            return
        self.process.write(str(data) + '\n')
        self.process.waitForBytesWritten(-1)
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
        if self.line_edit is None or not self.is_running():
            return
        code = self.line_edit.text()
        if self.prompt:
            self.append(self.prompt + code + '\n')
        else:
            self.append(code + '\n')
        self.write(code)
        if self.history:
            self.history.insert(code)
        self.line_edit.clear()
        return

