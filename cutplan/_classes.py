from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
from cutplan._gui import LogPlotGUI
from cutplan.__init__ import CPSchedule


class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, df=pd.DataFrame(), parent=None, completed=None):
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df
        if completed is None:
            self._completed = [False]*df.shape[0]
        else:
            self._completed = completed

    def setCompleted(self, id, val=True):
        self._completed[id] = val

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df.index.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.FontRole:
            font = QtGui.QFont()
            font.setBold(self._completed[index.row()])
            return QtCore.QVariant(font)
        elif role == QtCore.Qt.TextAlignmentRole and index.column() != 0:
            return QtCore.QVariant(
                QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        elif role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if not index.isValid():
            return QtCore.QVariant()

        return QtCore.QVariant(str(self._df.iloc[index.row(), index.column()]))

    def setData(self, index, value, role):
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self._df.set_value(row, col, value)
        return True

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.columns)

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(
            colname,
            ascending=(order == QtCore.Qt.AscendingOrder),
            inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()


class MayaviQWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, schedule=None, LDDir=""):
        super(QtWidgets.QWidget, self).__init__(parent)
        SchedDir = "000.dat"
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        if schedule is None:
            self.CPSched = CPSchedule(SchedDir, LDDir)
        else:
            self.CPSched = schedule
        self.LogPlotter = LogPlotGUI(self.CPSched, LDDir)

        self.ui = self.LogPlotter.edit_traits(
            parent=self, kind='subpanel').control
        self.layout.addWidget(self.ui)
        self.setLayout(self.layout)


class CA_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, ui=None):
        super(CA_MainWindow, self).__init__(parent)
        self.ui = ui

    def setUI(self, ui):
        self.ui = ui

    def closeEvent(self, e):
        quit_msg = "Are you sure you want to exit?"
        if self.ui.CPRunning:
            reply = QtWidgets.QMessageBox.question(
                self, 'Simulation still running...', quit_msg,
                QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:
                self.ui.SaveFunction()
                e.accept()
            else:
                e.ignore()
        else:
            self.ui.SaveFunction()
            e.accept()
