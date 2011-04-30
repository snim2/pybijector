#!/usr/bin/env python

"""
Search and replace for pybijector.

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

from find_dialog import Ui_Dialog

__author__ = 'Sarah Mount <s.mount@wlv.ac.uk>'
__credits__ = 'http://diotavelli.net/PyQtWiki/Capturing_Output_from_a_Process'
__date__ = 'April 2011'

# pylint: disable=W0231


class FindReplaceDialog(Qt.QDialog, Ui_Dialog):

    def __init__(self, parent, editor=None):
        Qt.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.search_string = None
        if editor is None:
            self.editor = parent.threadEdit
        else:
            self.editor = editor
        return

    def find(self):
        self.search_string = self.searchEdit.text()
        self.editor.findFirst(self.search_string,
                              self.regexCheck.isChecked(),
                              self.matchCaseCheck.isChecked(),
                              self.entireWordsCheck.isChecked(),
                              self.wrapCheck.isChecked(),
                              not self.backwardsCheck.isChecked(),
                              -1, # Start from current line.
                              -1, # Start from current cursor index.
                              True) # Make found text visible.
        return

    def replace(self):
        if not self.search_string == self.searchEdit.text():
            self.find()
        self.editor.replace(self.replaceEdit.text())
        return

    def replace_all(self):
        if not self.search_string == self.searchEdit.text():
            self.find()
        replace_string = self.replaceEdit.text()
        while True:
            self.editor.replace(replace_string)
            if not self.editor.findNext():
                break
        return

    def reject(self):
        self.search_string = None
        self.hide()
        return
