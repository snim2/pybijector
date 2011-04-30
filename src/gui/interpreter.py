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


class Debugger(AbstractProcess):

    def __init__(self, debugger, args, console=None, line_edit=None, prompt=None): 
        AbstractProcess.__init__(self, debugger, args, console=console, line_edit=line_edit, prompt=prompt)
        self.connect(self, Qt.SIGNAL('results()'), self.append)
        return        

    def debug_remove_all_breakpoints(self):
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

    def __init__(self, debugger, args, console=None, line_edit=None, prompt=None):
        Debugger.__init__(self, debugger, args, console=console, line_edit=None, prompt=None)
        return

    def __str__(self):
        return 'PDB interface'
