# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/find_dialog.ui'
#
# Created: Sat Apr 30 17:31:41 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(474, 301)
        self.formLayout = QtGui.QFormLayout(Dialog)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.searchEdit = QtGui.QLineEdit(Dialog)
        self.searchEdit.setObjectName(_fromUtf8("searchEdit"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.searchEdit)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.replaceEdit = QtGui.QLineEdit(Dialog)
        self.replaceEdit.setObjectName(_fromUtf8("replaceEdit"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.replaceEdit)
        self.matchCaseCheck = QtGui.QCheckBox(Dialog)
        self.matchCaseCheck.setObjectName(_fromUtf8("matchCaseCheck"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.matchCaseCheck)
        self.entireWordsCheck = QtGui.QCheckBox(Dialog)
        self.entireWordsCheck.setObjectName(_fromUtf8("entireWordsCheck"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.SpanningRole, self.entireWordsCheck)
        self.backwardsCheck = QtGui.QCheckBox(Dialog)
        self.backwardsCheck.setObjectName(_fromUtf8("backwardsCheck"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.SpanningRole, self.backwardsCheck)
        self.wrapCheck = QtGui.QCheckBox(Dialog)
        self.wrapCheck.setObjectName(_fromUtf8("wrapCheck"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.wrapCheck)
        self.regexCheck = QtGui.QCheckBox(Dialog)
        self.regexCheck.setObjectName(_fromUtf8("regexCheck"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.SpanningRole, self.regexCheck)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.findButton = QtGui.QPushButton(self.groupBox)
        self.findButton.setObjectName(_fromUtf8("findButton"))
        self.horizontalLayout.addWidget(self.findButton)
        self.replaceButton = QtGui.QPushButton(self.groupBox)
        self.replaceButton.setObjectName(_fromUtf8("replaceButton"))
        self.horizontalLayout.addWidget(self.replaceButton)
        self.replaceAllButton = QtGui.QPushButton(self.groupBox)
        self.replaceAllButton.setObjectName(_fromUtf8("replaceAllButton"))
        self.horizontalLayout.addWidget(self.replaceAllButton)
        self.closeButton = QtGui.QPushButton(self.groupBox)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.horizontalLayout.addWidget(self.closeButton)
        self.formLayout.setWidget(7, QtGui.QFormLayout.SpanningRole, self.groupBox)
        self.label.setBuddy(self.searchEdit)
        self.label_2.setBuddy(self.replaceEdit)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.findButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.find)
        QtCore.QObject.connect(self.replaceButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.replace)
        QtCore.QObject.connect(self.replaceAllButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.replace_all)
        QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.searchEdit, self.replaceEdit)
        Dialog.setTabOrder(self.replaceEdit, self.matchCaseCheck)
        Dialog.setTabOrder(self.matchCaseCheck, self.entireWordsCheck)
        Dialog.setTabOrder(self.entireWordsCheck, self.backwardsCheck)
        Dialog.setTabOrder(self.backwardsCheck, self.wrapCheck)
        Dialog.setTabOrder(self.wrapCheck, self.regexCheck)
        Dialog.setTabOrder(self.regexCheck, self.replaceButton)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "&Search for:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Replace &with:", None, QtGui.QApplication.UnicodeUTF8))
        self.matchCaseCheck.setText(QtGui.QApplication.translate("Dialog", "Match case", None, QtGui.QApplication.UnicodeUTF8))
        self.entireWordsCheck.setText(QtGui.QApplication.translate("Dialog", "Match entire words only", None, QtGui.QApplication.UnicodeUTF8))
        self.backwardsCheck.setText(QtGui.QApplication.translate("Dialog", "Search backwards", None, QtGui.QApplication.UnicodeUTF8))
        self.wrapCheck.setText(QtGui.QApplication.translate("Dialog", "Wrap around", None, QtGui.QApplication.UnicodeUTF8))
        self.regexCheck.setText(QtGui.QApplication.translate("Dialog", "Search string is a regular expression", None, QtGui.QApplication.UnicodeUTF8))
        self.findButton.setText(QtGui.QApplication.translate("Dialog", "&Find", None, QtGui.QApplication.UnicodeUTF8))
        self.replaceButton.setText(QtGui.QApplication.translate("Dialog", "&Replace", None, QtGui.QApplication.UnicodeUTF8))
        self.replaceAllButton.setText(QtGui.QApplication.translate("Dialog", "Replace &All", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("Dialog", "&Close", None, QtGui.QApplication.UnicodeUTF8))

