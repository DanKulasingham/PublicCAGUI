"""
@author: Daniel Kulasingham

Main Cutplan File
"""
import numpy as np
import pandas as pd
from os import path
import time
from pathos.multiprocessing import ProcessingPool as Pool, cpu_count
# import matplotlib.pyplot as plt
from statistics import mean

from cutplan._coordinates import GetLogCoords, CalcBoardVol, Recovery
from cutplan._helper import CalcUseable, GetUseableCoords
from cutplan._boards import BoardBreakdown

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class CPSchedule(QObject):
    finished = pyqtSignal()
    cp_progress = pyqtSignal(int)
    l_progress = pyqtSignal(float)

    def __init__(self, cpPath="", logPath=""):
        super().__init__()
        self.abort = False

        if cpPath == "":
            cpPath = path.dirname(path.realpath(__file__)) + \
                "\\CutplanSchedule.csv"
        if cpPath[-4] != ".":
            cpPath = cpPath + "\\CutplanSchedule.csv"
        if logPath == "":
            logPath = path.dirname(cpPath) + "\\"

        self.cpPath = cpPath
        self.logPath = logPath
        self.Cutplans = pd.read_csv(cpPath)  # open the cutplan schedule
        self.LogVol = np.empty((self.Cutplans.shape[0], 1000))
        self.LogVol[:] = np.nan
        # self.LogVolRand = np.empty((self.Cutplans.shape[0], 1000))
        # self.LogVolRand[:] = np.nan
        self.EstVol = np.empty(self.Cutplans.shape[0])
        self.EstVol[:] = np.nan
        self.ActVol = np.array(self.Cutplans.BoardVol)
        self.AveR = [None]*self.Cutplans.shape[0]
        self.MinHLog = np.zeros((self.Cutplans.shape[0], 2))
        self.MinWLog = np.zeros((self.Cutplans.shape[0], 2))
        self.MinH = np.zeros((self.Cutplans.shape[0], 2))
        self.MinW = np.zeros((self.Cutplans.shape[0], 2))
        self.completed = [False]*self.Cutplans.shape[0]
        self.BoardBreakdown = [None]*self.Cutplans.shape[0]
        self.OpenFacePerc = [0]*self.Cutplans.shape[0]
        self.progress = 0

    @pyqtSlot()
    def RunCutplan(self):
        # initialisations
        cbL = 3
        timer = True
        id = []
        # t = time.time()
        if id == []:
            start_id = sum(self.completed)
            id = list(range(start_id, self.Cutplans.shape[0]))
        numproc = cpu_count() - 2
        p = Pool(processes=numproc)
        # cpSched = self.Cutplans.iloc[id]
        total = len(id)*1000
        for cID in id:
            c = self.Cutplans.iloc[cID]
            # find desc to be used to open the correct log data file
            desc = c.Description[2:4]+"-"+str(int(c.Description[5:7])-1)
            # get data from log data file
            LD = pd.read_csv(self.logPath+desc+'.csv')

            # initialise recovery
            recovery = Recovery(c)
            iterLog = []
            iterC = []
            for i in range(LD.shape[0]):
                log = LD.iloc[i]
                iterLog.append(log)
                iterC.append(c)

