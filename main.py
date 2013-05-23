#!/usr/bin/python
#-*- coding: utf-8 -*-

import wx.xrc
from psi import analysis
from psi import graphics
import psi.properties_manager as pm
from psi import ui


class PSI(wx.App):

    def OnInit(self):
        self.props = pm.XMLProperties()
        self.props.Open('properties.xml')
        self.res = wx.xrc.XmlResource(u'main_grid.xrc')
        self.frame = self.res.LoadFrame(None, u'MainFrame')
        self.frame.SetDimensions(int(self.props[(u'main-window',
                                                 u'x-position')]),
                                 int(self.props[(u'main-window',
                                                 u'y-position')]),
                                 int(self.props[(u'main-window',
                                                 u'x-size')]),
                                 int(self.props[(u'main-window',
                                                 u'y-size')]))
        self.main_grid = ui.ctrl(self.frame, u'MainGrid')
        self.main_grid.CreateGrid(1000, 26)
        self.main_grid.EnableDragRowSize(False)
        self.main_grid.EnableDragColSize(False)
        self.frame.Bind(wx.EVT_MENU, self.PrintSelectedCells,
                            id=wx.xrc.XRCID(u'Print'))
        self.frame.Bind(wx.EVT_MENU, self.Close,
                            id=wx.xrc.XRCID(u'Quit'))
        self.frame.Bind(wx.EVT_MENU, self.OpenFile,
                            id=wx.xrc.XRCID(u'Open'))
        self.frame.Bind(wx.EVT_MENU, self.ShowStyleDialog,
                            id=wx.xrc.XRCID(u'DrawingStyle'))
        self.frame.Bind(wx.EVT_MENU, self.LinearRegression,
                            id=wx.xrc.XRCID(u'LinReg'))
        self.frame.Bind(wx.EVT_MENU, self.BasicStatistics,
                            id=wx.xrc.XRCID(u'DescStats'))
        self.frame.Bind(wx.EVT_MENU, self.HeatMap,
                            id=wx.xrc.XRCID(u'HeatMap'))
        aboutDialog = self.res.LoadDialog(self.frame, u'AboutDialog')
        self.frame.Bind(wx.EVT_MENU, lambda x: aboutDialog.ShowModal(),
                            id=wx.xrc.XRCID(u'About'))
        self.frame.Show()
        self.result = ui.Result(self.frame, self.props)
        self.result.Show()
        return True

    def PrintSelectedCells(self, e):
        print 'Printing selected cells:'
        for i in self.main_grid.GetSelectedCellsList('N'):
            print i

    def ShowStyleDialog(self, e):
        style_dialog = ui.StyleDialog(self.frame, self.props)
        self.result.text.SetFont(style_dialog.result_text_label.GetFont())
        self.result.graph.SetFont(style_dialog.graph_text_label.GetFont())
        style_dialog.Destroy()

    def Close(self, e):
        print 'Closing application...'
        (x, y) = self.frame.GetPosition()
        self.props[(u'main-window', u'x-position')] = x
        self.props[(u'main-window', u'y-position')] = y
        (w, h) = self.frame.GetSize()
        self.props[(u'main-window', u'x-size')] = w
        self.props[(u'main-window', u'y-size')] = h
        self.props.Save()
        try:
            self.results.Close(False)
        except:
            # Results window could have been closed before
            pass
        self.frame.Close(False)

    def OpenFile(self, e):
        print 'About to open file...'
        fd = wx.FileDialog(None, style=wx.OPEN,
                           wildcard='CSV files (.csv)|*.csv')
        if fd.ShowModal() == wx.ID_OK:
            # sd = self.res.LoadDialog(None, 'OpenDialog')
            # sd.ShowModal()
            sv = wx.SingleChoiceDialog(None, 'Separator',
                                       'Choose a separator',
                                        choices = [',', ';', ':'])
            if sv.ShowModal() == wx.ID_OK:
                path = fd.GetPath()
                self.main_grid.LoadCSV(path,
                                      separator = sv.GetStringSelection())
                sv.Destroy()

    def LinearRegression(self, e):
        analyst = analysis.LinearRegression()
        if analyst.LoadData(self.main_grid.GetSelectedCellsList('N')):
            if analyst.Calculate():
                self.result.text.Clear()
                analyst.PrintResult(self.result.text)
                analyst.DoDrawing(self.result.graph,
                                    graphics.Style(self.props))

    def BasicStatistics(self, e):
        analyst = analysis.BasicStatistics()
        if analyst.LoadData(self.main_grid.GetSelectedCellsList('N')):
            if analyst.Calculate():
                self.result.text.Clear()
                analyst.PrintResult(self.result.text)
                analyst.DoDrawing(self.result.graph,
                                    graphics.Style(self.props))

    def HeatMap(self, e):
        analyst = analysis.HeatMap()
        if analyst.LoadData(self.main_grid.GetSelectedCellsList('N')):
            if analyst.Calculate():
                self.result.text.Clear()
                analyst.PrintResult(self.result.text)
                analyst.DoDrawing(self.result.graph,
                                    graphics.Style(self.props))

if __name__ == '__main__':
    app = PSI(False)
    app.MainLoop()
