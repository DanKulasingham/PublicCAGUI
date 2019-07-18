"""
@author: Daniel Kulasingham

Class to plot log and cutplan
"""
from numpy import array as nparr, transpose, isnan, max as npmax, linspace
from mayavi import mlab
from cutplan._coordinates import GetLogCoords
from cutplan._helper import GetUseableCoords


class LogPlotter(object):
    def __init__(self, scene, c, coords=None, LD=None, view=False, unit=False):
        self.hasData = False
        self.logID = -1
        self.log = None
        self.Cutplan = c
        self.plotExists = False
        self.showText = True
        self.showPerc = unit
        self.showFront = view
        self.scene = scene
        if coords is None and LD is None:
            raise ValueError(
                'ERROR: Either log coordinates or log data file required.')
        elif coords is None:
            self.LD = LD
            self.hasData = True

        if LD is None:
            self.coords = coords
        else:
            self.logID = 0
            self.coords = GetLogCoords(LD.iloc[0], c)

        self.bL = npmax(self.coords.Z)

        return

    def PlotLog(self, opacity=0.8):
        col1 = (100, 60, 5)
        col2 = (190, 110, 40)
        self.log = self.scene.mlab.mesh(
            self.coords.X, self.coords.Y, self.coords.Z
        )
        r = linspace(col2[0], col1[0], 255)
        g = linspace(col2[1], col1[1], 255)
        b = linspace(col2[2], col1[2], 255)
        alphas = [opacity*255]*255
        self.log.module_manager.scalar_lut_manager.lut.table = transpose([
            r, g, b, alphas
        ])
        self.log.actor.property.lighting = False

        fig = mlab.gcf()

        mlab.figure(figure=fig, bgcolor=(0.83, 0.83, 0.83))
        self.scene.parallel_projection = True
        # self.FrontView()

        return

    def PlotBoard(self, coords, bW, bH, colour):
        w = bW/2
        h = bH/2
        x = coords[0]
        y = coords[1]
        z = coords[2]

        self.scene.mlab.mesh(
            transpose(nparr([[x-w, x-w, x+w, x+w, x-w]]*2)),
            transpose(nparr([[y-h, y+h, y+h, y-h, y-h]]*2)),
            transpose(nparr([[0, 0, 0, 0, 0], [z, z, z, z, z]])),
            color=colour
        )
        self.scene.mlab.mesh(
            transpose(nparr([
                [x-w, x-w, x-w, x-w, x-w], [x+w, x+w, x+w, x+w, x+w]
            ])),
            transpose(nparr([[y-h, y+h, y+h, y-h, y-h]]*2)),
            transpose(nparr([[0, 0, z, z, 0]]*2)),
            color=colour
        )

        return

    def SetCoords(self, newCoords):
        self.coords = newCoords
        return

    def GetRColour(self, recovery, bType, bNum=0, color=True):
        if recovery == -1:
            if bType == "CB":
                return (0, 1, 0)
            elif bType[:4] == "Prim":
                return (1, 0, 0)
            else:
                return (0, 0, 1)
        if bType == "CB":
            if isnan(recovery.WB["CentreWB"][bNum]):
                r = recovery.CB[bNum][0]
            else:
                r = recovery.WB["CentreWB"][bNum]
        else:
            r = recovery.WB[bType][bNum]
        col = (min((2*(1-r), 1)), r, 0)
        if color:
            return col
        else:
            return "{:.1f}%".format(r*100)

    def SecDraw(self, coords, r, w, t, k, bL, cH, split, bType):
        if w*t > 0:
            xyz = (coords.Offset[0], cH-t/2+coords.Offset[1], bL)
            rCol = self.GetRColour(r, bType)
            self.PlotBoard(xyz, w, t, rCol)
            cH -= t + k
            if split:
                xyz = (coords.Offset[0], cH-t/2+coords.Offset[1], bL)
                rCol = self.GetRColour(r, bType, 1)
                self.PlotBoard(xyz, w, t, rCol)
                cH -= t + k
        return cH

    def SecText(self, coords, r, w, t, k, bL, cH, split, bType):
        if w*t > 0:
            rText = self.GetRColour(r, bType, color=False)
            s = min([w/len(rText)+1, t*0.6])
            xyz = (coords.Offset[0], cH-t/2+coords.Offset[1], s)
            self.PlotText(xyz, w, t, rText)
            cH -= t + k
            if split:
                rText = self.GetRColour(r, bType, 1, color=False)
                s = min([w/len(rText)+1, t*0.6])
                xyz = (coords.Offset[0], cH-t/2+coords.Offset[1], s)
                self.PlotText(xyz, w, t, rText)
                cH -= t + k

    def PlotText(self, coords, bW, bH, rText, prim=0):
        r = float(rText[:-1])/100
        col = (min((2*(1-r), 1)), r, 0)
        col = (col[0]*0.6, col[1]*0.6, col[2]*0.6)

        s = coords[2]
        sp = 0.5
        if not self.showPerc:
            rText = "{:.0f}x{:.0f}".format(bW, bH)
            s = min([bW/(len(rText)+1), bH*0.6])
            sp = 0.5

        if bH > bW:
            s = min([bH/(len(rText)+1), bW*0.6])
            prim = 1

        if prim == 0:
            ori = (0, 180, 180)
            x = coords[0] - (s*(len(rText)-sp))/2
            y = coords[1] + s/2
            z = -2
        elif prim == 2:
            ori = (180, 0, 90)
            x = coords[0] - s/2
            y = coords[1] - (s*(len(rText)-sp))/2
            z = -2
        elif prim == 1:
            ori = (180, 0, 270)
            x = coords[0] + s/2
            y = coords[1] + (s*(len(rText)-sp))/2
            z = -2

        if self.showText:
            self.scene.mlab.text3d(
                x, y, z, rText,
                orient_to_camera=False,
                orientation=ori,
                color=col,
                scale=(s, s, s)
            )

        return

    def ShowBoards(self, r=-1):
        # initialisations
        coords = self.coords
        uC = GetUseableCoords(coords)
        coords.Offset[0] = (min(uC[0][0])+max(uC[0][0]))/2
        coords.Offset[1] = (min(uC[0][1])+max(uC[0][1]))/2
        c = self.Cutplan
        cbNum = c.CBNum
        cbT = nparr(c[14:(14+cbNum)])  # CB Thicknesses

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

        # find board length
        bL = npmax(coords.Z)

        # SECONDARY OUT TOP
        t = c.SecOutThickT
        w = c.SecOutWidth
        k = c.SecK
        split = c.SecOutSplitT
        self.SecText(coords, r, w, t, k, bL, cH, split, "SecOutT")
        cH = self.SecDraw(coords, r, w, t, k, bL, cH, split, "SecOutT")

        # SECONDARY IN TOP
        t = c.SecInThickT
        w = c.SecInWidth
        k = c.SecK
        split = c.SecInSplitT
        self.SecText(coords, r, w, t, k, bL, cH, split, "SecInT")
        cH = self.SecDraw(coords, r, w, t, k, bL, cH, split, "SecInT")

        # CENTREBOARDS
        w = c.CBWidth  # CB Width
        hNum = c.HSNum + 1  # Number of horizontal saws
        hW = nparr(c[37:(37+hNum)])  # HoriSaw board widths
        hK = list(c[41:(41+hNum-1)])  # Horizontal saw kerfs
        hK.append(0)
        for i in range(cbNum):
            t = cbT[i]
            if hNum > 1 and isnan(r.WB["CentreWB"][i]):
                hsW = -c.CBWidth/2 + hW[0]/2
                for j in range(hNum):
                    xyz = (hsW+coords.Offset[0], cH-t/2+coords.Offset[1], bL)
                    if r == -1:
                        rCol = (0.0, 1.0, 0.0)
                    else:
                        rCol = (min((2*(1-r.CB[i][j]), 1)), r.CB[i][j], 0)
                    self.PlotBoard(xyz, hW[j], t, rCol)
                    rText = "{:.1f}%".format(r.CB[i][j]*100)
                    s = min([hW[j]/len(rText)+1, t*0.6])
                    xyz = (xyz[0], xyz[1], s)
                    self.PlotText(xyz, hW[j], t, rText)
                    hsW += hW[j] + hK[j]
            else:
                xyz = (coords.Offset[0], cH-t/2+coords.Offset[1], bL)
                rCol = self.GetRColour(r, "CB", i)
                self.PlotBoard(xyz, w, t, rCol)
                rText = self.GetRColour(r, "CB", i, color=False)
                s = min([w/len(rText)+1, t*0.6])
                xyz = (xyz[0], xyz[1], s)
                self.PlotText(xyz, w, t, rText)
            cH -= t + c.SecK

        # SECONDARY IN BOTTOM
        t = c.SecInThickB
        w = c.SecInWidth
        k = c.SecK
        split = c.SecInSplitB
        self.SecText(coords, r, w, t, k, bL, cH, split, "SecInB")
        cH = self.SecDraw(coords, r, w, t, k, bL, cH, split, "SecInB")

        # SECONDARY OUT BOTTOM
        t = c.SecOutThickB
        w = c.SecOutWidth
        k = c.SecK
        split = c.SecOutSplitB
        self.SecText(coords, r, w, t, k, bL, cH, split, "SecOutB")
        cH = self.SecDraw(coords, r, w, t, k, bL, cH, split, "SecOutB")

        # PRIMARY IN
        cW = c.CBWidth/2
        t = c.PrimInThick
        w = c.PrimInWidth
        split = c.PrimInSplit
        if w > 0:
            cW += c.PrimInK

            # LEFT
            xyz = (-cW-t/2+coords.Offset[0], coords.Offset[1], bL)
            rCol = self.GetRColour(r, "PrimInL")
            self.PlotBoard(xyz, t, w, rCol)
            rText = self.GetRColour(r, "PrimInL", color=False)
            s = min([w/len(rText)+1, t*0.6])
            xyz = (xyz[0], xyz[1], s)
            self.PlotText(xyz, w, t, rText, prim=1)
            # RIGHT
            xyz = (cW+t/2+coords.Offset[0], coords.Offset[1], bL)
            rCol = self.GetRColour(r, "PrimInR")
            self.PlotBoard(xyz, t, w, rCol)
            rText = self.GetRColour(r, "PrimInR", color=False)
            s = min([w/len(rText)+1, t*0.6])
            xyz = (xyz[0], xyz[1], s)
            self.PlotText(xyz, w, t, rText, prim=2)

            cW += t
        if split:
            cW += c.PrimInK

            # LEFT
            xyz = (-cW-t/2+coords.Offset[0], coords.Offset[1], bL)
            rCol = self.GetRColour(r, "PrimInL", 1)
            self.PlotBoard(xyz, t, w, rCol)
            rText = self.GetRColour(r, "PrimInL", 1, color=False)
            s = min([w/len(rText)+1, t*0.6])
            xyz = (xyz[0], xyz[1], s)
            self.PlotText(xyz, w, t, rText, prim=1)
            # RIGHT
            xyz = (cW+t/2+coords.Offset[0], coords.Offset[1], bL)
            rCol = self.GetRColour(r, "PrimInR", 1)
            self.PlotBoard(xyz, t, w, rCol)
            rText = self.GetRColour(r, "PrimInR", 1, color=False)
            s = min([w/len(rText)+1, t*0.6])
            xyz = (xyz[0], xyz[1], s)
            self.PlotText(xyz, w, t, rText, prim=2)

            cW += t

        # PRIMARY OUT
        t = c.PrimOutThick
        w = c.PrimOutWidth
        split = c.PrimOutSplit
        if w > 0:
            cW += c.PrimOutK

            # LEFT
            xyz = (-cW-t/2+coords.Offset[0], coords.Offset[1], bL)
            rCol = self.GetRColour(r, "PrimOutL")
            self.PlotBoard(xyz, t, w, rCol)
            rText = self.GetRColour(r, "PrimOutL", color=False)
            s = min([w/len(rText)+1, t*0.6])
            xyz = (xyz[0], xyz[1], s)
            self.PlotText(xyz, w, t, rText, prim=1)
            # RIGHT
            xyz = (cW+t/2+coords.Offset[0], coords.Offset[1], bL)
            rCol = self.GetRColour(r, "PrimOutR")
            self.PlotBoard(xyz, t, w, rCol)
            rText = self.GetRColour(r, "PrimOutR", color=False)
            s = min([w/len(rText)+1, t*0.6])
            xyz = (xyz[0], xyz[1], s)
            self.PlotText(xyz, w, t, rText, prim=2)

            cW += t
        if split:
            cW += c.PrimOutK

            # LEFT
            xyz = (-cW-t/2+coords.Offset[0], coords.Offset[1], bL)
            rCol = self.GetRColour(r, "PrimOutL", 1)
            self.PlotBoard(xyz, t, w, rCol)
            rText = self.GetRColour(r, "PrimOutL", 1, color=False)
            s = min([w/len(rText)+1, t*0.6])
            xyz = (xyz[0], xyz[1], s)
            self.PlotText(xyz, w, t, rText, prim=1)
            # RIGHT
            xyz = (cW+t/2+coords.Offset[0], coords.Offset[1], bL)
            rCol = self.GetRColour(r, "PrimOutR", 1)
            self.PlotBoard(xyz, t, w, rCol)
            rText = self.GetRColour(r, "PrimOutR", 1, color=False)
            s = min([w/len(rText)+1, t*0.6])
            xyz = (xyz[0], xyz[1], s)
            self.PlotText(xyz, w, t, rText, prim=2)
        return

    def ShowUseable(self, useable, colour=(0, 0, 1)):
        coords = useable[2]
        z = coords[2]
        x = useable[0][0]
        y = useable[0][1]
        x1 = useable[1][0]
        y1 = useable[1][1]

        X = [x, x1, x1, x]
        Y = [y, y1, y1, y]
        Z = [
            [0]*len(x), [0]*len(x), [z]*len(x), [z]*len(x)
        ]

        self.scene.mlab.mesh(
            transpose(nparr(X)),
            transpose(nparr(Y)),
            transpose(nparr(Z)),
            color=colour, opacity=0.8
        )
        return

    def ShowOval(
        self, useable, coords, cbL=None, colour=(1, 0.2, 0.2), lw=1.0
    ):
        cs, cs1, origin = GetUseableCoords(coords)
        offX = (min(cs[0])+max(cs[0]))/2
        offY = (min(cs[1])+max(cs[1]))/2
        tempC = GetLogCoords(useable, None, False)
        cs, cs1, origin = GetUseableCoords(tempC, cbL, lw)
        # z = npmax(coords.Z)
        offX1 = (min(cs[0])+max(cs[0]))/2
        offY1 = (min(cs[1])+max(cs[1]))/2

