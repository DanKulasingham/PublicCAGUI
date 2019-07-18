"""
@author: Daniel Kulasingham

Helper functions
"""
import sys
from math import floor, ceil
from numpy import nansum, isnan, amin, amax, arctan2, sin, cos, sqrt, \
    max as npmax, argmin, logical_and, concatenate


def print_progress(
    iteration, total, prefix='', suffix='', decimals=1, bar_length=100
):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration  (Required): current iteration (Int)
        total      (Required): total iterations (Int)
        prefix     (Optional): prefix string (Str)
        suffix     (Optional): suffix string (Str)
        decimals   (Optional): +ve number of decimals in percent complete (Int)
        bar_length (Optional): character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    prtStr = '\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)

    if iteration == total:
        prtStr += '\n'

    return prtStr


# keep track to work out how much longer simulation will take
def Timer(id, ic, il, elapsed, tl=1000):
    total = len(id)*tl
    count = id.index(ic)*tl + il + 1
    t = (elapsed/count) * (total-count)
    tmin = floor(t/60)
    tsec = round(t % 60)
    if tmin > 0:
        tStr = \
            r'Time Remaining: {:d} min(s) {:d} sec(s)'.format(tmin, tsec)
    else:
        tStr = r'Time Remaining: {:d} sec(s)'.format(tsec)
    prtStr = print_progress(
        count, total,
        prefix="Cutplan "+str(id.index(ic)+1)+" of "+str(len(id))+":",
        suffix=" "+tStr+"          "
    )

    sys.stdout.write(prtStr)
    sys.stdout.flush()


# Evaluating how good recovery is
def SumRecov(recovery):
    rSum = 0
    for k in recovery.WB.keys():
        rSum += nansum(recovery.WB[k])
    for i in recovery.CB:
        if isinstance(i, list):
            rSum += nansum(i)
        elif not isnan(i):
            rSum += i
    return rSum


# finding the where board falls outside of log
def GetWane(coords, cH, t, w, prim=False):
    if prim:
        Y = coords.X
        X = coords.Y
        Offset = [coords.Offset[1], coords.Offset[0]]
    else:
        Y = coords.Y
        X = coords.X
        Offset = [coords.Offset[0], coords.Offset[1]]
    if cH > t/2:
        wane = (
            sum(
                (Y >= cH+Offset[1])
                * (X <= (-w+Offset[0]))
            ) * sum(
                (Y >= cH+Offset[1])
                * (X >= (w+Offset[0]))
            )
        ) > 0
    else:
        wane = (
            sum(
                (Y <= cH+Offset[1]-t)
                * (X <= (-w+Offset[0]))
            ) * sum(
                (Y <= cH+Offset[1]-t)
                * (X >= (w+Offset[0]))
            )
        ) > 0
    return wane


# given the affect of wane, determine cutback as percentage of board length
def BoardRecovery(wane, fullZ, bL):
    # Initialisations
    Z = fullZ[0]
    noWane = [0]
    startZ = 0
    for i in range(len(wane)):
        if not wane[i]:
            noWane.append(Z[i]-startZ)
            startZ = Z[i]
    noWane.append(Z[i]-startZ)

    newL = max(noWane)
    if bL == 4600:
        cutbacks = [4600, 3600, 3300, 3000]
    else:
        cutbacks = [4000, 3600, 3300, 3000]
    for i in range(len(cutbacks)):
        if newL >= cutbacks[i]:
            return cutbacks[i]/bL
    return 0


