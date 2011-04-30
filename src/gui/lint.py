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

from PyQt4.Qsci import QsciStyle
from abstractprocess import AbstractProcess

from PyQt4 import Qt

import os
import re

__author__ = 'Sarah Mount <s.mount@wlv.ac.uk>'
__credits__ = 'http://diotavelli.net/PyQtWiki/Capturing_Output_from_a_Process'
__date__ = 'April 2011'


class Lint(AbstractProcess): #, LintStyleMixin):

    def __init__(self, lint, args, editor, results_iter, message):
        AbstractProcess.__init__(self, lint, args, editor)
        # self.lint = lint
        # self.args = args
        # self.editor = editor
        self.results_iter = results_iter
        self.message = message # Must be callable.
        # Set up styling for annotations.        
        self.console.setAnnotationDisplay(2)
        self.font = Qt.QFont('Courier', 9, Qt.QFont.Normal, True)
        self.info = QsciStyle(-1, 'Hilite style for lint info',
                               Qt.QColor('#222222'), Qt.QColor('#FFFFFF'),
                               self.font)
        self.warning = QsciStyle(-1, 'Hilite style for lint warnings',
                                  Qt.QColor('#222222'), Qt.QColor('#FFFF44'),
                                  self.font)
        self.error = QsciStyle(-1, 'Hilite style for lint errors',
                                Qt.QColor('#222222'), Qt.QColor('#EE0000'),
                                self.font)
        self.severities = {'I':self.info, 'C':self.info, 
                           'W':self.warning, 'R':self.warning,
                           'E':self.error, 'F':self.error}
        self.connect(self, Qt.SIGNAL('results()'), self.apply_results)
        return

    def lint_error(self, msg):
        """Annotate an editor with a single LintMessage object.
        """
        if msg is None:
            return
        if msg.severity in self.severities.keys():
            hilite = self.severities[msg.severity]
        else:
            hilite = self.severities['W']
        if self.console:
            self.console.annotate(int(msg.linenum) - 1, msg.message, hilite)
        else:
            self.get_editor().annotate(int(msg.linenum) - 1, msg.message, hilite)
        return

    def clear_all_lint_errors(self):
        """Remove all annotations from the editor.
        """
        self.console.clearAnnotations(-1)
        return

    def clear_lint_error(self, linenum):
        """Remove an annotation from a given line in the editor.
        """
        self.console.clearAnnotations(linenum - 1)
        return

    def apply_results(self):
        name = os.path.basename(self.program)
        for message in self.results_iter(str(self.output)):
            self.lint_error(message)
            self.message('Code annotated with %s output.' % name)
        return
    

class LintMessage(object):
    """An individual report from a lint process.
    """

    def __init__(self, linenum, message, severity):
        self.linenum = linenum
        self.message = message
        self.severity = severity
        return

    def __str__(self):
        return ':'.join([self.severity, str(self.linenum), self.message])


class LintOutputIterator(object):
    """Iterate over all messages from a lint process.
    """

    def __init__(self, lint_output):
        self.results = []
        self.lint_output = lint_output.split('\n')
        self.index = 0
        return


class CSPLintIterator(LintOutputIterator):
    """Iterate over output from csplint.
    """

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
    """Iterate over output from pylint.
    """

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