# =============================================================================
#         rhos = linspace(w, h, 26)
#         rhos = hstack((rhos, rhos[-2::-1]))
#         rhos = hstack((rhos, rhos[-2::-1]))
# =============================================================================

# =============================================================================
#         thetas = linspace(0, 2*pi, 100)
#         bcos = b*cos(thetas)
#         asin = a*sin(thetas)
#         rhos = (a*b)/sqrt(bcos*bcos + asin*asin)
#         Z = [[0]*len(rhos), [0]*len(rhos), [z]*len(rhos), [z]*len(rhos)]
#         rhos1 = rhos-lw
#
#         x = rhos*cos(thetas) + offX
#         x1 = rhos1*cos(thetas) + offX
#         y = rhos*sin(thetas) + offY
#         y1 = rhos1*sin(thetas) + offY
# =============================================================================

        x = cs[0]-offX1+offX
        y = cs[1]-offY1+offY
        x1 = cs1[0]-offX1+offX
        y1 = cs1[1]-offY1+offY
        Z = [[0]*len(x), [0]*len(x), [2]*len(x), [2]*len(x)]

        X = [x, x1, x1, x]
        Y = [y, y1, y1, y]
        self.scene.mlab.mesh(
            transpose(nparr(X)),
            transpose(nparr(Y)),
            transpose(nparr(Z)),
            color=colour
        )
        return

    def FrontView(self):
        if self.showFront:
            self.scene.mlab.view(azimuth=180, elevation=180)
            if self.log is not None:
                self.log.scene.camera.zoom(7.5)
        else:
            self.scene.mlab.view(azimuth=165, elevation=181.5, roll=180)
            if self.log is not None:
                self.log.scene.camera.zoom(7)
        return
