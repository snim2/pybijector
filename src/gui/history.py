#!/usr/bin/env python

"""
History management for text edit widgets.

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

from PyQt4 import Qt, QtCore

from basics import uniq

__author__ = 'Sarah Mount <s.mount@wlv.ac.uk>'
__credits__ = 'http://diotavelli.net/PyQtWiki/Capturing_Output_from_a_Process'
__date__ = 'April 2011'

# pylint: disable=W0511


class HistoryEventFilter(Qt.QObject):
    HISTORY = 200

    def __init__(self, parent, settings_manager):
        Qt.QObject.__init__(self, parent)
        self.settings = settings_manager
        self.editor = parent
        self.editor.installEventFilter(self)
        self.history = self.get_history()
        return

    # Overridden from Qt.QObject.
    def eventFilter(self, obj, event):
        """Filter up and down keypresses to manage history.
        """
        if not event.type() == Qt.QEvent.KeyPress:
            self.editor.eventFilter(obj, event)
            return False
        elif event.key() == QtCore.Qt.Key_Up:
            self.set_text_previous()
            return True
        elif event.key() == QtCore.Qt.Key_Down:
            self.set_text_next()
            return True
        return False

    def get_history(self):
        """Get history for the line edit widget.
        Should only be called once by the constructor.
        """
        if not self.settings:
            return []
        history = self.settings.get_value(self.editor.objectName())
        if history is None:
            return []
        elif not isinstance(history, Qt.QStringList):
            return [history]
        return list(history)

    def insert(self, text):
        """Insert text into the history of the line edit widget.
        """
        if self.history is None or self.history == []:
            self.history = [text]
        else:
            self.history.insert(0, text)
            self.history = uniq(self.history) # Remove duplicates.
        if len(self.history) > HistoryEventFilter.HISTORY:
            del self.history[HistoryEventFilter.HISTORY:]
        return

    def save_history(self):
        self.settings.set_value(self.editor.objectName(), self.history)
        return

    def set_text_previous(self):
        """Get the next item in the object history and display in editor.
        Signaled by Key_Up.
        """
        if not self.history:
            return
        text = self.editor.text()
        if text in self.history:
            index = (self.history.index(text) + 1) % len(self.history)
        else:
            index = 0
        self.editor.setText(self.history[index])
        return

    def set_text_next(self):
        """Get the previous item in the object history and display in editor.
        Signaled by Key_Down.
        """
        if not self.history:
            return
        text = self.editor.text()
        if text in self.history:
            index = self.history.index(text) - 1
        else:
            index = -1
        self.editor.setText(self.history[index])
        return
