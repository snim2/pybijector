#!/usr/bin/env python

"""
Run an external lint program, and parse its output.

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
import re

__author__ = 'Sarah Mount <s.mount@wlv.ac.uk>'
__date__ = 'April 2011'


class Lint(Qt.QWidget):
    # Based loosely on the PyQt wiki page:
    # http://diotavelli.net/PyQtWiki/Capturing_Output_from_a_Process
    # Edited by: Mathias Helminger, DavidBoddie, 193, cm-62
    def __init__(self, lint):    
        Qt.QWidget.__init__(self)
        self.lint = lint
        self.process = Qt.QProcess()
        self.output = None
        self.errors = None
        self.connect(self.process, Qt.SIGNAL("finished(int)"), self.finished)
        self.connect(self.process, Qt.SIGNAL("readyReadStderr()"), self.readErrors)
        return
        
    def start(self, filename, args):
        self.output = None
        self.errors = None
        lint_args = args + [filename]
        self.process.start(self.lint, lint_args)
        return

    def finished(self, exit_status):
        self.readOutput()
        return

    def readOutput(self):
        self.output = self.process.readAllStandardOutput()
        self.emit(Qt.SIGNAL("results(QString)"), Qt.QString(self.lint))
        return
    
    def readErrors(self):
        self.errors = self.process.readLineStderr()
        return


class LintMessage(object):
    SEVERITIES = {'F':'Fatal',
                  'E':'Error',
                  'W':'Warning',
                  'I':'Information',
                  'R':'Refactor',
                  'C':'Convention',
                  'I':'Information',
                  }

    def __init__(self, linenum, message, severity):
        self.linenum = linenum
        self.message = message
        self.severity = severity
        return

    def __str__(self):
        return ':'.join([self.severity, str(self.linenum), self.message])


class LintOutputIterator(object):

    def __init__(self, lint_output):
        self.results = []
        self.lint_output = lint_output.split('\n')
        self.index = 0
        return


class CSPLintIterator(LintOutputIterator):

    def __init__(self, lint_output):
        LintOutputIterator.__init__(self, lint_output)
        re1 = '.*?\['	
        re2 = '(\S*\\.py)'
        re3 = '.*?'	
        re4 = '(\d+)'	
        re5 = '\].*?'	
        re6 = '(\w\d\d\d)'
        re7 = '.*?'	
        re8 = '(:)'
        re9 = '(.*)$'
        self.pattern = re.compile(re1+re2+re3+re4+re5+re6+re7+re8+re9,
                                  re.IGNORECASE|re.DOTALL)
        return

    def __iter__(self):
        return self

    def next(self):
        if self.index >= len(self.lint_output):
            raise StopIteration
        
        result = self.lint_output[self.index].strip()
        res = re.match(self.pattern, result)
        self.index += 1

        if not result:
            return None
        try:
            return LintMessage(res.group(2), res.group(5), res.group(3)[0])
        except Exception, e:
            return None


class PyLintIterator(LintOutputIterator):

    def __init__(self, lint_output):
        LintOutputIterator.__init__(self, lint_output)
        self.pattern = re.compile('^(\w)(\d\d\d\d)(:)\s*(...)(:)\s*(.*)$',
                                  re.IGNORECASE|re.DOTALL)
        return

    def __iter__(self):
        return self

    def next(self):
        if self.index >= len(self.lint_output):
            raise StopIteration
        
        result = self.lint_output[self.index].strip()
        res = re.match(self.pattern, result)
        self.index += 1

        if not result:
            return None
        try:
            return LintMessage(res.group(4), res.group(6), res.group(1))
        except Exception, e:
            return None


