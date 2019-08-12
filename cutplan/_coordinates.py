"""
@author: Daniel Kulasingham

Functions that focus on getting coordinates of log
"""
from numpy import \
    linspace, empty, transpose, max, min, cos, sin, nan, \
    array as arraynp, isnan, sqrt, arange, zeros, argmax, append
from scipy.optimize import minimize_scalar as FindMin
from numpy.matlib import repmat
from math import pi, floor
from random import random
from itertools import groupby
from cutplan._helper import SumRecov, GetWane, BoardRecovery


# class for how coordinates will be stored
class Coordinates():
    def __init__(self, X=0, Y=0, Z=0, Offset=[0, 0], OpenFace=[0, 0, 0, 0]):
        self.X = X
        self.Y = Y
        self.Z = Z
        self.Offset = Offset
        self.OpenFace = OpenFace

    def __repr__(self):
        return (
            "X = "+str(self.X)+"\n"
            "Y = "+str(self.Y)+"\n"
            "Z = "+str(self.Z)+"\n"
            "Offset = "+str(self.Offset)
        )


# class for how recovery will be stored
class Recovery():
    def __init__(self, c):
        self.Cutplan = c
        self.CBNum = 0
        self.CB = [[]]*c.CBNum
        self.WB = {
            "SecOutT": [],
            "SecOutB": [],
            "SecInT": [],
            "SecInB": [],
            "PrimOutL": [],
            "PrimOutR": [],
            "PrimInL": [],
            "PrimInR": [],
            "CentreWB": [0]*c.CBNum
        }
        self.CheckCB()
        self.CheckWB()
        self.CheckSplit()

    def CheckSplit(self):
        c = self.Cutplan
        if c.SecOutSplitT:
            self.WB["SecOutT"].append(0)
        if c.SecOutSplitB:
            self.WB["SecOutB"].append(0)
        if c.SecInSplitT:
            self.WB["SecInT"].append(0)
        if c.SecInSplitB:
            self.WB["SecInB"].append(0)
        if c.PrimOutSplit:
            self.WB["PrimOutL"].append(0)
            self.WB["PrimOutR"].append(0)
        if c.PrimInSplit:
            self.WB["PrimInL"].append(0)
            self.WB["PrimInR"].append(0)
        self.WBNum = sum([len(i) for i in self.WB.values()]) - self.CBNum
        return

    def CheckCB(self):
        cbs = list(self.Cutplan[14:(14+self.Cutplan.CBNum)])
        count = [sum(1 for i in g) for _, g in groupby(cbs)]
        index = [i for i in range(len(count)) if count[i] == max(count)]
        start = sum(count[i] for i in range(index[floor(len(index)/2)]))
        for i in range(start, (start+max(count))):
            self.CB[i] = [0]*(self.Cutplan.HSNum+1)
        self.WB["CentreWB"][start:(start+max(count))] = [nan]*max(count)
        self.CBNum = max(count)
        return

    def CheckWB(self):
        c = self.Cutplan
        if c.PrimInThick > 0:
            self.WB["PrimInL"].append(0)
            self.WB["PrimInR"].append(0)
        if c.PrimOutThick > 0:
            self.WB["PrimOutL"].append(0)
            self.WB["PrimOutR"].append(0)
        if c.SecOutThickT:
            self.WB["SecOutT"].append(0)
        if c.SecOutThickB:
            self.WB["SecOutB"].append(0)
        if c.SecInThickT:
            self.WB["SecInT"].append(0)
        if c.SecInThickB:
            self.WB["SecInB"].append(0)
        return

    def RunRecovery(self, coords):
        # initialisations
        c = self.Cutplan
        cbNum = c.CBNum
        cbT = arraynp(c[14:(14+cbNum)])  # CB Thicknesses

        # cant calculations
        cantH = sum(cbT) + (sum(cbT > 0)-1)*c.SecK  # centreboards
        cantH += (c.SecInSplitT+1) * \
            (c.SecInThickT+c.SecK*(c.SecInThickT > 0))  # secondary in top
        cantH += (c.SecInSplitB+1) * \
            (c.SecInThickB+c.SecK*(c.SecInThickB > 0))  # secondary in bot
        cantH += (c.SecOutSplitT+1) * \
            (c.SecOutThickT+c.SecK*(c.SecOutThickT > 0))  # secondary out top
        cantH += (c.SecOutSplitB+1) * \
            (c.SecOutThickB+c.SecK*(c.SecOutThickB > 0))  # secondary out bot

        cH = cantH/2

        # find group length
        if c.Description[5:7] == '41':
            bL = 4000
        else:
            bL = 4600

        # SECONDARY OUT TOP
        cH = self.FindRecovery(
            "SecOutT", coords, cH, bL,
            c.SecOutThickT, c.SecOutWidth/2, c.SecOutSplitT, c.SecK
        )

        # SECONDARY IN TOP
        cH = self.FindRecovery(
            "SecInT", coords, cH, bL,
            c.SecInThickT, c.SecInWidth/2, c.SecInSplitT, c.SecK
        )

        # CENTREBOARDS
        w = c.CBWidth/2  # CB Width
        hNum = c.HSNum + 1  # Number of horizontal saws
        hW = arraynp(c[37:(37+hNum)])  # HoriSaw board widths
        hK = list(c[41:(41+hNum-1)])  # Horizontal saw kerfs
        hK.append(0)
        for i in range(cbNum):
            t = cbT[i]
            if hNum > 1 and isnan(self.WB["CentreWB"][i]):
                hsW = -c.CBWidth/2 + hW[0]/2
                for j in range(hNum):
                    wane = GetWane(coords, cH, t, hW[j]/2)
                    self.CB[i][j] = min(wane) + 0.0  # recovery 0 if any wane
                    hsW = hsW + hW[j] + hK[j]
            else:
                wane = GetWane(coords, cH, t, w)
                if isnan(self.WB["CentreWB"][i]):
                    self.CB[i][0] = min(wane) + 0.0  # recovery 0 if any wane
                else:
                    self.WB["CentreWB"][i] = BoardRecovery(wane, coords.Z, bL)

            cH = cH - t - c.SecK

        # SECONDARY IN BOTTOM
        cH = self.FindRecovery(
            "SecInB", coords, cH, bL,
            c.SecInThickB, c.SecInWidth/2, c.SecInSplitB, c.SecK
        )

        # SECONDARY OUT BOTTOM
        cH = self.FindRecovery(
            "SecOutB", coords, cH, bL,
            c.SecOutThickB, c.SecOutWidth/2, c.SecOutSplitB, c.SecK
        )

        # PRIMARY IN
        cW = c.CBWidth/2
        t = c.PrimInThick
        w = c.PrimInWidth/2
        split = c.PrimInSplit
        if t > 0:
            cW = cW + c.PrimInK

            wane = GetWane(coords, cW+t, t, w, True)
            self.WB["PrimInR"][0] = BoardRecovery(wane, coords.Z, bL)
            wane = GetWane(coords, -cW, t, w, True)
            self.WB["PrimInL"][0] = BoardRecovery(wane, coords.Z, bL)

            cW = cW + t
        if split:
            cW = cW + c.PrimInK

            wane = GetWane(coords, cW+t, t, w, True)
            self.WB["PrimInR"][1] = BoardRecovery(wane, coords.Z, bL)
            wane = GetWane(coords, -cW, t, w, True)
            self.WB["PrimInL"][1] = BoardRecovery(wane, coords.Z, bL)

            cW = cW + t

        # PRIMARY OUT
        cW = c.CBWidth/2
        t = c.PrimOutThick
        w = c.PrimOutWidth/2
        split = c.PrimOutSplit
        if t > 0:
            cW = cW + c.PrimOutK

            wane = GetWane(coords, cW+t, t, w, True)
            self.WB["PrimOutR"][0] = BoardRecovery(wane, coords.Z, bL)
            wane = GetWane(coords, -cW, t, w, True)
            self.WB["PrimOutL"][0] = BoardRecovery(wane, coords.Z, bL)

            cW = cW + t
        if split:
            cW = cW + c.PrimOutK

            wane = GetWane(coords, cW+t, t, w, True)
            self.WB["PrimOutR"][1] = BoardRecovery(wane, coords.Z, bL)
            wane = GetWane(coords, -cW, t, w, True)
            self.WB["PrimOutL"][1] = BoardRecovery(wane, coords.Z, bL)

            cW = cW + t

        OF = cantH <= (coords.OpenFace[1] - coords.OpenFace[3])
        OF = OF and (cW*2 <= (coords.OpenFace[0] - coords.OpenFace[2]))

        return OF

    def RunRecoveryRand(self, coordsOri, offS=3):
        # initialisations
        c = self.Cutplan
        cbNum = c.CBNum
        cbT = arraynp(c[14:(14+cbNum)])  # CB Thicknesses
        # off = (offS + max(coordsOri.X[0])/100 - 1)/25
        off = offS/25
        off = max(coordsOri.X[0])*off
        rX = random()*off - off/2
        rY = random()*off - off/2
        coords = Coordinates(
            coordsOri.X,
            coordsOri.Y,
            coordsOri.Z,
            (coordsOri.Offset[0] + rX, coordsOri.Offset[1] + rY),
            coordsOri.OpenFace
        )

        # cant calculations
        cantH = sum(cbT) + (sum(cbT > 0)-1)*c.SecK  # centreboards
        cantH += (c.SecInSplitT+1) * \
            (c.SecInThickT+c.SecK*(c.SecInThickT > 0))  # secondary in top
        cantH += (c.SecInSplitB+1) * \
            (c.SecInThickB+c.SecK*(c.SecInThickB > 0))  # secondary in bot
        cantH += (c.SecOutSplitT+1) * \
            (c.SecOutThickT+c.SecK*(c.SecOutThickT > 0))  # secondary out top
        cantH += (c.SecOutSplitB+1) * \
            (c.SecOutThickB+c.SecK*(c.SecOutThickB > 0))  # secondary out bot

        cH = cantH/2

        # find group length
        if c.Description[5:7] == '41':
            bL = 4000
        else:
            bL = 4600

        # SECONDARY OUT TOP
        cH = self.FindRecovery(
            "SecOutT", coords, cH, bL,
            c.SecOutThickT, c.SecOutWidth/2, c.SecOutSplitT, c.SecK
        )

        # SECONDARY IN TOP
        cH = self.FindRecovery(
            "SecInT", coords, cH, bL,
            c.SecInThickT, c.SecInWidth/2, c.SecInSplitT, c.SecK
        )

        # CENTREBOARDS
        w = c.CBWidth/2  # CB Width
        hNum = c.HSNum + 1  # Number of horizontal saws
        hW = arraynp(c[37:(37+hNum)])  # HoriSaw board widths
        hK = list(c[41:(41+hNum-1)])  # Horizontal saw kerfs
        hK.append(0)
        for i in range(cbNum):
            t = cbT[i]
            if hNum > 1 and isnan(self.WB["CentreWB"][i]):
                hsW = -c.CBWidth/2 + hW[0]/2
                for j in range(hNum):
                    wane = GetWane(coords, cH, t, hW[j]/2)
                    self.CB[i][j] = min(wane) + 0.0  # recovery 0 if any wane
                    hsW = hsW + hW[j] + hK[j]
            else:
                wane = GetWane(coords, cH, t, w)
                if isnan(self.WB["CentreWB"][i]):
                    self.CB[i][0] = min(wane) + 0.0  # recovery 0 if any wane
                else:
                    self.WB["CentreWB"][i] = BoardRecovery(wane, coords.Z, bL)

            cH = cH - t - c.SecK

        # SECONDARY IN BOTTOM
        cH = self.FindRecovery(
            "SecInB", coords, cH, bL,
            c.SecInThickB, c.SecInWidth/2, c.SecInSplitB, c.SecK
        )

        # SECONDARY OUT BOTTOM
        cH = self.FindRecovery(
            "SecOutB", coords, cH, bL,
            c.SecOutThickB, c.SecOutWidth/2, c.SecOutSplitB, c.SecK
        )

        # PRIMARY IN
        cW = c.CBWidth/2
        t = c.PrimInThick
        w = c.PrimInWidth/2
        split = c.PrimInSplit
        if t > 0:
            cW = cW + c.PrimInK

            wane = GetWane(coords, cW+t, t, w, True)
            self.WB["PrimInR"][0] = BoardRecovery(wane, coords.Z, bL)
            wane = GetWane(coords, -cW, t, w, True)
            self.WB["PrimInL"][0] = BoardRecovery(wane, coords.Z, bL)

            cW = cW + t
        if split:
            cW = cW + c.PrimInK

            wane = GetWane(coords, cW+t, t, w, True)
            self.WB["PrimInR"][1] = BoardRecovery(wane, coords.Z, bL)
            wane = GetWane(coords, -cW, t, w, True)
            self.WB["PrimInL"][1] = BoardRecovery(wane, coords.Z, bL)

            cW = cW + t

        # PRIMARY OUT
        cW = c.CBWidth/2
        t = c.PrimOutThick
        w = c.PrimOutWidth/2
        split = c.PrimOutSplit
        if t > 0:
            cW = cW + c.PrimOutK

            wane = GetWane(coords, cW+t, t, w, True)
            self.WB["PrimOutR"][0] = BoardRecovery(wane, coords.Z, bL)
            wane = GetWane(coords, -cW, t, w, True)
            self.WB["PrimOutL"][0] = BoardRecovery(wane, coords.Z, bL)

            cW = cW + t
        if split:
            cW = cW + c.PrimOutK

            wane = GetWane(coords, cW+t, t, w, True)
            self.WB["PrimOutR"][1] = BoardRecovery(wane, coords.Z, bL)
            wane = GetWane(coords, -cW, t, w, True)
            self.WB["PrimOutL"][1] = BoardRecovery(wane, coords.Z, bL)

            cW = cW + t

        OF = cantH <= (coords.OpenFace[1] - coords.OpenFace[3])
        OF = OF and (cW*2 <= (coords.OpenFace[0] - coords.OpenFace[2]))

        return OF

    def FindRecovery(self, board, coords, cH, bL, t, w, split, k):
        if t > 0:
            wane = GetWane(coords, cH, t, w)
            self.WB[board][0] = BoardRecovery(wane, coords.Z, bL)
            cH = cH - t - k
        if split:
            wane = GetWane(coords, cH, t, w)
            self.WB[board][1] = BoardRecovery(wane, coords.Z, bL)
            cH = cH - t - k
        return cH

    def AddRecovery(self, r):
        # Get sum of WB
        for k in r.WB.keys():
            if len(r.WB[k]) > 0:
                for i in range(len(r.WB[k])):
                    self.WB[k][i] += r.WB[k][i]
        # Get sum of CB
        for i in range(len(r.CB)):
            if isnan(r.WB['CentreWB'][i]):
                for j in range(len(r.CB[i])):
                    self.CB[i][j] += r.CB[i][j]

    def AverageRecovery(self, numR):
        # Get average of WB
        for k in self.WB.keys():
            if len(self.WB[k]) > 0:
                for i in range(len(self.WB[k])):
                    self.WB[k][i] /= numR
        # Get average of CB
        for i in range(len(self.CB)):
            if isnan(self.WB['CentreWB'][i]):
                for j in range(len(self.CB[i])):
                    self.CB[i][j] /= numR

    def __repr__(self):
        return (
            "{:d} Centreboard(s) and {:d} Wingboard(s)".format(
                self.CBNum, self.WBNum)
        )