def CalcUseable(coords, length=None):
    # =========================================================================
    #     x = zeros(coords.X.shape[0])
    #     y = zeros(coords.Y.shape[0])
    #     for i in range(x.shape[0]):
    #         rhos = sqrt(coords.X[i]*coords.X[i] + coords.Y[i]*coords.Y[i])
    #         minID = 0
    #         for rID in range(len(rhos)):
    #             if rhos[rID] < rhos[minID]:
    #                 minID = rID
    #         x[i] = coords.X[i][minID]
    #         y[i] = coords.Y[i][minID]
    #     width = amax(x) - amin(x)
    #     height = amax(y) - amin(y)
    # =========================================================================

    rhos = sqrt(coords.X*coords.X + coords.Y*coords.Y)

    if length is None:
        minIDs = argmin(rhos, 1)
        x = [coords.X[i][minIDs[i]] for i in range(len(minIDs))]
        y = [coords.Y[i][minIDs[i]] for i in range(len(minIDs))]
        width = amax(x)-amin(x)
        height = amax(y)-amin(y)
    else:
        if length < 20:
            length *= 1000
        iLen = ceil(length/(coords.Z[0][1]-coords.Z[0][0])) + 1
        width = 0
        height = 0
        for i in range(coords.Z.shape[1]-iLen-1):
            minIDs = argmin(rhos[:, i:iLen+i], 1)
            x = [coords.X[j][minIDs[j]+i] for j in range(len(minIDs))]
            y = [coords.Y[j][minIDs[j]+i] for j in range(len(minIDs))]
            width = max(amax(x)-amin(x), width)
            height = max(amax(y)-amin(y), height)

    return (width, height)


def CalcUseableWID(coords, length=None):
    rhos = sqrt(coords.X*coords.X + coords.Y*coords.Y)

    if length < 20:
        length *= 1000
    iLen = ceil(length/(coords.Z[0][1]-coords.Z[0][0])) + 1
    width = 0
    minID = 0
    for i in range(coords.Z.shape[1]-iLen-1):
        minIDs = argmin(rhos[:, i:iLen+i], 1)
        x = [coords.X[j][minIDs[j]+i] for j in range(len(minIDs))]
        newW = amax(x)-amin(x)
        if newW > width:
            minID = i
            width = newW

    return minID


def GetUseableCoords(coords, length=None, lw=1.0):
    if length is None:
        rhos = sqrt(coords.X*coords.X + coords.Y*coords.Y)
        minIDs = argmin(rhos, 1)
        x = [coords.X[i][minIDs[i]] for i in range(len(minIDs))]
        y = [coords.Y[i][minIDs[i]] for i in range(len(minIDs))]
    else:
        rhos = sqrt(coords.X*coords.X + coords.Y*coords.Y)

        if length < 20:
            length *= 1000
        iLen = ceil(length/(coords.Z[0][1]-coords.Z[0][0])) + 1
        width = 0
        minID = 0
        for i in range(coords.Z.shape[1]-iLen-1):
            minIDs = argmin(rhos[:, i:iLen+i], 1)
            x = [coords.X[j][minIDs[j]+i] for j in range(len(minIDs))]
            newW = amax(x)-amin(x)
            if newW > width:
                minID = i
                width = newW

        xL = coords.X[:, minID]
        yL = coords.Y[:, minID]

        sweepID = argmin(-coords.X[0, :])
        xR = coords.X[:, sweepID]
        yR = coords.Y[:, sweepID]

        idsR = [i for i in range(xR.shape[0]) if any(
            logical_and(xR[i] <= xL, abs(yR[i]) <= abs(yL)))]
        idsL = [i for i in range(xL.shape[0]) if any(
            logical_and(xL[i] >= xR, abs(yL[i]) <= abs(yR)))]

        if len(idsL) == coords.X.shape[0]:
            x = xL
            y = yL
        else:
            x = [xL[idsL[0]]]
            y = [yL[idsL[0]]]
            i = 1
            while (idsL[i]-idsL[i-1] == 1):
                x.append(xL[idsL[i]])
                y.append(yL[idsL[i]])
                i += 1
            x = concatenate([x, xR[idsR], xL[idsL[i:]]])
            y = concatenate([y, yR[idsR], yL[idsL[i:]]])

    thetas = arctan2(y, x)
    x1 = x - lw*cos(thetas)
    y1 = y - lw*sin(thetas)

    origin = (coords.Offset[0], coords.Offset[1], npmax(coords.Z))

    return ((x, y), (x1, y1), origin)
