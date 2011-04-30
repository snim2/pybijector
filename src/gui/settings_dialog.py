# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/settings_dialog.ui'
#
# Created: Sat Apr 30 21:38:25 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName(_fromUtf8("SettingsDialog"))
        SettingsDialog.resize(474, 222)
        self.formLayout = QtGui.QFormLayout(SettingsDialog)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(SettingsDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.pythonEdit = QtGui.QLineEdit(SettingsDialog)
        self.pythonEdit.setObjectName(_fromUtf8("pythonEdit"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.pythonEdit)
        self.label_2 = QtGui.QLabel(SettingsDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.pdbEdit = QtGui.QLineEdit(SettingsDialog)
        self.pdbEdit.setObjectName(_fromUtf8("pdbEdit"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.pdbEdit)
        self.label_3 = QtGui.QLabel(SettingsDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.pylintEdit = QtGui.QLineEdit(SettingsDialog)
        self.pylintEdit.setObjectName(_fromUtf8("pylintEdit"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.pylintEdit)
        self.label_4 = QtGui.QLabel(SettingsDialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.cspdbEdit = QtGui.QLineEdit(SettingsDialog)
        self.cspdbEdit.setObjectName(_fromUtf8("cspdbEdit"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.cspdbEdit)
        self.label_5 = QtGui.QLabel(SettingsDialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_5)
        self.csplintEdit = QtGui.QLineEdit(SettingsDialog)
        self.csplintEdit.setObjectName(_fromUtf8("csplintEdit"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.csplintEdit)
        self.buttonBox = QtGui.QDialogButtonBox(SettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.SpanningRole, self.buttonBox)
        self.label.setBuddy(self.pythonEdit)
        self.label_2.setBuddy(self.pdbEdit)
        self.label_3.setBuddy(self.pylintEdit)
        self.label_4.setBuddy(self.cspdbEdit)
        self.label_5.setBuddy(self.csplintEdit)

        self.retranslateUi(SettingsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SettingsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)
        SettingsDialog.setTabOrder(self.pythonEdit, self.pdbEdit)
        SettingsDialog.setTabOrder(self.pdbEdit, self.pylintEdit)
        SettingsDialog.setTabOrder(self.pylintEdit, self.cspdbEdit)
        SettingsDialog.setTabOrder(self.cspdbEdit, self.csplintEdit)
        SettingsDialog.setTabOrder(self.csplintEdit, self.buttonBox)

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(QtGui.QApplication.translate("SettingsDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SettingsDialog", "&Python interpreter", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("SettingsDialog", "Python &Debugger", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("SettingsDialog", "Py&Lint", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("SettingsDialog", "python-&csp debugger", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("SettingsDialog", "python-csp lin&t", None, QtGui.QApplication.UnicodeUTF8))