# Change coordinates from polar to cartesian system
def pol2cart(thetas, rhos, zs):
    X = rhos * cos(thetas)  # Get X coords
    Y = rhos * sin(thetas)  # Get Y coords
    Offset = [
        ((max(X)+min(X))/2),
        ((max(Y)+min(Y))/2)
    ]  # Offset so centre of log is (0,0)
    return Coordinates(X, Y, zs, Offset)


# given the recovery of each board, return total timber value per log
def CalcBoardVol(log, c, r):
    # Initialisations
    if c.HSNum > 0:
        cbW = arraynp(c[37:(37+c.HSNum+1)])  # HoriSaw widths
    else:
        cbW = c.CBWidth
    cbNum = c.CBNum
    cbT = arraynp(c[14:(14+cbNum)])  # CB Thicknesses
    if log.Length > 4400:
        gl = 4.6
    else:
        gl = 4

    # Wingboard volumes
    bVol = 0
    bVol += c.PrimOutWidth*c.PrimOutThick*gl*(
        sum(r.WB["PrimOutR"])+sum(r.WB["PrimOutL"]))
    bVol += c.PrimInWidth*c.PrimInThick*gl*(
        sum(r.WB["PrimInR"])+sum(r.WB["PrimInL"]))
    bVol += c.SecOutWidth*c.SecOutThickT*gl*(sum(r.WB["SecOutT"]))
    bVol += c.SecInWidth*c.SecInThickT*gl*(sum(r.WB["SecInT"]))
    bVol += c.SecOutWidth*c.SecOutThickB*gl*(sum(r.WB["SecOutB"]))
    bVol += c.SecInWidth*c.SecInThickB*gl*(sum(r.WB["SecInB"]))

    for i in range(cbNum):
        if isnan(r.WB["CentreWB"][i]):
            if c.HSNum > 0:
                bVol += sum(r.CB[i]*cbW*cbT[i]*gl)
            else:
                if len(r.CB[i]) > 0:
                    bVol += r.CB[i][0]*c.CBWidth*cbT[i]*gl
        else:
            bVol += r.WB["CentreWB"][i]*cbT[i]*c.CBWidth*gl

    return (bVol/1000000)


