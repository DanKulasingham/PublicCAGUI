"""
@author: Daniel Kulasingham

Sets up the data frame to keep track of cutback volumes
"""
import pandas as pd
from numpy import isnan
from cutplan._coordinates import Recovery

class BoardBreakdown():
    def __init__(self, c):
        self.c = c
        if c.Description[5:7] == '41':
            self.bL = 4.0
        else:
            self.bL = 4.6
        self.boards = GetBoards(c)
        data = {
            'Board': self.boards,
            str(self.bL)+'m': [0.0]*len(self.boards),
            '3.6m': [0.0]*len(self.boards),
            '3.3m': [0.0]*len(self.boards),
            '3.0m': [0.0]*len(self.boards)
        }
        self.breakdown = pd.DataFrame(data)
        self.breakdown.set_index('Board')

    def AddRecovery(self, r):
        # Initialisations
        c = self.c
        if c.HSNum > 0:
            cbW = list(c[37:(37+c.HSNum+1)])  # HoriSaw widths
        else:
            cbW = c.CBWidth
        cbNum = c.CBNum
        cbT = list(c[14:(14+cbNum)])  # CB Thicknesses

        # Wingboard volumes
        for i in r.WB["PrimOutR"]:
            self.AddVol(c.PrimOutWidth, c.PrimOutThick, i)
        for i in r.WB["PrimOutL"]:
            self.AddVol(c.PrimOutWidth, c.PrimOutThick, i)
        for i in r.WB["PrimInR"]:
            self.AddVol(c.PrimInWidth, c.PrimInThick, i)
        for i in r.WB["PrimInL"]:
            self.AddVol(c.PrimInWidth, c.PrimInThick, i)
        for i in r.WB["SecOutT"]:
            self.AddVol(c.SecOutWidth, c.SecOutThickT, i)
        for i in r.WB["SecOutB"]:
            self.AddVol(c.SecOutWidth, c.SecOutThickB, i)
        for i in r.WB["SecInT"]:
            self.AddVol(c.SecInWidth, c.SecInThickT, i)
        for i in r.WB["SecInB"]:
            self.AddVol(c.SecInWidth, c.SecInThickB, i)

        for i in range(cbNum):
            if isnan(r.WB["CentreWB"][i]):
                if c.HSNum > 0:
                    for j in range(len(cbW)):
                        self.AddVol(cbW[j], cbT[i], r.CB[i][j])
                else:
                    if len(r.CB[i]) > 0:
                        self.AddVol(c.CBWidth, cbT[i], r.CB[i][0])
            else:
                self.AddVol(c.CBWidth, cbT[i], r.WB["CentreWB"][i])

    def AverageRecovery(self, numLogs):
        for i in range(self.breakdown.shape[0]):
            for j in range(1, self.breakdown.shape[1]):
                self.breakdown.iat[i, j] /= numLogs
                # self.breakdown.iat[i, j] /= 1000000

    def AddVol(self, w, t, r):
        if r == 0:
            return
        i = self.DimToInd(w, t)  # get index based on dimension

        cb = -1
        for j in range(1, self.breakdown.shape[1]):
            k = self.breakdown.keys()[j]  # loop through cb lengths
            if r == (float(k[:-1])/self.bL):
                # if r matches cutback length
                cb = j
                break

        if cb == -1:  # cb length not found
            raise Exception(
                DimToStr(w, t)+": "+str(r)+", "+"{0}".format(self.bL))

        self.breakdown.iat[i, cb] += 1

    def DimToInd(self, w, t):
        dim = DimToStr(w, t)
        ind = self.boards.index(dim)
        return ind

    def __repr__(self):
        return self.breakdown.to_string()


def GetBoards(c):
    r = Recovery(c)
    boards = []
    cbW = c.CBWidth  # CB Width
    cbT = list(c[14:(14+c.CBNum)])  # CB Thicknesses
    hsW = list(c[37:(37+c.HSNum+1)])  # HoriSaw widths
    hNum = c.HSNum + 1  # Number of horizontal saws

    # Wingboards
    if len(r.WB["PrimOutL"]) > 0:
        boards.append(DimToStr(c.PrimOutWidth, c.PrimOutThick))
    if len(r.WB["PrimInL"]) > 0:
        boards.append(DimToStr(c.PrimInWidth, c.PrimInThick))
    if len(r.WB["SecOutT"]) > 0:
        boards.append(DimToStr(c.SecOutWidth, c.SecOutThickT))
    if len(r.WB["SecOutB"]) > 0:
        boards.append(DimToStr(c.SecOutWidth, c.SecOutThickB))
    if len(r.WB["SecInT"]) > 0:
        boards.append(DimToStr(c.SecInWidth, c.SecInThickT))
    if len(r.WB["SecInB"]) > 0:
        boards.append(DimToStr(c.SecInWidth, c.SecInThickB))

    # Centreboards
    for i in range(c.CBNum):
        if hNum > 1 and isnan(r.WB["CentreWB"][i]):
            for j in range(hNum):
                boards.append(DimToStr(hsW[j], cbT[i]))
        else:
            boards.append(DimToStr(cbW, cbT[i]))

    boards = list(dict.fromkeys(boards))
    return boards


def DimToStr(w, t):
    if w > t:
        dim = "{0}x{1}".format(w, t)
    else:
        dim = "{0}x{1}".format(t, w)
    return dim
