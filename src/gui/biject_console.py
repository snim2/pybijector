from PyQt4 import Qt

#
# Based on the PyQt wiki page:
#
# http://diotavelli.net/PyQtWiki/Capturing_Output_from_a_Process
#
# Edited by: Mathias Helminger, DavidBoddie, 193, cm-62
#

class Console(Qt.QWidget):
    def __init__(self, textBrowser, lineEdit, ok, abort, reset, get_filename):
    
        Qt.QWidget.__init__(self)

        # Should be a callable.
        self.get_filename = get_filename
        
        self.textBrowser = textBrowser
#        self.textBrowser.setTextFormat(Qt.QTextBrowser.LogText)
        self.lineEdit = lineEdit
        self.startButton = ok
        self.startButton.setText('Start')
        self.stopButton = abort
        self.stopButton.setEnabled(False)
        self.resetButton = reset

        self.connect(self.lineEdit, Qt.SIGNAL("returnPressed()"), self.startCommand)
        self.connect(self.startButton, Qt.SIGNAL("clicked()"), self.startCommand)
        self.connect(self.stopButton, Qt.SIGNAL("clicked()"), self.stopCommand)
        self.connect(self.resetButton, Qt.SIGNAL("clicked()"), self.resetCommand)

        self.process = Qt.QProcess()
        self.connect(self.process, Qt.SIGNAL("readyReadStdout()"), self.readOutput)
        self.connect(self.process, Qt.SIGNAL("readyReadStderr()"), self.readErrors)
        self.connect(self.process, Qt.SIGNAL("processExited()"), self.resetButtons)

    def startCommand(self):
        self.process.setArguments(Qt.QString.split(" ", self.lineEdit.text()))
        self.process.closeStdin()
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.textBrowser.clear()
        
        if not self.process.start():
            self.textBrowser.setText(
                Qt.QString("*** Failed to run %1 ***").arg(self.lineEdit.text())
                )
            self.resetButtons()
        return

    def stopCommand(self):
        self.resetButtons()
        self.process.tryTerminate()
        Qt.QTimer.singleShot(5000, self.process, Qt.SLOT("kill()"))
        return
        
    def resetCommand(self):
        self.stopCommand()
        self.textBrowser.clear()
        return

    def readOutput(self):
        self.textBrowser.append(Qt.QString(self.process.readStdout()))
        return
    
    def readErrors(self):
        self.textBrowser.append("error: " + Qt.QString(self.process.readLineStderr()))
        return

    def resetButtons(self):
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.resetButton.setEnabled(True)
        return