def EvalRecovery(pos, coords, r):
    temp = Coordinates(
        coords.X, coords.Y, coords.Z,
        (coords.Offset[0]+pos, coords.Offset[1])
    )
    r.RunRecovery(temp)
    sumR = SumRecov(r)
    return -sumR


# given the cutplan and coordinates of log, find offset for optimum recovery
def OptBoardPos(coords, c):
    w = max(coords.X)/10
    r = Recovery(c)

    opt = FindMin(EvalRecovery, bounds=(-w, w), method='bounded',
                  options={'xatol': 0.05}, args=(coords, r))
    coords.Offset[0] += opt.x
    return opt


# returns the coordinates for the log inputted with optimum offset based on c
def GetLogCoords(log, c, Opt=True):
    # Set up SED and LED circle coordinates in polar coordinates
    # AveSED = (log.SED+log.MinSED)/2
    # AveLED = (log.LED+log.MaxLED)/2
    # =========================================================================
    #     SEDpts = linspace(log.MinSED/2, log.SED/2, 26)
    #     LEDpts = linspace(log.LED/2, log.MaxLED/2, 26)
    #     SEDpts = hstack((SEDpts, SEDpts[-2::-1]))
    #     SEDpts = hstack((SEDpts, SEDpts[-2::-1]))
    #     LEDpts = hstack((LEDpts, LEDpts[-2::-1]))
    #     LEDpts = hstack((LEDpts, LEDpts[-2::-1]))
    #     z = linspace(0, log.Length, 50)
    #
    #     rhos = empty((SEDpts.shape[0], z.shape[0]))
    #     for i in range(SEDpts.shape[0]):
    #         # coordinates through the log with taper, in polar coordinates
    #         rhos[i, ] = linspace(SEDpts[i], LEDpts[i], z.shape[0])
    #
    #     thetas = transpose(repmat(linspace(0, 2*pi, 101), 50, 1))
    #     zs = repmat(z, 101, 1)
    # =========================================================================
    swPos = 1/3*log.Length
    z = append(arange(0, log.Length, 100), log.Length)
    thetas = linspace(0, 2*pi, 100)
    cos2 = cos(thetas)*cos(thetas)
    sin2 = sin(thetas)*sin(thetas)
    a = log.SED/2
    b = (log.MinSED+log.SED)/4
    if isnan(log.MinSED):
        b = log.SED/2
    rhosS = (a*b)/sqrt(b*b*cos2 + a*a*sin2)
    a = (log.MaxLED+log.LED)/4
    b = log.LED/2
    rhosL = (a*b)/sqrt(b*b*cos2 + a*a*sin2)
    rhos = empty((rhosS.shape[0], z.shape[0]))
    for i in range(rhosS.shape[0]):
        # coordinates through the log with taper, in polar coordinates
        rhos[i, ] = linspace(rhosS[i], rhosL[i], z.shape[0])
    thetas = transpose(repmat(thetas, len(z), 1))
    zs = repmat(z, rhosS.shape[0], 1)

    coords = pol2cart(thetas, rhos, zs)

    sweepY = 0
    if log.CompSweep > 0:
        # =====================================================================
        #         sweepY = interp1d(
        #             [0, log.Length/2, log.Length],
        #             [0, log.CompSweep*log.SED*0.01, 0]
        #         )(coords.Z)
        # =====================================================================
        a = -(log.CompSweep*log.SED*0.04)/(log.Length*log.Length)
        sweepY = a*coords.Z*(coords.Z-log.Length)

    def f_sweep(x):
        X = zeros(x.shape)
        a = -(log.Sweep*log.SED*0.01)/(swPos*swPos)
        i = x[x <= swPos]
        X[x <= swPos] = a*i*(i-2*swPos)
        a = (log.Sweep*log.SED*0.01)/(
            (swPos-log.Length)*(log.Length-swPos))
        i = x[x > swPos]
        X[x > swPos] = a*(i-log.Length)*(i-2*swPos+log.Length)
        return X

