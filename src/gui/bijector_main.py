# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/bijector_main.ui'
#
# Created: Thu Apr 28 15:08:19 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(926, 600)
        MainWindow.setDockOptions(QtGui.QMainWindow.AllowTabbedDocks|QtGui.QMainWindow.AnimatedDocks|QtGui.QMainWindow.ForceTabbedDocks|QtGui.QMainWindow.VerticalTabs)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter_2 = QtGui.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.splitter = QtGui.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.threadEdit = Qsci.QsciScintilla(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.threadEdit.sizePolicy().hasHeightForWidth())
        self.threadEdit.setSizePolicy(sizePolicy)
        self.threadEdit.setToolTip(_fromUtf8(""))
        self.threadEdit.setWhatsThis(_fromUtf8(""))
        self.threadEdit.setObjectName(_fromUtf8("threadEdit"))
        self.cspEdit = Qsci.QsciScintilla(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cspEdit.sizePolicy().hasHeightForWidth())
        self.cspEdit.setSizePolicy(sizePolicy)
        self.cspEdit.setToolTip(_fromUtf8(""))
        self.cspEdit.setWhatsThis(_fromUtf8(""))
        self.cspEdit.setObjectName(_fromUtf8("cspEdit"))
        self.consoleTabs = QtGui.QTabWidget(self.splitter_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.consoleTabs.sizePolicy().hasHeightForWidth())
        self.consoleTabs.setSizePolicy(sizePolicy)
        self.consoleTabs.setTabPosition(QtGui.QTabWidget.North)
        self.consoleTabs.setElideMode(QtCore.Qt.ElideNone)
        self.consoleTabs.setObjectName(_fromUtf8("consoleTabs"))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.tab_3)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.pythonConsole = QtGui.QTextBrowser(self.tab_3)
        self.pythonConsole.setObjectName(_fromUtf8("pythonConsole"))
        self.verticalLayout_4.addWidget(self.pythonConsole)
        self.lineEdit_3 = QtGui.QLineEdit(self.tab_3)
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.verticalLayout_4.addWidget(self.lineEdit_3)
        self.consoleTabs.addTab(self.tab_3, _fromUtf8(""))
        self.tab_5 = QtGui.QWidget()
        self.tab_5.setObjectName(_fromUtf8("tab_5"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.tab_5)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.cspConsole = QtGui.QTextBrowser(self.tab_5)
        self.cspConsole.setObjectName(_fromUtf8("cspConsole"))
        self.verticalLayout_6.addWidget(self.cspConsole)
        self.buttonBox = QtGui.QDialogButtonBox(self.tab_5)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Abort|QtGui.QDialogButtonBox.Reset)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_6.addWidget(self.buttonBox)
        self.consoleTabs.addTab(self.tab_5, _fromUtf8(""))
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName(_fromUtf8("tab_4"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.tab_4)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.buttonBox_2 = QtGui.QDialogButtonBox(self.tab_4)
        self.buttonBox_2.setStandardButtons(QtGui.QDialogButtonBox.Abort|QtGui.QDialogButtonBox.Reset)
        self.buttonBox_2.setObjectName(_fromUtf8("buttonBox_2"))
        self.verticalLayout_5.addWidget(self.buttonBox_2)
        self.threadConsole = QtGui.QTextBrowser(self.tab_4)
        self.threadConsole.setObjectName(_fromUtf8("threadConsole"))
        self.verticalLayout_5.addWidget(self.threadConsole)
        self.consoleTabs.addTab(self.tab_4, _fromUtf8(""))
        self.gridLayout.addWidget(self.splitter_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 926, 26))
        self.menubar.setNativeMenuBar(False)
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menu_Recent_Files = QtGui.QMenu(self.menuFile)
        self.menu_Recent_Files.setObjectName(_fromUtf8("menu_Recent_Files"))
        self.menu_Help = QtGui.QMenu(self.menubar)
        self.menu_Help.setObjectName(_fromUtf8("menu_Help"))
        self.menu_Edit = QtGui.QMenu(self.menubar)
        self.menu_Edit.setObjectName(_fromUtf8("menu_Edit"))
        self.menuBijector = QtGui.QMenu(self.menubar)
        self.menuBijector.setObjectName(_fromUtf8("menuBijector"))
        self.menuSource = QtGui.QMenu(self.menubar)
        self.menuSource.setObjectName(_fromUtf8("menuSource"))
        self.menu_Run = QtGui.QMenu(self.menubar)
        self.menu_Run.setObjectName(_fromUtf8("menu_Run"))
        self.menuWindow = QtGui.QMenu(self.menubar)
        self.menuWindow.setObjectName(_fromUtf8("menuWindow"))
        self.menuSearch = QtGui.QMenu(self.menubar)
        self.menuSearch.setObjectName(_fromUtf8("menuSearch"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.action_Open_File = QtGui.QAction(MainWindow)
        self.action_Open_File.setObjectName(_fromUtf8("action_Open_File"))
        self.action_New_File = QtGui.QAction(MainWindow)
        self.action_New_File.setObjectName(_fromUtf8("action_New_File"))
        self.action_Save_File = QtGui.QAction(MainWindow)
        self.action_Save_File.setObjectName(_fromUtf8("action_Save_File"))
        self.action_Save_File_As = QtGui.QAction(MainWindow)
        self.action_Save_File_As.setObjectName(_fromUtf8("action_Save_File_As"))
        self.action_Print_File = QtGui.QAction(MainWindow)
        self.action_Print_File.setObjectName(_fromUtf8("action_Print_File"))
        self.action_Close_File = QtGui.QAction(MainWindow)
        self.action_Close_File.setObjectName(_fromUtf8("action_Close_File"))
        self.action_Quit = QtGui.QAction(MainWindow)
        self.action_Quit.setObjectName(_fromUtf8("action_Quit"))
        self.action_About_Help = QtGui.QAction(MainWindow)
        self.action_About_Help.setObjectName(_fromUtf8("action_About_Help"))
        self.action_Undo_Edit = QtGui.QAction(MainWindow)
        self.action_Undo_Edit.setObjectName(_fromUtf8("action_Undo_Edit"))
        self.action_Redo_Edit = QtGui.QAction(MainWindow)
        self.action_Redo_Edit.setObjectName(_fromUtf8("action_Redo_Edit"))
        self.action_Cut_Edit = QtGui.QAction(MainWindow)
        self.action_Cut_Edit.setObjectName(_fromUtf8("action_Cut_Edit"))
        self.action_Copy_Edit = QtGui.QAction(MainWindow)
        self.action_Copy_Edit.setObjectName(_fromUtf8("action_Copy_Edit"))
        self.action_Paste_Edit = QtGui.QAction(MainWindow)
        self.action_Paste_Edit.setObjectName(_fromUtf8("action_Paste_Edit"))
        self.action_Select_All_Edit = QtGui.QAction(MainWindow)
        self.action_Select_All_Edit.setObjectName(_fromUtf8("action_Select_All_Edit"))
        self.action_Convert_to_CSP_Bijector = QtGui.QAction(MainWindow)
        self.action_Convert_to_CSP_Bijector.setObjectName(_fromUtf8("action_Convert_to_CSP_Bijector"))
        self.action_Convert_to_Threads_Bijector = QtGui.QAction(MainWindow)
        self.action_Convert_to_Threads_Bijector.setObjectName(_fromUtf8("action_Convert_to_Threads_Bijector"))
        self.action_Folding_Mode_Source = QtGui.QAction(MainWindow)
        self.action_Folding_Mode_Source.setCheckable(True)
        self.action_Folding_Mode_Source.setObjectName(_fromUtf8("action_Folding_Mode_Source"))
        self.action_Fold_All_Source = QtGui.QAction(MainWindow)
        self.action_Fold_All_Source.setObjectName(_fromUtf8("action_Fold_All_Source"))
        self.action_Whitespace_Visible_Source = QtGui.QAction(MainWindow)
        self.action_Whitespace_Visible_Source.setCheckable(True)
        self.action_Whitespace_Visible_Source.setObjectName(_fromUtf8("action_Whitespace_Visible_Source"))
        self.action_Word_Wrap_Source = QtGui.QAction(MainWindow)
        self.action_Word_Wrap_Source.setCheckable(True)
        self.action_Word_Wrap_Source.setObjectName(_fromUtf8("action_Word_Wrap_Source"))
        self.action_Indent_Selection_Source = QtGui.QAction(MainWindow)
        self.action_Indent_Selection_Source.setObjectName(_fromUtf8("action_Indent_Selection_Source"))
        self.action_Unindent_Selection_Source = QtGui.QAction(MainWindow)
        self.action_Unindent_Selection_Source.setObjectName(_fromUtf8("action_Unindent_Selection_Source"))
        self.action_Run_Threaded_Code_Run = QtGui.QAction(MainWindow)
        self.action_Run_Threaded_Code_Run.setObjectName(_fromUtf8("action_Run_Threaded_Code_Run"))
        self.action_Run_CSP_Code_Run = QtGui.QAction(MainWindow)
        self.action_Run_CSP_Code_Run.setObjectName(_fromUtf8("action_Run_CSP_Code_Run"))
        self.action_Debug_Threaded_Code_Run = QtGui.QAction(MainWindow)
        self.action_Debug_Threaded_Code_Run.setObjectName(_fromUtf8("action_Debug_Threaded_Code_Run"))
        self.action_Debug_CSP_Code_Run = QtGui.QAction(MainWindow)
        self.action_Debug_CSP_Code_Run.setObjectName(_fromUtf8("action_Debug_CSP_Code_Run"))
        self.action_Remove_All_Folds_Source = QtGui.QAction(MainWindow)
        self.action_Remove_All_Folds_Source.setObjectName(_fromUtf8("action_Remove_All_Folds_Source"))
        self.action_Clear_All_Breakpoints_Run = QtGui.QAction(MainWindow)
        self.action_Clear_All_Breakpoints_Run.setObjectName(_fromUtf8("action_Clear_All_Breakpoints_Run"))
        self.action_Toggle_Console_Window = QtGui.QAction(MainWindow)
        self.action_Toggle_Console_Window.setCheckable(True)
        self.action_Toggle_Console_Window.setObjectName(_fromUtf8("action_Toggle_Console_Window"))
        self.action_Threaded_Code_Editor = QtGui.QAction(MainWindow)
        self.action_Threaded_Code_Editor.setObjectName(_fromUtf8("action_Threaded_Code_Editor"))
        self.action_Python_CSP_Code_Editor = QtGui.QAction(MainWindow)
        self.action_Python_CSP_Code_Editor.setObjectName(_fromUtf8("action_Python_CSP_Code_Editor"))
        self.action_Consoles_Windows = QtGui.QAction(MainWindow)
        self.action_Consoles_Windows.setObjectName(_fromUtf8("action_Consoles_Windows"))
        self.action_Find_Search = QtGui.QAction(MainWindow)
        self.action_Find_Search.setObjectName(_fromUtf8("action_Find_Search"))
        self.action_Find_Next_Search = QtGui.QAction(MainWindow)
        self.action_Find_Next_Search.setObjectName(_fromUtf8("action_Find_Next_Search"))
        self.action_Find_Previous_Search = QtGui.QAction(MainWindow)
        self.action_Find_Previous_Search.setObjectName(_fromUtf8("action_Find_Previous_Search"))
        self.action_Goto_Line_Search = QtGui.QAction(MainWindow)
        self.action_Goto_Line_Search.setObjectName(_fromUtf8("action_Goto_Line_Search"))
        self.action_Replace_Search = QtGui.QAction(MainWindow)
        self.action_Replace_Search.setObjectName(_fromUtf8("action_Replace_Search"))
        self.action_Clear_Menu_Files = QtGui.QAction(MainWindow)
        self.action_Clear_Menu_Files.setObjectName(_fromUtf8("action_Clear_Menu_Files"))
        self.action_Zoom_In_View = QtGui.QAction(MainWindow)
        self.action_Zoom_In_View.setObjectName(_fromUtf8("action_Zoom_In_View"))
        self.action_Zoom_Out_View = QtGui.QAction(MainWindow)
        self.action_Zoom_Out_View.setObjectName(_fromUtf8("action_Zoom_Out_View"))
        self.menu_Recent_Files.addSeparator()
        self.menu_Recent_Files.addAction(self.action_Clear_Menu_Files)
        self.menuFile.addAction(self.action_New_File)
        self.menuFile.addAction(self.action_Open_File)
        self.menuFile.addAction(self.menu_Recent_Files.menuAction())
        self.menuFile.addAction(self.action_Save_File)
        self.menuFile.addAction(self.action_Save_File_As)
        self.menuFile.addAction(self.action_Print_File)
        self.menuFile.addAction(self.action_Close_File)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.action_Quit)
        self.menu_Help.addSeparator()
        self.menu_Help.addAction(self.action_About_Help)
        self.menu_Edit.addAction(self.action_Undo_Edit)
        self.menu_Edit.addAction(self.action_Redo_Edit)
        self.menu_Edit.addAction(self.action_Cut_Edit)
        self.menu_Edit.addAction(self.action_Copy_Edit)
        self.menu_Edit.addAction(self.action_Paste_Edit)
        self.menu_Edit.addSeparator()
        self.menu_Edit.addAction(self.action_Select_All_Edit)
        self.menuBijector.addAction(self.action_Convert_to_CSP_Bijector)
        self.menuBijector.addAction(self.action_Convert_to_Threads_Bijector)
        self.menuSource.addAction(self.action_Folding_Mode_Source)
        self.menuSource.addAction(self.action_Fold_All_Source)
        self.menuSource.addAction(self.action_Remove_All_Folds_Source)
        self.menuSource.addSeparator()
        self.menuSource.addAction(self.action_Whitespace_Visible_Source)
        self.menuSource.addSeparator()
        self.menuSource.addAction(self.action_Word_Wrap_Source)
        self.menuSource.addSeparator()
        self.menuSource.addAction(self.action_Indent_Selection_Source)
        self.menuSource.addAction(self.action_Unindent_Selection_Source)
        self.menu_Run.addAction(self.action_Run_Threaded_Code_Run)
        self.menu_Run.addAction(self.action_Run_CSP_Code_Run)
        self.menu_Run.addSeparator()
        self.menu_Run.addAction(self.action_Clear_All_Breakpoints_Run)
        self.menu_Run.addSeparator()
        self.menu_Run.addAction(self.action_Debug_Threaded_Code_Run)
        self.menu_Run.addAction(self.action_Debug_CSP_Code_Run)
        self.menuWindow.addAction(self.action_Threaded_Code_Editor)
        self.menuWindow.addAction(self.action_Python_CSP_Code_Editor)
        self.menuWindow.addAction(self.action_Consoles_Windows)
        self.menuWindow.addSeparator()
        self.menuWindow.addAction(self.action_Toggle_Console_Window)
        self.menuWindow.addSeparator()
        self.menuWindow.addAction(self.action_Zoom_In_View)
        self.menuWindow.addAction(self.action_Zoom_Out_View)
        self.menuSearch.addAction(self.action_Find_Search)
        self.menuSearch.addAction(self.action_Find_Next_Search)
        self.menuSearch.addAction(self.action_Find_Previous_Search)
        self.menuSearch.addSeparator()
        self.menuSearch.addAction(self.action_Replace_Search)
        self.menuSearch.addSeparator()
        self.menuSearch.addAction(self.action_Goto_Line_Search)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menu_Edit.menuAction())
        self.menubar.addAction(self.menuWindow.menuAction())
        self.menubar.addAction(self.menuSearch.menuAction())
        self.menubar.addAction(self.menuSource.menuAction())
        self.menubar.addAction(self.menu_Run.menuAction())
        self.menubar.addAction(self.menuBijector.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())
        self.toolBar.addAction(self.action_Open_File)
        self.toolBar.addAction(self.action_New_File)
        self.toolBar.addAction(self.action_Save_File)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_Undo_Edit)
        self.toolBar.addAction(self.action_Redo_Edit)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_Convert_to_CSP_Bijector)
        self.toolBar.addAction(self.action_Convert_to_Threads_Bijector)

        self.retranslateUi(MainWindow)
        self.consoleTabs.setCurrentIndex(1)
        QtCore.QObject.connect(self.action_Open_File, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.load_file)
        QtCore.QObject.connect(self.action_New_File, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.new_file)
        QtCore.QObject.connect(self.action_About_Help, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.about)
        QtCore.QObject.connect(self.action_Close_File, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.close_file)
        QtCore.QObject.connect(self.action_Print_File, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.print_file)
        QtCore.QObject.connect(self.action_Quit, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.close)
        QtCore.QObject.connect(self.action_Save_File, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.save_file)
        QtCore.QObject.connect(self.action_Save_File_As, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.save_as_file)
        QtCore.QObject.connect(self.action_Convert_to_CSP_Bijector, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.to_csp)
        QtCore.QObject.connect(self.action_Convert_to_Threads_Bijector, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.to_threads)
        QtCore.QObject.connect(self.action_Copy_Edit, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.copy)
        QtCore.QObject.connect(self.action_Cut_Edit, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.cut)
        QtCore.QObject.connect(self.action_Paste_Edit, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.paste)
        QtCore.QObject.connect(self.action_Redo_Edit, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.redo)
        QtCore.QObject.connect(self.action_Select_All_Edit, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.selectAll)
        QtCore.QObject.connect(self.action_Undo_Edit, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.undo)
        QtCore.QObject.connect(self.action_Fold_All_Source, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.foldAll)
        QtCore.QObject.connect(self.action_Indent_Selection_Source, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.indent_selection)
        QtCore.QObject.connect(self.action_Folding_Mode_Source, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.toggle_folding_mode)
        QtCore.QObject.connect(self.action_Word_Wrap_Source, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.toggle_word_wrap)
        QtCore.QObject.connect(self.action_Unindent_Selection_Source, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.unindent_selection)
        QtCore.QObject.connect(self.action_Whitespace_Visible_Source, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.toggle_whitespace_visible)
        QtCore.QObject.connect(self.action_Run_CSP_Code_Run, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.run_csp)
        QtCore.QObject.connect(self.action_Run_Threaded_Code_Run, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.run_threads)
        QtCore.QObject.connect(self.action_Debug_CSP_Code_Run, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.debug_csp)
        QtCore.QObject.connect(self.action_Debug_Threaded_Code_Run, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.debug_threads)
        QtCore.QObject.connect(self.action_Remove_All_Folds_Source, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.clearFolds)
        QtCore.QObject.connect(self.action_Clear_All_Breakpoints_Run, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.remove_all_breakpoints)
        QtCore.QObject.connect(self.action_Toggle_Console_Window, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.toggle_console)
        QtCore.QObject.connect(self.action_Threaded_Code_Editor, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.focus_threads)
        QtCore.QObject.connect(self.action_Python_CSP_Code_Editor, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.focus_csp)
        QtCore.QObject.connect(self.action_Consoles_Windows, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.focus_console)
        QtCore.QObject.connect(self.action_Find_Search, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.find)
        QtCore.QObject.connect(self.action_Find_Next_Search, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.find_next)
        QtCore.QObject.connect(self.action_Find_Previous_Search, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.find_previous)
        QtCore.QObject.connect(self.action_Replace_Search, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.replace)
        QtCore.QObject.connect(self.action_Goto_Line_Search, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.goto_line)
        QtCore.QObject.connect(self.action_Clear_Menu_Files, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.clear_recent_files)
        QtCore.QObject.connect(self.action_Zoom_In_View, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.zoomIn)
        QtCore.QObject.connect(self.action_Zoom_Out_View, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.zoomOut)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.consoleTabs.setTabText(self.consoleTabs.indexOf(self.tab_3), QtGui.QApplication.translate("MainWindow", "Python interpreter", None, QtGui.QApplication.UnicodeUTF8))
        self.consoleTabs.setTabText(self.consoleTabs.indexOf(self.tab_5), QtGui.QApplication.translate("MainWindow", "CSP code console", None, QtGui.QApplication.UnicodeUTF8))
        self.consoleTabs.setTabText(self.consoleTabs.indexOf(self.tab_4), QtGui.QApplication.translate("MainWindow", "Threaded code console", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Recent_Files.setTitle(QtGui.QApplication.translate("MainWindow", "&Recent Files", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Help.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Edit.setTitle(QtGui.QApplication.translate("MainWindow", "&Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuBijector.setTitle(QtGui.QApplication.translate("MainWindow", "Bijector", None, QtGui.QApplication.UnicodeUTF8))
        self.menuSource.setTitle(QtGui.QApplication.translate("MainWindow", "&Source", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Run.setTitle(QtGui.QApplication.translate("MainWindow", "&Run", None, QtGui.QApplication.UnicodeUTF8))
        self.menuWindow.setTitle(QtGui.QApplication.translate("MainWindow", "View", None, QtGui.QApplication.UnicodeUTF8))
        self.menuSearch.setTitle(QtGui.QApplication.translate("MainWindow", "Search", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open_File.setText(QtGui.QApplication.translate("MainWindow", "&Open File", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open_File.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.action_New_File.setText(QtGui.QApplication.translate("MainWindow", "&New File", None, QtGui.QApplication.UnicodeUTF8))
        self.action_New_File.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Save_File.setText(QtGui.QApplication.translate("MainWindow", "&Save File", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Save_File.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Save_File_As.setText(QtGui.QApplication.translate("MainWindow", "Save File &As", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Print_File.setText(QtGui.QApplication.translate("MainWindow", "&Print File", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Print_File.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+P", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Close_File.setText(QtGui.QApplication.translate("MainWindow", "&Close File", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Close_File.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+W", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setText(QtGui.QApplication.translate("MainWindow", "&Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.action_About_Help.setText(QtGui.QApplication.translate("MainWindow", "&About", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Undo_Edit.setText(QtGui.QApplication.translate("MainWindow", "&Undo", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Undo_Edit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+U", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Redo_Edit.setText(QtGui.QApplication.translate("MainWindow", "&Redo", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Redo_Edit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+R", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Cut_Edit.setText(QtGui.QApplication.translate("MainWindow", "Cu&t", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Cut_Edit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+X", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Copy_Edit.setText(QtGui.QApplication.translate("MainWindow", "&Copy", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Copy_Edit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+C", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Paste_Edit.setText(QtGui.QApplication.translate("MainWindow", "&Paste", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Paste_Edit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+V", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Select_All_Edit.setText(QtGui.QApplication.translate("MainWindow", "Select &All", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Select_All_Edit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+A", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Convert_to_CSP_Bijector.setText(QtGui.QApplication.translate("MainWindow", "Convert to &CSP", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Convert_to_Threads_Bijector.setText(QtGui.QApplication.translate("MainWindow", "Convert to &Threads", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Folding_Mode_Source.setText(QtGui.QApplication.translate("MainWindow", "Folding Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Folding_Mode_Source.setToolTip(QtGui.QApplication.translate("MainWindow", "Allow indented blocks to be folded and unfolded", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Fold_All_Source.setText(QtGui.QApplication.translate("MainWindow", "Fold All", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Fold_All_Source.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Shift+F", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Whitespace_Visible_Source.setText(QtGui.QApplication.translate("MainWindow", "Make Whitespace Visible", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Whitespace_Visible_Source.setToolTip(QtGui.QApplication.translate("MainWindow", "Make whitespace visible", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Word_Wrap_Source.setText(QtGui.QApplication.translate("MainWindow", "Word Wrap", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Word_Wrap_Source.setToolTip(QtGui.QApplication.translate("MainWindow", "Word wrap long lines", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Indent_Selection_Source.setText(QtGui.QApplication.translate("MainWindow", "Indent Selection", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Indent_Selection_Source.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Right", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Unindent_Selection_Source.setText(QtGui.QApplication.translate("MainWindow", "Unindent Selection", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Unindent_Selection_Source.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Left", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Run_Threaded_Code_Run.setText(QtGui.QApplication.translate("MainWindow", "Run Threaded Code", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Run_Threaded_Code_Run.setShortcut(QtGui.QApplication.translate("MainWindow", "F4", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Run_CSP_Code_Run.setText(QtGui.QApplication.translate("MainWindow", "Run CSP Code", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Run_CSP_Code_Run.setShortcut(QtGui.QApplication.translate("MainWindow", "F5", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Debug_Threaded_Code_Run.setText(QtGui.QApplication.translate("MainWindow", "Debug Threaded Code", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Debug_Threaded_Code_Run.setShortcut(QtGui.QApplication.translate("MainWindow", "F6", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Debug_CSP_Code_Run.setText(QtGui.QApplication.translate("MainWindow", "Debug CSP Code", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Debug_CSP_Code_Run.setShortcut(QtGui.QApplication.translate("MainWindow", "F7", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Remove_All_Folds_Source.setText(QtGui.QApplication.translate("MainWindow", "Remove All Folds", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Clear_All_Breakpoints_Run.setText(QtGui.QApplication.translate("MainWindow", "Clear All Breakpoints", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Clear_All_Breakpoints_Run.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+B", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Toggle_Console_Window.setText(QtGui.QApplication.translate("MainWindow", "Show Consoles", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Toggle_Console_Window.setToolTip(QtGui.QApplication.translate("MainWindow", "Show / hide consoles", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Toggle_Console_Window.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+T", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Threaded_Code_Editor.setText(QtGui.QApplication.translate("MainWindow", "Threaded Code Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Threaded_Code_Editor.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+1", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Python_CSP_Code_Editor.setText(QtGui.QApplication.translate("MainWindow", "python-csp Code Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Python_CSP_Code_Editor.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+2", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Consoles_Windows.setText(QtGui.QApplication.translate("MainWindow", "Consoles", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Consoles_Windows.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+3", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Find_Search.setText(QtGui.QApplication.translate("MainWindow", "&Find", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Find_Search.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+F", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Find_Next_Search.setText(QtGui.QApplication.translate("MainWindow", "Find &Next", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Find_Next_Search.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+G", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Find_Previous_Search.setText(QtGui.QApplication.translate("MainWindow", "Find &Previous", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Find_Previous_Search.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Shift+G", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Goto_Line_Search.setText(QtGui.QApplication.translate("MainWindow", "&Goto Line", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Goto_Line_Search.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+L", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Replace_Search.setText(QtGui.QApplication.translate("MainWindow", "&Replace", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Replace_Search.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+R", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Clear_Menu_Files.setText(QtGui.QApplication.translate("MainWindow", "Clear Menu", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Clear_Menu_Files.setToolTip(QtGui.QApplication.translate("MainWindow", "Clear list of recent files", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Zoom_In_View.setText(QtGui.QApplication.translate("MainWindow", "Zoom &In", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Zoom_In_View.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl++", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Zoom_Out_View.setText(QtGui.QApplication.translate("MainWindow", "Zoom &Out", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Zoom_Out_View.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+-", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import Qsci
