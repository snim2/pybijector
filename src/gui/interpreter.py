#!/usr/bin/env python

"""
Run an external interpreter, and parse its output.

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

from abstractprocess import AbstractProcess

__author__ = 'Sarah Mount <s.mount@wlv.ac.uk>'
__credits__ = 'http://diotavelli.net/PyQtWiki/Capturing_Output_from_a_Process'
__date__ = 'April 2011'

# pylint: disable=W0511
    

class Interpreter(AbstractProcess):

    def __init__(self, interpreter, args, console, line_edit=None, prompt=None, settings=None, history=None): 
        AbstractProcess.__init__(self, interpreter, args, console, line_edit=line_edit, prompt=prompt, settings=settings, history=history)
        self.connect(self.process, Qt.SIGNAL("readyReadStandardOutput()"), self.readOutput)
        self.connect(self, Qt.SIGNAL('results()'), self.append)
        return


class PdbDebugger(AbstractProcess):
    """Interface to the Python debugger, PDB.
    """
    
    def __init__(self, interpreter, args, console, line_edit=None, prompt=None, settings=None, history=None): 
        AbstractProcess.__init__(self, interpreter, args, console, line_edit=line_edit, prompt=prompt, settings=settings, history=history)
        self.process.setProcessChannelMode(Qt.QProcess.MergedChannels)
        self.connect(self.process, Qt.SIGNAL("readyReadStandardOutput()"), self.readOutput)
        self.connect(self, Qt.SIGNAL('results()'), self.append)
        return

    def remove_breakpoint(self, lineno):
        self.write('clear %d' % lineno)
        return

    def remove_all_breakpoints(self):
        self.write('clear')
        self.write('yes')
        return
    
    def set_breakpoint(self, lineno):
        self.write('break %d' % lineno)
        return

    def print_stacktrace(self):
        self.write('where')
        return

    def step(self):
        self.write('step')
        return
    
    def next(self):
        self.write('next')
        return
    
    def return_(self):
        self.write('return')
        return
    
    def continue_(self):
        self.write('continue')
        return
    
    def jump(self, lineno):
        self.write('jump %d' % lineno)
        return
    
    def args_(self):
        self.write('args')
        return
    
    def eval(self, expr):
        self.write('p %s' % expr)
        return

    def until(self):
        self.write('until')
        return
