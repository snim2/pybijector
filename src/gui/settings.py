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
