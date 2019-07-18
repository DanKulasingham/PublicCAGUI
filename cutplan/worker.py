from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class Worker(QObject):
    finished = pyqtSignal()
    intReady = pyqtSignal(int)

    @pyqtSlot()
    def procCounter(self):  # A slot takes no params
        for i in range(1, 100):
            self.intReady.emit(i)

        self.finished.emit()
