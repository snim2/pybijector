#!/usr/bin/env python

"""
Run an external interpreter or debugger, and parse its output.

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
__date__ = 'April 2011'

# pylint: disable=W0511


class Interpreter(Qt.QWidget):
    # Based loosely on the PyQt wiki page:
    # http://diotavelli.net/PyQtWiki/Capturing_Output_from_a_Process
    # Edited by: Mathias Helminger, DavidBoddie, 193, cm-62
    def __init__(self, interpreter): 
        Qt.QWidget.__init__(self)
        self.interpreter = interpreter
        self.process = Qt.QProcess()
        # Merge standard in and out.
        self.process.setReadChannel(Qt.QProcess.StandardOutput)
        self.process.setProcessChannelMode(Qt.QProcess.MergedChannels)
        self.output = None
        self.errors = None
        self.connect(self.process, Qt.SIGNAL("finished(int)"), self.finished)
        self.connect(self.process, Qt.SIGNAL("readyReadStandardError()"), self.readErrors)
        self.connect(self.process, Qt.SIGNAL("readyReadStandardOutput()"), self.readOutput)
        return
        
    def start(self, filename, args):
        interp_args = args + [filename]
        self.process.start(self.interpreter, interp_args)
        return

    def start_interactive(self, args):
        self.process.start(self.interpreter, args)
        self.process.waitForStarted(-1)
        return

    def finished(self, exit_status):
        self.readOutput()
        return

    def readOutput(self):
        self.output = self.process.readAllStandardOutput()
        self.emit(Qt.SIGNAL("results(QString)"), Qt.QString(self.interpreter))
        return
    
    def readErrors(self):
        self.errors = self.process.readAllStandardError()
        return

    def write(self, data):
        self.process.write(str(data) + '\n')
        self.process.waitForBytesWritten(-1)
        return

    def terminate(self):
        self.process.kill()
        return
