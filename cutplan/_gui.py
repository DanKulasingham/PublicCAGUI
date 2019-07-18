# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 13:33:04 2019

@author: Daniel
"""
from cutplan._coordinates import GetLogCoords
from cutplan._logplotter import LogPlotter

from traits.api import HasTraits, Instance, Button, on_trait_change
from traitsui.api import View, Item, Group
from mayavi.core.ui.api import MlabSceneModel
from tvtk.pyface.api import Scene
from tvtk.pyface.scene_editor import SceneEditor


class LogPlotGUI(HasTraits):

    scene = Instance(MlabSceneModel, ())

    button1 = Button('Reset')

    def __init__(self, cpSchedule, logPath, id=0):
        HasTraits.__init__(self)
        self.id = id

        self.logPath = logPath
        self.CPSched = cpSchedule
        self.AveR = cpSchedule.AveR

        self.showLog = True
        self.showBoards = True
        self.showFL = False
        self.show3m = False
        self.showPerc = False
        self.showFront = False

        if self.CPSched.Cutplans.shape[0] > 0:
            c = self.CPSched.Cutplans.iloc[self.id]
            log = self.CPSched.AverageLog(self.id)
            self.scene.mlab.clf()
            self.coords = GetLogCoords(log, c)
            self.myOff = self.coords.Offset
            self.plotter = LogPlotter(self.scene, c, self.coords)
            self.plotter.PlotLog()
        else:
            c = None
            self.plotter = None

    @on_trait_change('scene.activated')
    def scene_load(self):
        self.plotter.FrontView()

    def redraw_scene(self):
        # Notice how each mlab call points explicitely to the figure it
        # applies to.

        # CURRENTLY CAN ONLY OPEN FIRST CUTPLAN IN SCHEDULE
        c = self.CPSched.Cutplans.iloc[self.id]
        log = self.CPSched.AverageLog(self.id)
        self.scene.mlab.clf()
        self.coords = GetLogCoords(log, c, False)
        self.myOff = self.coords.Offset
        self.plotter = LogPlotter(
            self.scene, c, self.coords,
            view=self.showFront, unit=self.showPerc)
        self.plotter.PlotLog(0.9*self.showLog)
        if self.showBoards and self.CPSched.completed[self.id]:
            self.plotter.ShowBoards(self.AveR[self.id])
        # uC1 = (self.CPSched.MinW[id][0], self.CPSched.MinH[id][0])
        if self.showFL and self.CPSched.completed[self.id]:
            uC1 = self.CPSched.GetMinWLog(self.id, 0)
            self.plotter.ShowOval(uC1, self.coords)
        # uC2 = (self.CPSched.MinW[id][1], self.CPSched.MinH[id][1])
        if self.show3m and self.CPSched.completed[self.id]:
            uC2 = self.CPSched.GetMinWLog(self.id, 1)
            self.plotter.ShowOval(
                uC2, self.coords, cbL=3, colour=(0.75, 0.1, 0.1))
        self.plotter.FrontView()

    # The layout of the dialog created
    view = View(Group(
            Item(
                'scene', editor=SceneEditor(scene_class=Scene),
                resizable=False), show_labels=False))
