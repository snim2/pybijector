from PyQt4 import Qt

#
# Based loosely on the PyQt wiki page:
#
# http://diotavelli.net/PyQtWiki/Capturing_Output_from_a_Process
#
# Edited by: Mathias Helminger, DavidBoddie, 193, cm-62
#

class Lint(Qt.QWidget):
    def __init__(self, lint):
    
        Qt.QWidget.__init__(self)

        self.lint = lint
        self.process = Qt.QProcess()

        self.connect(self.process, Qt.SIGNAL("finished(int)"), self.finished)
        self.connect(self.process, Qt.SIGNAL("readyReadStderr()"), self.readErrors)

        self.results = None
        self.errors = None
        return
        
    def start(self, filename, args):
        self.results = None
        self.errors = None
        lint_args = args + [filename]
        self.process.start(self.lint, lint_args)
        return

    def finished(self, exit_status):
        self.readOutput()
        return

    def readOutput(self):
        self.results = self.process.readAllStandardOutput()
        self.emit(Qt.SIGNAL("results()"))
        return
    
    def readErrors(self):
        self.errors = self.process.readLineStderr()
        return

