# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CAGUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from AddWindow import AddWindow as AddCPUI
from pickle import load, dump
from os import system as ossystem
from numpy import nanmean, array as nparray
import pandas as pd
import pyodbc as sql
from cutplan._gui import LogPlotGUI
from cutplan.__init__ import CPSchedule
from cutplan._classes import PandasModel, MayaviQWidget, CA_MainWindow


class CAGUI(object):
    def setupUi(self, MainWindow):
        self.host = "192.168.3.55"
        self.LDDir = "data\\"
        self.SettingsUI = None
        self.SettingsDialog = None
        self.id = 0
        self.MainWindow = MainWindow
        self.CPRunning = False
        self.ShowOpt = False
        self.optTxt = "Full"
        self.pieceCount = True

        # CP SCHEDULE
        # self.CPSched = CPSchedule(self.SchedDir, self.LDDir)
        self.LoadFunction()
        self.ready = [False]*self.CPSched.Cutplans.shape[0]
        for i in range(len(self.ready)):
            if self.CPSched.completed[i]:
                self.ready[i] = True
        self.progressCP = sum(self.ready)

        MainWindow.setObjectName("MainWindow")
        MainWindow.setUI(self)
        MainWindow.resize(1100, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap("icons\\CutplanIcon.png"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, -1)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setObjectName("frame")
        self.frameHoriLayout = QtWidgets.QHBoxLayout(self.frame)
        self.frameHoriLayout.setContentsMargins(4, 4, 10, 4)
        self.frameHoriLayout.setSpacing(0)
        self.frameHoriLayout.setObjectName("frameHoriLayout")
        self.menuHoriLayout = QtWidgets.QHBoxLayout()
        self.menuHoriLayout.setContentsMargins(0, 0, 0, 0)
        self.menuHoriLayout.setSpacing(4)
        self.menuHoriLayout.setObjectName("menuHoriLayout")
        self.saveLoadLayout = QtWidgets.QHBoxLayout()
        self.saveLoadLayout.setContentsMargins(0, 0, 0, 0)
        self.saveLoadLayout.setSpacing(0)
        self.saveLoadLayout.setObjectName("saveLoadLayout")
        self.SaveButton = QtWidgets.QToolButton(self.frame)
        self.SaveButton.setMinimumSize(QtCore.QSize(30, 30))
        self.SaveButton.setMaximumSize(QtCore.QSize(30, 30))
        self.SaveButton.setText("")
        self.SaveButton.setToolTip("Save copy of cutplans...")
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap("icons\\save.png"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SaveButton.setIcon(icon)
        self.SaveButton.setObjectName("SaveButton")
        self.saveLoadLayout.addWidget(self.SaveButton)
        self.LoadButton = QtWidgets.QToolButton(self.frame)
        self.LoadButton.setMinimumSize(QtCore.QSize(30, 30))
        self.LoadButton.setMaximumSize(QtCore.QSize(30, 30))
        self.LoadButton.setText("")
        self.LoadButton.setToolTip("Load copy of cutplans...")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap("icons\\open.png"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.LoadButton.setIcon(icon1)
        self.LoadButton.setObjectName("LoadButton")
        self.saveLoadLayout.addWidget(self.LoadButton)
        self.menuHoriLayout.addLayout(self.saveLoadLayout)
        # self.line = QtWidgets.QFrame(self.frame)
        # self.line.setObjectName("line")
        # self.line.setFrameShape(QtWidgets.QFrame.VLine)
        # self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        # self.menuHoriLayout.addWidget(self.line)
        self.RunButton = QtWidgets.QToolButton(self.frame)
        self.RunButton.setMinimumSize(QtCore.QSize(30, 30))
        self.RunButton.setMaximumSize(QtCore.QSize(30, 30))
        self.RunButton.setText("")
        self.RunButton.setToolTip("Simulate cutplans...")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap("icons\\run.png"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.RunButton.setIcon(icon2)
        self.RunButton.setObjectName("RunButton")
        self.menuHoriLayout.addWidget(self.RunButton)
        self.UnitButton = QtWidgets.QToolButton(self.frame)
        self.UnitButton.setMinimumSize(QtCore.QSize(46, 30))
        self.UnitButton.setMaximumSize(QtCore.QSize(46, 30))
        self.UnitButton.setText("")
        self.UnitButton.setToolTip("Show board recovery percentage")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(
            QtGui.QPixmap("icons\\dims2.png"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.UnitButton.setIcon(icon5)
        self.UnitButton.setIconSize(QtCore.QSize(32, 16))
        self.UnitButton.setObjectName("UnitButton")
        self.menuHoriLayout.addWidget(self.UnitButton)
        self.ViewButton = QtWidgets.QToolButton(self.frame)
        self.ViewButton.setMinimumSize(QtCore.QSize(46, 30))
        self.ViewButton.setMaximumSize(QtCore.QSize(46, 30))
        self.ViewButton.setText("")
        self.ViewButton.setToolTip("Show front view")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(
            QtGui.QPixmap("icons\\3dView2.png"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ViewButton.setIcon(icon6)
        self.ViewButton.setIconSize(QtCore.QSize(32, 16))
        self.ViewButton.setObjectName("ViewButton")
        self.menuHoriLayout.addWidget(self.ViewButton)
        self.CameraButton = QtWidgets.QToolButton(self.frame)
        self.CameraButton.setMinimumSize(QtCore.QSize(30, 30))
        self.CameraButton.setMaximumSize(QtCore.QSize(30, 30))
        self.CameraButton.setText("")
        self.CameraButton.setToolTip("Export screenshot of log")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(
            QtGui.QPixmap("icons\\camera.png"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.CameraButton.setIcon(icon7)
        self.CameraButton.setObjectName("CameraButton")
        self.menuHoriLayout.addWidget(self.CameraButton)
        self.UpdateButton = QtWidgets.QToolButton(self.frame)
        self.UpdateButton.setMinimumSize(QtCore.QSize(30, 30))
        self.UpdateButton.setMaximumSize(QtCore.QSize(30, 30))
        self.UpdateButton.setText("")
        self.UpdateButton.setToolTip("Update log data")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(
            QtGui.QPixmap("icons\\update.png"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.UpdateButton.setIcon(icon7)
        self.UpdateButton.setObjectName("UpdateButton")
        self.menuHoriLayout.addWidget(self.UpdateButton)
        self.frameHoriLayout.addLayout(self.menuHoriLayout)
        spacerItem = QtWidgets.QSpacerItem(
            519, 20,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum)
        self.frameHoriLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.frameHoriLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_7.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.frame_2)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.groupBox.setFont(font)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox.setObjectName("checkBox")
        self.checkBox.setChecked(True)
        self.gridLayout_3.addWidget(self.checkBox, 0, 0, 1, 1)
        self.checkBox_2 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout_3.addWidget(self.checkBox_2, 0, 1, 1, 1)
        self.checkBox_3 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_3.setChecked(True)
        self.gridLayout_3.addWidget(self.checkBox_3, 1, 0, 1, 1)
        self.checkBox_4 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_4.setObjectName("checkBox_4")
        self.gridLayout_3.addWidget(self.checkBox_4, 1, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.tableView = QtWidgets.QTableView(self.frame_2)
        self.tableView.setObjectName("tableView")
        self.verticalLayout_2.addWidget(self.tableView)
        self.adddeleteLayout = QtWidgets.QHBoxLayout()
        self.adddeleteLayout.setObjectName("adddeleteLayout")
        spacerItem = QtWidgets.QSpacerItem(
            40, 20,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum)
        self.adddeleteLayout.addItem(spacerItem)
        self.addButton = QtWidgets.QToolButton(self.frame_2)
        self.addButton.setObjectName("addButton")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(
            QtGui.QPixmap("icons\\add.png"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addButton.setIcon(icon3)
        self.adddeleteLayout.addWidget(self.addButton)
        self.deleteButton = QtWidgets.QToolButton(self.frame_2)
        self.deleteButton.setObjectName("deleteButton")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(
            QtGui.QPixmap("icons\\delete.png"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.deleteButton.setIcon(icon4)
        self.adddeleteLayout.addWidget(self.deleteButton)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum)
        self.adddeleteLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.adddeleteLayout)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setContentsMargins(0, 0, -1, -1)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.loadingText = QtWidgets.QLabel(self.frame_2)
        self.loadingText.setObjectName("loadingText")
        self.horizontalLayout_8.addWidget(self.loadingText)
        self.progressBar = QtWidgets.QProgressBar(self.frame_2)
        self.progressBar.setMinimumSize(QtCore.QSize(100, 0))
        self.progressBar.setMaximumSize(QtCore.QSize(10000, 12))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setEnabled(False)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setVisible(False)
        self.horizontalLayout_8.addWidget(self.progressBar)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_7.addLayout(self.verticalLayout_2)

        # MAYAVI WIDGET
        self.widget = MayaviQWidget(self.frame_2, self.CPSched, self.LDDir)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(500, 0))
        self.widget.setObjectName("widget")
        self.horizontalLayout_7.addWidget(self.widget)

        # CUTPLAN ANALYSIS LAYOUT
        self.CA_Layout = QtWidgets.QVBoxLayout()
        self.CA_Layout.setContentsMargins(10, -1, -1, -1)
        self.CA_Layout.setObjectName("CA_Layout")
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding)
        self.CA_Layout.addItem(spacerItem1)
        self.LogsToCutLayout = QtWidgets.QHBoxLayout()
        self.LogsToCutLayout.setObjectName("LogsToCutLayout")
        self.LogsToCut = QtWidgets.QLabel(self.frame_2)
        self.LogsToCut.setObjectName("LogsToCut")
        self.LogsToCutLayout.addWidget(self.LogsToCut)
        self.LogsToCutTB = QtWidgets.QLineEdit(self.frame_2)
        self.LogsToCutTB.setObjectName("LogsToCutTB")
        self.LogsToCutTB.setValidator(QtGui.QIntValidator(
            0, 1000000, self.frame_2
        ))
        self.LogsToCutLayout.addWidget(self.LogsToCutTB)
        self.CA_Layout.addLayout(self.LogsToCutLayout)
        self.CA_GridLayout = QtWidgets.QGridLayout()
        self.CA_GridLayout.setObjectName("CA_GridLayout")
        self.TimberVolumeTB = QtWidgets.QLineEdit(self.frame_2)
        self.TimberVolumeTB.setReadOnly(True)
        self.TimberVolumeTB.setObjectName("TimberVolumeTB")
        self.CA_GridLayout.addWidget(self.TimberVolumeTB, 0, 1, 1, 1)
        self.Recovery = QtWidgets.QLabel(self.frame_2)
        self.Recovery.setObjectName("Recovery")
        self.CA_GridLayout.addWidget(self.Recovery, 0, 2, 1, 1)
        self.RecoveryTB = QtWidgets.QLineEdit(self.frame_2)
        self.RecoveryTB.setReadOnly(True)
        self.RecoveryTB.setObjectName("RecoveryTB")
        self.CA_GridLayout.addWidget(self.RecoveryTB, 0, 3, 1, 1)
        self.TimberVolume = QtWidgets.QLabel(self.frame_2)
        self.TimberVolume.setObjectName("TimberVolume")
        self.CA_GridLayout.addWidget(self.TimberVolume, 0, 0, 1, 1)
        self.SimTimberVolume = QtWidgets.QLabel(self.frame_2)
        self.SimTimberVolume.setObjectName("SimTimberVolume")
        self.CA_GridLayout.addWidget(self.SimTimberVolume, 1, 0, 1, 1)
        self.SimTimberVolumeTB = QtWidgets.QLineEdit(self.frame_2)
        self.SimTimberVolumeTB.setReadOnly(True)
        self.SimTimberVolumeTB.setObjectName("SimTimberVolumeTB")
        self.CA_GridLayout.addWidget(self.SimTimberVolumeTB, 1, 1, 1, 1)
        self.SimRecoveryTB = QtWidgets.QLineEdit(self.frame_2)
        self.SimRecoveryTB.setReadOnly(True)
        self.SimRecoveryTB.setObjectName("SimRecoveryTB")
        self.CA_GridLayout.addWidget(self.SimRecoveryTB, 1, 3, 1, 1)
        self.SimRecovery = QtWidgets.QLabel(self.frame_2)
        self.SimRecovery.setObjectName("SimRecovery")
        self.CA_GridLayout.addWidget(self.SimRecovery, 1, 2, 1, 1)
        self.CA_Layout.addLayout(self.CA_GridLayout)
        self.CutbackTable = QtWidgets.QTableView(self.frame_2)
        self.CutbackTable.setObjectName("CutbackTable")
        font2 = QtGui.QFont()
        font2.setPointSize(8)
        self.CutbackTable.setFont(font2)
        self.CA_Layout.addWidget(self.CutbackTable)

        self.rbHoriLayout = QtWidgets.QHBoxLayout()
        self.rbHoriLayout.setObjectName("rbHoriLayout")
        rbHoriSpacer1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum)
        self.rbHoriLayout.addItem(rbHoriSpacer1)
        self.rbPieceCount = QtWidgets.QRadioButton(self.frame_2)
        self.rbPieceCount.setObjectName("rbPieceCount")
        self.rbHoriLayout.addWidget(self.rbPieceCount)
        self.rbVolume = QtWidgets.QRadioButton(self.frame_2)
        self.rbVolume.setObjectName("rbVolume")
        self.rbHoriLayout.addWidget(self.rbVolume)
        rbHoriSpacer2 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum)
        self.rbHoriLayout.addItem(rbHoriSpacer2)
        self.rbPieceCount.setChecked(True)
        self.CA_Layout.addLayout(self.rbHoriLayout)

        self.OFHoriLayout = QtWidgets.QHBoxLayout()
        self.OFHoriLayout.setObjectName("OFHoriLayout")
        self.OFLabel = QtWidgets.QLabel(self.frame_2)
        self.OFLabel.setObjectName("OFLabel")
        self.OFHoriLayout.addWidget(self.OFLabel)
        self.OFTextBox = QtWidgets.QLineEdit(self.frame_2)
        self.OFLabel.setObjectName("OFTextBox")
        self.OFHoriLayout.addWidget(self.OFTextBox)
        self.checkBox_OF = QtWidgets.QCheckBox(self.frame_2)
        self.checkBox_OF.setObjectName("checkBox_OF")
        self.OFHoriLayout.addWidget(self.checkBox_OF)
        self.CA_Layout.addLayout(self.OFHoriLayout)

        spacerItem2 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding)
        self.CA_Layout.addItem(spacerItem2)
        self.horizontalLayout_7.addLayout(self.CA_Layout)
        self.verticalLayout.addWidget(self.frame_2)
        MainWindow.setCentralWidget(self.centralwidget)

        # TABLEVIEW
        self.TVSetUp()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # CLOCK
        self.timer = QtCore.QTimer(MainWindow)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.displayTime)
        self.timer.start()

        # CHECKBOXES
        self.checkBox.stateChanged.connect(self.on_checkBox)
        self.checkBox_2.stateChanged.connect(self.on_checkBox)
        self.checkBox_3.stateChanged.connect(self.on_checkBox)
        self.checkBox_4.stateChanged.connect(self.on_checkBox)
        self.checkBox_OF.stateChanged.connect(self.on_checkBox)
        if not self.ready[self.id]:
            self.checkBox_2.setEnabled(False)
            self.checkBox_3.setEnabled(False)
            self.checkBox_4.setEnabled(False)

        # BUTTONS
        self.SaveButton.clicked.connect(self.on_Save)
        self.LoadButton.clicked.connect(self.on_Load)
        self.RunButton.clicked.connect(self.on_Run)
        self.UnitButton.clicked.connect(self.on_UnitChange)
        self.ViewButton.clicked.connect(self.on_ViewChange)
        self.CameraButton.clicked.connect(self.on_Screenshot)
        self.addButton.clicked.connect(self.on_AddCP)
        self.deleteButton.clicked.connect(self.on_DeleteCP)
        self.UpdateButton.clicked.connect(self.on_LoadLogs)

        # CA TEXTBOXES
        self.LogsToCutTB.textChanged.connect(self.on_LTC)
        self.TimberVolumeTB.textChanged.connect(self.on_TV)
        self.SimTimberVolumeTB.textChanged.connect(self.on_STV)
        self.EnableAnalysis(self.ready[self.id])

        # CA RADIOBUTTON
        self.rbPieceCount.toggled.connect(self.AnalTVSetUp)

        # KB SHORTCUTS
        self.sc_Save = QtWidgets.QShortcut(
            QtGui.QKeySequence("Ctrl+S"), MainWindow)
        self.sc_Save.activated.connect(self.SaveFunction)
        self.sc_Opt = QtWidgets.QShortcut(
            QtGui.QKeySequence("Ctrl+Shift+O"), MainWindow)
        self.sc_Opt.activated.connect(self.ShowOptimiser)

    def ShowAnalysis(self, init=True):
        if init:
            numLogs = self.CPSched.Cutplans.LogCount[self.id]
            self.LogsToCutTB.setText(str(numLogs))
        else:
            if self.LogsToCutTB.text():
                numLogs = int(self.LogsToCutTB.text())
            else:
                numLogs = 0
        if self.ShowOpt:
            actVol = self.CPSched.ActVol[self.id] / numLogs
        else:
            actVol = self.CPSched.GetTimberVolume(self.id)
        simLV = nanmean(self.CPSched.LogVol[self.id])
        self.TimberVolumeTB.setText("{:.1f} m3".format(actVol * numLogs))
        self.SimTimberVolumeTB.setText("{:.1f} m3".format(simLV * numLogs))

        avgLog = self.CPSched.AverageLog(self.id)
        self.RecoveryTB.setText("{:.1f}%".format((actVol / avgLog.Vol)*100))
        self.SimRecoveryTB.setText("{:.1f}%".format((simLV / avgLog.Vol)*100))

        self.OFTextBox.setText("{:.1f}%".format(
            self.CPSched.OpenFacePerc[self.id]*100))

        self.AnalTVSetUp()

    def ClearAnalysis(self):
        self.LogsToCutTB.setText("")
        self.TimberVolumeTB.setText("")
        self.RecoveryTB.setText("")
        self.SimTimberVolumeTB.setText("")
        self.SimRecoveryTB.setText("")
        self.CutbackTable.setModel(None)

    def on_Screenshot(self):
        defFN = "Screenshot" + str(self.CPSched.Cutplans.CutplanID[self.id])
        file = QtWidgets.QFileDialog.getSaveFileName(
            self.MainWindow, "Save File", defFN,
            filter="Image  file (*.png)")
        if str(file[0]) != "":
            self.widget.LogPlotter.scene.mlab.savefig(filename=file[0])

    def ShowOptimiser(self):
        if self.ShowOpt:
            self.ShowOpt = False
            self.optTxt = "Full"
            if self.ready[self.id]:
                self.ShowAnalysis()
        else:
            self.ShowOpt = True
            self.optTxt = "Optimiser"
            if self.ready[self.id]:
                self.ShowAnalysis()
        self.Recovery.setText(self.optTxt+"\nRecovery:")
        self.TimberVolume.setText(self.optTxt+"\nTimber Volume:")

    def on_UnitChange(self):
        if self.widget.LogPlotter.showPerc:
            self.widget.LogPlotter.showPerc = False
            self.widget.LogPlotter.update_scene()
            icon = QtGui.QIcon()
            icon.addPixmap(
                QtGui.QPixmap("icons\\dims2.png"),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.UnitButton.setIcon(icon)
            self.UnitButton.setIconSize(QtCore.QSize(32, 16))
            self.UnitButton.setToolTip("Show board recovery percentage")
        else:
            self.widget.LogPlotter.showPerc = True
            self.widget.LogPlotter.update_scene()
            icon = QtGui.QIcon()
            icon.addPixmap(
                QtGui.QPixmap("icons\\percent2.png"),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.UnitButton.setIcon(icon)
            self.UnitButton.setIconSize(QtCore.QSize(32, 16))
            self.UnitButton.setToolTip("Show board dimensions")

    def on_ViewChange(self):
        if self.widget.LogPlotter.showFront:
            self.widget.LogPlotter.showFront = False
            self.widget.LogPlotter.redraw_scene()
            icon = QtGui.QIcon()
            icon.addPixmap(
                QtGui.QPixmap("icons\\3dView2.png"),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ViewButton.setIcon(icon)
            self.ViewButton.setIconSize(QtCore.QSize(32, 16))
            self.ViewButton.setToolTip("Show front view")
        else:
            self.widget.LogPlotter.showFront = True
            self.widget.LogPlotter.redraw_scene()
            icon = QtGui.QIcon()
            icon.addPixmap(
                QtGui.QPixmap("icons\\frontView2.png"),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ViewButton.setIcon(icon)
            self.ViewButton.setIconSize(QtCore.QSize(32, 16))
            self.ViewButton.setToolTip("Show 3D view")

    def on_LTC(self):
        if self.ready[self.id]:
            self.ShowAnalysis(False)

    def on_TV(self):
        return

    def on_STV(self):
        return

    def on_RunCutplan(self, i):
        self.progressCP = i + 1
        a = i + 1
        b = self.CPSched.Cutplans.shape[0]
        self.loadingText.setText(str(a) + "/" + str(b) + " Cutplans Loaded")
        self.ready[i] = True
        self.pdModel._completed[i] = True
        self.tableView.update()
        if self.id == i:
            self.checkBox_2.setEnabled(True)
            self.checkBox_3.setEnabled(True)
            self.checkBox_4.setEnabled(True)
            self.EnableAnalysis(True)
            self.ShowAnalysis()
        self.SaveFunction()
        QtWidgets.QApplication.processEvents()

    def on_RunLog(self, i):
        self.progressBar.setValue(i*100)
        QtWidgets.QApplication.processEvents()

    def on_CPFinished(self):
        self.progressCP = self.CPSched.Cutplans.shape[0]
        self.progressBar.setValue(100)
        a = str(self.progressCP)
        b = str(self.progressCP)
        self.loadingText.setText(a + "/" + b + " Cutplans Loaded")
        self.checkBox_2.setEnabled(True)
        self.checkBox_3.setEnabled(True)
        self.checkBox_4.setEnabled(True)
        QtWidgets.QApplication.processEvents()
        for i in range(len(self.ready)):
            self.ready[i] = True
            self.pdModel._completed[i] = True
        self.CPRunning = False
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap("icons\\run.png"),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.RunButton.setIcon(icon2)
        self.RunButton.setToolTip("Simulate cutplans...")
        self.progressBar.setEnabled(False)
        self.progressBar.setVisible(False)
        self.thread.quit()
        self.thread.wait()
        self.SaveFunction()

    def on_Save(self):
        file = QtWidgets.QFileDialog.getSaveFileName(
            self.MainWindow, "Save File",
            filter="Data File (*.dat)")
        if str(file[0]) != "":
            self.SaveFunction(file[0])

    def SaveFunction(self, filePath=None):
        if filePath is None:
            filePath = "001.dat"
        # print("Attempting to save...")
        # self.thread.start()
        sf = []
        my_csv = self.CPSched.Cutplans.to_csv(index=False)
        sf.append(my_csv)
        sf.append(self.CPSched.AveR)
        sf.append(self.CPSched.MinHLog)
        sf.append(self.CPSched.MinWLog)
        sf.append(self.CPSched.MinH)
        sf.append(self.CPSched.MinW)
        sf.append(self.CPSched.completed)
        sf.append(self.CPSched.LogVol)
        sf.append(self.CPSched.BoardBreakdown)
        sf.append(self.CPSched.OpenFacePerc)
        # sf.append(self.CPSched.LogVolRand)
        # sf.append(self.CPSched.SavedCoords)
        with open(filePath, "wb") as save_file:
            dump(sf, save_file)
        # print("Save Successful")

    def on_AddCP(self):
        quit_msg = "Cannot add new cutplan when simulation running."
        if self.CPRunning:
            QtWidgets.QMessageBox.warning(
                self.MainWindow, 'Simulation running...', quit_msg,
                QtWidgets.QMessageBox.Ok)
            return

        # Ping to see if can connect, use wait cursor
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.WaitCursor))
        ping = ossystem(
            "ping -n 1 " + self.host
        )
        QtWidgets.QApplication.restoreOverrideCursor()
        quit_msg = "Check internet connection to Log Scanner Server."
        if ping:
            QtWidgets.QMessageBox.critical(
                self.MainWindow, "Connection Failed", quit_msg,
                QtWidgets.QMessageBox.Ok
            )
            return

        self.AddDialog = QtWidgets.QDialog()
        self.AddCPUI = AddCPUI()
        self.AddCPUI.setupUi(self.AddDialog, host=self.host)
        self.AddDialog.show()
        self.AddCPUI.buttonBox.accepted.connect(self.AddFunction)

    def AddFunction(self):
        tempID = self.id
        newCPID = self.AddCPUI.chosen

        # Ping to see if can connect, use wait cursor
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.WaitCursor))
        ping = ossystem(
            "ping -n 1 " + self.host
        )
        QtWidgets.QApplication.restoreOverrideCursor()
        quit_msg = "Check internet connection to Log Scanner Server."
        if ping:
            QtWidgets.QMessageBox.critical(
                self.MainWindow, "Connection Failed", quit_msg,
                QtWidgets.QMessageBox.Ok
            )
            return

        conn = sql.connect(
            'Driver={SQL Server};'
            'Server=192.168.3.55;'
            'Database=SequalLogScanner;'
            'UID=sa;'
            'PWD=gg8976@;')

        f = open("support\\cpquery2.sql", 'r')
        sqltext = f.read()
        sqltext = sqltext.replace("@CPID", str(newCPID))
        data = pd.read_sql(sqltext, conn)
        newCP = data.iloc[0]
        conn.close()
        f.close()

        self.CPSched.AddNewRow(newCP)
        self.ready.append(False)
        self.TVSetUp()
        tempSched = self.CPSched
        self.widget.CPSched = tempSched
        showPerc = self.widget.LogPlotter.showPerc
        showFront = self.widget.LogPlotter.showFront
        self.widget.LogPlotter = LogPlotGUI(
            self.widget.CPSched, self.LDDir)
        self.widget.LogPlotter.showPerc = showPerc
        self.widget.LogPlotter.showFront = showFront
        self.widget.LogPlotter.showLog = self.checkBox.isChecked()
        self.widget.LogPlotter.showBoards = self.checkBox_3.isChecked()
        self.widget.LogPlotter.showFL = self.checkBox_2.isChecked()
        self.widget.LogPlotter.show3m = self.checkBox_4.isChecked()
        self.widget.LogPlotter.showOpenFace = self.checkBox_OF.isChecked()
        self.tableView.selectRow(tempID)
        self.on_idChange()
        self.progressCP = sum(self.ready)
        a = self.progressCP
        b = self.CPSched.Cutplans.shape[0]
        self.loadingText.setText(
            str(a) + "/" + str(b) + " Cutplans Loaded")

    def on_DeleteCP(self):
        quit_msg = "Cannot delete cutplan when simulation running."
        if self.CPRunning:
            QtWidgets.QMessageBox.warning(
                self.MainWindow, 'Simulation running...', quit_msg,
                QtWidgets.QMessageBox.Ok)
            return

        des = self.CPSched.Cutplans.Description[self.id]
        cID = self.CPSched.Cutplans.CutplanID[self.id]
        quit_msg = "Are you sure you want to delete Cutplan {0} (".format(
            cID) + des + ")?"
        reply = QtWidgets.QMessageBox.question(
            self.MainWindow, 'Simulation still running...', quit_msg,
            QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.Cancel)

        if reply == QtWidgets.QMessageBox.Yes:
            self.DeleteFunction()
        else:
            return

    def DeleteFunction(self):
        tempID = self.id - 1
        self.CPSched.DeleteRow(self.id)
        del self.ready[self.id]
        self.TVSetUp()
        tempSched = self.CPSched
        self.widget.CPSched = tempSched
        showPerc = self.widget.LogPlotter.showPerc
        showFront = self.widget.LogPlotter.showFront
        self.widget.LogPlotter = LogPlotGUI(
            self.widget.CPSched, self.LDDir)
        self.widget.LogPlotter.showPerc = showPerc
        self.widget.LogPlotter.showFront = showFront
        self.widget.LogPlotter.showLog = self.checkBox.isChecked()
        self.widget.LogPlotter.showBoards = self.checkBox_3.isChecked()
        self.widget.LogPlotter.showFL = self.checkBox_2.isChecked()
        self.widget.LogPlotter.show3m = self.checkBox_4.isChecked()
        self.widget.LogPlotter.showOpenFace = self.checkBox_OF.isChecked()
        self.tableView.selectRow(tempID)
        self.on_idChange()
        self.progressCP = sum(self.ready)
        a = self.progressCP
        b = self.CPSched.Cutplans.shape[0]
        self.loadingText.setText(
            str(a) + "/" + str(b) + " Cutplans Loaded")

    def on_Load(self):
        quit_msg = (
            "Loading new file will lose current progress. "
            "Are you sure you want to load?"
        )
        if self.CPRunning:
            reply = QtWidgets.QMessageBox.question(
                self.MainWindow, 'Simulation still running...', quit_msg,
                QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:
                self.SaveFunction()
            else:
                return
        file = QtWidgets.QFileDialog.getOpenFileName(
            self.MainWindow, "Load File",
            filter="Data File (*.dat);;Cutplan Schedule (*.csv)")
        if str(file[0]) != "":
            if self.CPRunning:
                self.CPSched.abort = True
                self.thread.quit()
                self.thread.wait()
                self.CPRunning = False
                icon2 = QtGui.QIcon()
                icon2.addPixmap(
                    QtGui.QPixmap("icons\\run.png"),
                    QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.RunButton.setIcon(icon2)
                self.progressBar.setEnabled(False)
                self.progressBar.setVisible(False)
            self.LoadFunction(file[0])

    def LoadFunction(self, filePath=None):
        if filePath is None:
            file = "001.dat"
        elif filePath[-4:] == ".csv":
            self.CPSched = CPSchedule(filePath, self.LDDir)
            self.ready = [False]*self.CPSched.Cutplans.shape[0]
            self.CPThreadSetUp()
            self.TVSetUp()
            tempSched = self.CPSched
            self.widget.CPSched = tempSched
            showPerc = self.widget.LogPlotter.showPerc
            showFront = self.widget.LogPlotter.showFront
            self.widget.LogPlotter = LogPlotGUI(
                self.widget.CPSched, self.LDDir)
            self.widget.LogPlotter.showPerc = showPerc
            self.widget.LogPlotter.showFront = showFront
            self.on_checkBox()
            self.on_idChange()
            self.progressCP = sum(self.ready)
            a = self.progressCP
            b = self.CPSched.Cutplans.shape[0]
            self.loadingText.setText(
                str(a) + "/" + str(b) + " Cutplans Loaded")
            return
        else:
            file = filePath
        # print("Attempting to load...")
        try:
            with open(file, "rb") as load_file:
                lf = load(load_file)
                my_csv = lf[0]
                f = open("000.csv", "w", newline="")
                f.write(my_csv)
                f.close()
                self.CPSched = CPSchedule("000.csv", self.LDDir)
                self.CPSched.AveR = lf[1]
                self.CPSched.MinHLog = lf[2]
                self.CPSched.MinWLog = lf[3]
                self.CPSched.MinH = lf[4]
                self.CPSched.MinW = lf[5]
                self.CPSched.completed = lf[6]
                self.CPSched.LogVol = lf[7]
                self.CPSched.BoardBreakdown = lf[8]
                if len(lf) > 9:
                    self.CPSched.OpenFacePerc = lf[9]
                self.CPThreadSetUp()
                # self.CPSched.LogVolRand = lf[9]
                # self.CPSched.SavedCoords = lf[10]
                for i in range(len(self.CPSched.completed)):
                    if self.CPSched.completed[i]:
                        self.CPSched.EstVol[i] = nanmean(
                            self.CPSched.LogVol[i]
                        ) * nparray(self.CPSched.Cutplans.LogCount[i])

                if filePath is not None:
                    self.ready = [False]*self.CPSched.Cutplans.shape[0]
                    for i in range(len(self.ready)):
                        if self.CPSched.completed[i]:
                            self.ready[i] = True
                    self.TVSetUp()
                    tempSched = self.CPSched
                    self.widget.CPSched = tempSched
                    showPerc = self.widget.LogPlotter.showPerc
                    showFront = self.widget.LogPlotter.showFront
                    self.widget.LogPlotter = LogPlotGUI(
                        self.widget.CPSched, self.LDDir)
                    self.widget.LogPlotter.showPerc = showPerc
                    self.widget.LogPlotter.showFront = showFront
                    self.on_checkBox()
                    self.on_idChange()
                    self.progressCP = sum(self.ready)
                    a = self.progressCP
                    b = self.CPSched.Cutplans.shape[0]
                    self.loadingText.setText(
                        str(a) + "/" + str(b) + " Cutplans Loaded")
            # print("Load Successful")
        except OSError:
            self.CPSched = CPSchedule("000.csv", self.LDDir)
            self.CPThreadSetUp()
            # print("Load Failed")

    def TVSetUp(self):
        self.pdModel = PandasModel(
            self.CPSched.Cutplans[['CutplanID', 'Description']],
            completed=self.ready)
        self.tableView.setModel(self.pdModel)
        self.tableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.tableView.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.tableView.verticalHeader().setVisible(False)
        selModel = self.tableView.selectionModel()
        selModel.selectionChanged.connect(self.on_idChange)

    def AnalTVSetUp(self):
        df = self.CPSched.BoardBreakdown[self.id].breakdown
        headers = df.columns
        data = []
        for i, row in df.iterrows():
            r = [row[0]]
            w = float(row[0].split("x")[0])
            t = float(row[0].split("x")[1])
            for j in range(1, len(row)):
                bL = float(df.columns[j][:3])
                if self.LogsToCutTB.text():
                    val = int(self.LogsToCutTB.text())*row[j]
                else:
                    val = 0
                if val == 0:
                    r.append(" ")
                else:
                    if self.rbPieceCount.isChecked():
                        r.append("{:.0f}".format(val))
                    else:
                        val *= w*t*bL*0.000001
                        if val < 1:
                            r.append("{:.3f}m3".format(val))
                        elif val < 10:
                            r.append("{:.2f}m3".format(val))
                        elif val < 100:
                            r.append("{:.1f}m3".format(val))
                        else:
                            r.append("{:.0f}m3".format(val))
            data.append(tuple(r))
        df = pd.DataFrame(data, columns=headers)

        self.analModel = PandasModel(df)
        self.CutbackTable.setModel(self.analModel)
        self.CutbackTable.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.CutbackTable.setSelectionMode(
            QtWidgets.QTableView.SingleSelection)
        self.CutbackTable.verticalHeader().setVisible(False)
        self.CutbackTable.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(9)
        self.CutbackTable.horizontalHeader().setFont(font)

    def EnableAnalysis(self, val):
        self.LogsToCutTB.setEnabled(val)
        self.TimberVolumeTB.setEnabled(val)
        self.RecoveryTB.setEnabled(val)
        self.SimTimberVolumeTB.setEnabled(val)
        self.SimRecoveryTB.setEnabled(val)
        self.UnitButton.setEnabled(val)
        self.CutbackTable.setEnabled(val)
        self.rbPieceCount.setEnabled(val)
        self.rbVolume.setEnabled(val)
        self.OFTextBox.setEnabled(val)
        self.checkBox_OF.setEnabled(val)

    def CPThreadSetUp(self):
        self.thread = QtCore.QThread()
        self.CPSched.cp_progress.connect(self.on_RunCutplan)
        self.CPSched.l_progress.connect(self.on_RunLog)
        self.CPSched.moveToThread(self.thread)
        self.CPSched.finished.connect(self.on_CPFinished)
        self.thread.started.connect(self.CPSched.RunCutplan)

    def on_Run(self):
        if self.CPRunning:
            self.CPSched.abort = True
            self.thread.quit()
            self.thread.wait()
            self.CPRunning = False
            icon2 = QtGui.QIcon()
            icon2.addPixmap(
                QtGui.QPixmap("icons\\run.png"),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.RunButton.setIcon(icon2)
            self.RunButton.setToolTip("Simulate cutplans...")
            self.progressBar.setEnabled(False)
            self.progressBar.setVisible(False)
        else:
            self.CPRunning = True
            self.thread.start()
            icon2 = QtGui.QIcon()
            icon2.addPixmap(
                QtGui.QPixmap("icons\\stop.png"),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.RunButton.setIcon(icon2)
            self.RunButton.setToolTip("Stop simulation")
            self.progressBar.setEnabled(True)
            self.progressBar.setVisible(True)
        # self.SettingsDialog = QtWidgets.QDialog()
        # self.SettingsUI = SettingsUI()
        # self.SettingsUI.setupUi(self.SettingsDialog, self)
        # self.SettingsDialog.show()

    def on_checkBox(self):
        self.widget.LogPlotter.showLog = self.checkBox.isChecked()
        self.widget.LogPlotter.showBoards = self.checkBox_3.isChecked()
        self.widget.LogPlotter.showFL = self.checkBox_2.isChecked()
        self.widget.LogPlotter.show3m = self.checkBox_4.isChecked()
        self.widget.LogPlotter.showOpenFace = self.checkBox_OF.isChecked()
        self.widget.LogPlotter.update_scene()

    def on_idChange(self):
        selected = self.tableView.selectionModel().selectedRows()
        if len(selected) == 0:
            self.tableView.selectRow(0)
            self.widget.LogPlotter.id = 0
            self.widget.LogPlotter.redraw_scene()
            self.id = 0
        else:
            self.widget.LogPlotter.id = selected[0].row()
            self.widget.LogPlotter.redraw_scene()
            self.id = selected[0].row()
        if self.ready[self.id]:
            self.checkBox_2.setEnabled(True)
            self.checkBox_3.setEnabled(True)
            self.checkBox_4.setEnabled(True)
            self.ShowAnalysis()
            self.EnableAnalysis(True)
        else:
            self.checkBox_2.setEnabled(False)
            self.checkBox_3.setEnabled(False)
            self.checkBox_4.setEnabled(False)
            self.ClearAnalysis()
            self.EnableAnalysis(False)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate(
            "MainWindow", "Cutplan Analysis Tool"))
        self.label.setText(_translate("MainWindow", "Thursday, 30 May 2019"))
        self.checkBox.setText(_translate("MainWindow", "Show Log"))
        self.checkBox_2.setText(
            _translate("MainWindow", "Show Full-Length Area"))
        self.checkBox_3.setText(_translate("MainWindow", "Show Boards"))
        self.checkBox_4.setText(_translate("MainWindow", "Show 3m Area"))
        self.checkBox_OF.setText(_translate("MainWindow", "Show Open Face"))
        a = str(self.progressCP)
        b = str(len(self.widget.CPSched.completed))
        self.loadingText.setText(_translate(
            "MainWindow", a + "/" + b + " Cutplans Loaded"))
        self.LogsToCut.setText(_translate("MainWindow", "Logs to Cut:"))
        self.Recovery.setText(_translate(
            "MainWindow", self.optTxt+"\nRecovery:"))
        self.TimberVolume.setText(_translate(
            "MainWindow", self.optTxt+"\nTimber Volume:"))
        self.SimTimberVolume.setText(_translate(
            "MainWindow", "Simulated\nTimber Volume:"))
        self.SimRecovery.setText(_translate(
            "MainWindow", "Simulated\nRecovery:"))
        header = self.tableView.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.tableView.selectRow(self.id)
        self.rbPieceCount.setText(_translate("MainWindow", "Piece Count"))
        self.rbVolume.setText(_translate("MainWindow", "Volume"))
        self.OFLabel.setText(_translate(
            "MainWindow", "Lost Open Face\nPercentage"))

    def on_LoadLogs(self):
        quit_msg = "Cannot update logs when simulation running."
        if self.CPRunning:
            QtWidgets.QMessageBox.warning(
                self.MainWindow, 'Simulation running...', quit_msg,
                QtWidgets.QMessageBox.Ok)
            return

        # Ping to see if can connect, use wait cursor
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.WaitCursor))
        ping = ossystem(
            "ping -n 1 " + self.host
        )
        QtWidgets.QApplication.restoreOverrideCursor()
        quit_msg = "Check internet connection to Log Scanner Server."
        if ping:
            QtWidgets.QMessageBox.critical(
                self.MainWindow, "Connection Failed", quit_msg,
                QtWidgets.QMessageBox.Ok
            )
            return

        self.ReloadFunction()
        quit_msg = "Log data successfully updated from server."
        QtWidgets.QMessageBox.warning(
            self.MainWindow, 'Log Data Updated!', quit_msg,
            QtWidgets.QMessageBox.Ok)

    def ReloadFunction(self):
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.WaitCursor))
        sqlfile = "support\\ldQuery.sql"
        sqlfile2 = "support\\ldQuery2.sql"

        conn = sql.connect(
            'Driver={SQL Server};'
            'Server=192.168.3.55;'
            'Database=SequalLogScanner;'
            'UID=sa;'
            'PWD=gg8976@;')

        f = open(sqlfile, 'r')
        sqltext = f.read()
        sorts = pd.read_sql(sqltext, conn)

        f = open(sqlfile2, 'r')
        sqltext = f.read()

        data = []
        for des in sorts.Description:
            data.append(pd.read_sql(
                sqltext.replace('@sort', des), conn))

        folder = self.LDDir
        for i in range(len(sorts)):
            des = sorts.Description[i]
            des = des.replace('-41', '-40')
            des = des.replace('-47', '-46')
            des2 = des.replace('-46', '-45')
            d = data[i]
            f = open(folder+des+".csv", "w", newline="")
            f.write(d.to_csv(index=False))
            f.close()
            if des2 != des:
                f = open(folder+des2+".csv", "w", newline="")
                f.write(d.to_csv(index=False))
                f.close()

        QtWidgets.QApplication.restoreOverrideCursor()

    def displayTime(self):
        self.label.setText(QtCore.QDateTime.currentDateTime().toString())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication.instance()
    MainWindow = CA_MainWindow()
    ui = CAGUI()
    ui.setupUi(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())