# =============================================================================
#             completed = []
#             for lID in range(len(iterLog)):
#                 log = iterLog[lID]
#                 coords = GetLogCoords(log, c)
#                 completed.append(coords)
#                 Timer(id, cID, lID, time.time()-t)
# =============================================================================
            # if id.index(cID) > 0:
            #     p.restart()
            data = []
            data = p.imap(GetLogCoords, iterLog, iterC)
            completed = []
            i = 0
            while len(completed) < LD.shape[0]:
                try:
                    res = next(iter(data))
                    completed.append(res)
                    if self.abort:
                        self.abort = False
                        return
                    if timer:
                        count = id.index(cID)*1000 + len(completed)
                        self.l_progress.emit(count/total)
                        # Timer(id, cID, len(completed)-1, time.time()-t)
                except BaseException:
                    break

            self.AveR[cID] = Recovery(c)
            self.BoardBreakdown[cID] = BoardBreakdown(c)
            minW = [1000000, 1000000]
            minH = [1000000, 1000000]
            minWID = [0, 0]
            minHID = [0, 0]
            numOF = 0
            for lID in range(LD.shape[0]):
                coords = completed[lID]
                newW, newH = CalcUseable(coords)
                if newW < minW[0]:
                    minW[0] = newW
                    minWID[0] = lID
                if newH < minH[0]:
                    minH[0] = newH
                    minHID[0] = lID
                newW1, newH1 = CalcUseable(coords, cbL)
                if newW1 < minW[1]:
                    minW[1] = newW1
                    minWID[1] = lID
                if newH1 < minH[1]:
                    minH[1] = newH1
                    minHID[1] = lID
                # OF = recovery.RunRecoveryRand(coords, offS=2.725)
                # numOF += not OF
                OF = recovery.RunRecovery(coords)
                numOF += not OF
                self.AveR[cID].AddRecovery(recovery)
                self.BoardBreakdown[cID].AddRecovery(recovery)
                self.LogVol[cID, lID] = CalcBoardVol(
                    LD.iloc[lID], c, recovery
                )
                # recovery.RunRecovery(coords)
                # self.LogVol[cID, lID] = CalcBoardVol(
                #     LD.iloc[lID], c, recovery
                # )

            self.AveR[cID].AverageRecovery(LD.shape[0])
            self.BoardBreakdown[cID].AverageRecovery(LD.shape[0])
            self.MinHLog[cID][0] = minHID[0]
            self.MinWLog[cID][0] = minWID[0]
            self.MinW[cID][0] = minW[0]
            self.MinH[cID][0] = minH[0]
            self.MinHLog[cID][1] = minHID[1]
            self.MinWLog[cID][1] = minWID[1]
            self.MinW[cID][1] = minW[1]
            self.MinH[cID][1] = minH[1]
            self.OpenFacePerc[cID] = numOF/LD.shape[0]

            time.sleep(0.1)

            self.completed[cID] = True
            self.cp_progress.emit(cID)

        self.EstVol = np.nanmean(self.LogVol, 1) * np.array(
            self.Cutplans.LogCount)

        self.finished.emit()
        return self.AveR

    def AddNewRow(self, newCP):
        temp = self.Cutplans
        self.Cutplans = temp.append(newCP, True)
        temp = list(self.LogVol)
        temp.append(np.empty(1000) * np.nan)
        self.LogVol = np.array(temp)
        self.EstVol = np.nanmean(self.LogVol, 1) * np.array(
            self.Cutplans.LogCount)
        self.ActVol = np.array(self.Cutplans.BoardVol)
        self.AveR.append(None)
        temp = list(self.MinHLog)
        temp.append([0., 0.])
        self.MinHLog = np.array(temp)
        temp = list(self.MinWLog)
        temp.append([0., 0.])
        self.MinWLog = np.array(temp)
        temp = list(self.MinH)
        temp.append([0., 0.])
        self.MinH = np.array(temp)
        temp = list(self.MinW)
        temp.append([0., 0.])
        self.MinW = np.array(temp)
        self.completed.append(False)
        self.BoardBreakdown.append(None)
        self.OpenFacePerc.append(0)

    def DeleteRow(self, row):
        self.Cutplans = self.Cutplans.drop(
            [row], axis=0
        ).reset_index().drop('index', axis=1)
        self.LogVol = np.delete(self.LogVol, [row], axis=0)
        self.EstVol = np.nanmean(self.LogVol, 1) * np.array(
            self.Cutplans.LogCount)
        self.ActVol = np.array(self.Cutplans.BoardVol)
        del self.AveR[row]
        self.MinHLog = np.delete(self.MinHLog, [row], axis=0)
        self.MinWLog = np.delete(self.MinWLog, [row], axis=0)
        self.MinH = np.delete(self.MinH, [row], axis=0)
        self.MinW = np.delete(self.MinW, [row], axis=0)
        del self.completed[row]
        del self.BoardBreakdown[row]
        del self.OpenFacePerc[row]

    # def PlotResults(self):
    #     fig, axs = plt.subplots(nrows=1, ncols=2)
    #     fig.suptitle(r'Cutplan Estimation Results')
    #
    #     ax = axs[0]
    #     ax.plot(
    #         [0, max(self.ActVol)], [0, max(self.ActVol)],
    #         linewidth=0.75, c=[1, 0.85, 0.65]
    #     )
    #     ax.plot(self.ActVol, self.EstVol, 'o', c=[0.93, 0.63, 0.203])
    #     ax.set_xlabel(r'Optimiser Value ($m^3$)')
    #     ax.set_ylabel(r'Calculated Value ($m^3$)')
    #
    #     ax = axs[1]
    #     res = (self.EstVol-self.ActVol)/self.ActVol
    #     ax.plot([0, len(res)], [0, 0], linewidth=0.75, c=[1, 0.85, 0.65])
    #     ax.plot(range(len(res)), res, 'o', c=[0.93, 0.63, 0.203])
    #     ax.set_xlabel(r'Cutplan Number')
    #     ax.set_ylabel(r'Difference (%)')
    #     return

    def AverageLog(self, id):
        c = self.Cutplans.iloc[id]
        # find desc to be used to open the correct log data file
        desc = c.Description[2:4]+"-"+str(int(c.Description[5:7])-1)
        # get data from log data file
        LD = pd.read_csv(self.logPath+desc+'.csv')

        log = pd.Series({
            "Length": mean(LD.Length),
            "SED": mean(LD.SED),
            "MinSED": mean(LD.MinSED),
            "LED": mean(LD.LED),
            "MaxLED": mean(LD.MaxLED),
            "Sweep": mean(LD.Sweep),
            "CompSweep": mean(LD.CompSweep),
            "Vol": mean(LD.Vol)
        })

        return log

    def MinWUseable(self, id):
        log = self.MinWLog[id]
        coords = GetLogCoords(log, None, False)
        return GetUseableCoords(coords)

    def MinHUseable(self, id):
        log = self.MinHLog[id]
        coords = GetLogCoords(log, None, False)
        return GetUseableCoords(coords)

    def GetMinWLog(self, id, full=0):
        lID = self.MinWLog[id][full]
        c = self.Cutplans.iloc[id]
        # find desc to be used to open the correct log data file
        desc = c.Description[2:4]+"-"+str(int(c.Description[5:7])-1)
        # get data from log data file
        LD = pd.read_csv(self.logPath+desc+'.csv')

        log = pd.Series({
            "Length": (LD.Length[lID]),
            "SED": (LD.SED[lID]),
            "MinSED": (LD.MinSED[lID]),
            "LED": (LD.LED[lID]),
            "MaxLED": (LD.MaxLED[lID]),
            "Sweep": (LD.Sweep[lID]),
            "CompSweep": (LD.CompSweep[lID]),
            "Vol": (LD.Vol[lID])
        })

        return log

    def GetTimberVolume(self, id):
        avgLog = self.AverageLog(id)
        c = self.Cutplans.iloc[id]
        r = Recovery(c)
        # Set to 1 for each WB
        for k in r.WB.keys():
            if len(r.WB[k]) > 0:
                for i in range(len(r.WB[k])):
                    r.WB[k][i] = 1
        # Set to 1 for each CB
        for i in range(len(r.CB)):
            if np.isnan(r.WB['CentreWB'][i]):
                for j in range(len(r.CB[i])):
                    r.CB[i][j] = 1
        TimVol = CalcBoardVol(avgLog, c, r)
        return TimVol

    def __repr__(self):
        return ("Cutplan Schedule with "+str(len(self.Cutplans))+" cutplans")
