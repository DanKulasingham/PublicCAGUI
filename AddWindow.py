# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CAGUI-AddCutplanUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from cutplan._classes import PandasModel
from os import system as ossystem
import pyodbc as sql
import pandas as pd
import datetime as dt


class AddWindow(object):
    def setupUi(self, Dialog, sqlfile=None, host=None):
        self.chosen = None

        # SQL
        if sqlfile is None:
            self.sqlfile = "support\\cpquery.sql"
        else:
            self.sqlfile = sqlfile

        # Host server
        if host is None:
            self.host = '192.168.3.55'
        else:
            self.host = host

        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.conn = sql.connect(
            'Driver={SQL Server};'
            'Server='+self.host+';'
            'Database=SequalLogScanner;'
            'UID=sa;'
            'PWD=gg8976@;'
        )
        QtWidgets.QApplication.restoreOverrideCursor()

        Dialog.setObjectName("Dialog")
        Dialog.resize(575, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableView = QtWidgets.QTableView(Dialog)
        self.tableView.setObjectName("tableView")
        self.horizontalLayout.addWidget(self.tableView)
        self.calendarWidget = QtWidgets.QCalendarWidget(Dialog)
        self.calendarWidget.setMaximumSize(QtCore.QSize(200, 16777215))
        self.calendarWidget.setObjectName("calendarWidget")
        self.horizontalLayout.addWidget(self.calendarWidget)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.on_Date()

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.calendarWidget.clicked[QtCore.QDate].connect(self.on_Date)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def on_Date(self, date=None):
        f = open(self.sqlfile, 'r')
        sqltext = f.read()

        date = self.calendarWidget.selectedDate().toPyDate()
        date1 = dt.datetime(date.year, date.month, date.day, 4)
        date1 = date1 + dt.timedelta(days=1)

        sqltext = sqltext.replace("@datenow", "'"+str(date1)+"'")

        self.data = pd.read_sql(sqltext, self.conn)

        self.TVSetUp()

    def TVSetUp(self):
        self.pdModel = PandasModel(
            self.data[['CutplanID', 'Description', 'LogCount']]
        )
        self.tableView.setModel(self.pdModel)
        self.tableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.tableView.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.tableView.verticalHeader().setVisible(False)
        selModel = self.tableView.selectionModel()
        self.on_idChange()
        selModel.selectionChanged.connect(self.on_idChange)

    def on_idChange(self):
        selected = self.tableView.selectionModel().selectedRows()
        if len(selected) == 0:
            self.tableView.selectRow(0)
            self.id = 0
            self.chosen = self.data.CutplanID[0]
        else:
            self.id = selected[0].row()
            self.chosen = self.data.CutplanID[self.id]

    def ping(self):
        response = ossystem("ping -c 1 " + self.host)

        if response == 0:
            pingstatus = "Network Active"
        else:
            pingstatus = "Network Error"

        return pingstatus

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Choose cutplan to add:"))
        header = self.tableView.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     Dialog = QtWidgets.QDialog()
#     ui = AddWindow()
#     ui.setupUi(Dialog)
#     Dialog.show()
#     sys.exit(app.exec_())