# =============================================================================
#     sweepX = interp1d(
#         [0, swPos, log.Length],
#         [0, log.Sweep*log.SED*0.01, 0],
#         kind='quadratic'
#     )(coords.Z)
# =============================================================================
    sweepX = f_sweep(coords.Z)

    of = GetOpenFace(log)
    coords.OpenFace[0] = of[0]
    coords.OpenFace[1] = of[1]
    coords.OpenFace[2] = -of[0]
    coords.OpenFace[3] = -of[1]
    minid = argmax(coords.X[50]+sweepX)
    if minid > 0:
        d = coords.Y[25:50, minid]

        # Open Face openface set here
        inout = d < (75/2)
        i = len(inout)-1
        while inout[i-1]:
            if i == 0:
                break
            else:
                i -= 1

    coords.X += sweepX
    coords.Y += sweepY

    if minid > 0:
        d = coords.X[25:50, minid]
        coords.OpenFace[2] = d[i]

    if Opt:
        OptBoardPos(coords, c)

    return coords


# Gets the max length to maintain open face
def GetOpenFace(log, openface=75):
    thetas = linspace(0, 0.5*pi, 100)
    cos2 = cos(thetas)*cos(thetas)
    sin2 = sin(thetas)*sin(thetas)
    a = log.SED/2
    b = (log.MinSED+log.SED)/4
    if isnan(log.MinSED):
        b = log.SED/2
    rhos = (a*b)/sqrt(b*b*cos2 + a*a*sin2)

    dx = cos(thetas)*rhos
    dy = sin(thetas)*rhos

    i = 0
    inout = dy < (openface/2)
    while inout[i+1]:
        if (i+2) == len(inout):
            i += 1
            break
        else:
            i += 1

    ofx = dx[i]

    i = len(inout)-1
    inout = dx < (openface/2)
    while inout[i-1]:
        if i == 1:
            i = 0
            break
        else:
            i -= 1

    ofy = dy[i]

    return (ofx, ofy)
