#!/usr/bin/env python

"""
Manage settings for a particular app.

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

from settings_dialog import Ui_SettingsDialog

__author__ = 'Sarah Mount <s.mount@wlv.ac.uk>'
__date__ = 'April 2011'

# pylint: disable=W0511

class SettingsManager(object):

    def __init__(self, author, app_name):
        self.settings = Qt.QSettings(author, app_name)
        return

    def get_value(self, name):
        try:
            return self.settings.value(name)
        except Exception, e:
            return None

    def set_value(self, name, value):
        self.settings.setValue(name, value)
        return


class SettingsDialog(Qt.QDialog, Ui_SettingsDialog):

    def __init__(self, parent, settings):
        Qt.QDialog.__init__(self, parent)
        self.settings = settings
        self.setupUi(self)
        self.pythonEdit.setText(self.settings.get_value('python'))
        self.pdbEdit.setText(self.settings.get_value('pdb'))
        self.pylintEdit.setText(self.settings.get_value('pylint'))
        self.cspdbEdit.setText(self.settings.get_value('cspdb'))
        self.csplintEdit.setText(self.settings.get_value('csplint'))
        return

    def accept(self):
        self.settings.set_value('python',  self.pythonEdit.text())
        self.settings.set_value('pdb',     self.pdbEdit.text())
        self.settings.set_value('pylint',  self.pylintEdit.text())
        self.settings.set_value('cspdb',   self.cspdbEdit.text())
        self.settings.set_value('csplint', self.csplintEdit.text())
        Qt.QDialog.accept(self)
        return
