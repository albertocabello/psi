#!/usr/bin/python
#-*- coding: utf-8 -*-

import wx
from wx import xrc
from wx import grid
from psi import analysis
from psi import graphics
import psi.properties_manager as pm
from psi import ui


class PSI(wx.App):

    def OnInit(self):
        self.props = pm.XMLProperties()
        self.props.Open('properties.xml')
        self.res = xrc.XmlResource(u'main_grid.xrc')
        self.frame = self.res.LoadFrame(None, u'MainFrame')
        self.main_grid = xrc.XRCCTRL(self.frame, u'MainGrid')
        self.main_grid.CreateGrid(1000, 26)
        self.main_grid.EnableDragRowSize(False)
        self.main_grid.EnableDragColSize(False)
        self.frame.Bind(wx.EVT_MENU, self.PrintSelectedCells,
                        id = xrc.XRCID(u'Print'))
        self.frame.Bind(wx.EVT_MENU, self.Close,
                        id = xrc.XRCID(u'Quit'))
        self.frame.Bind(wx.EVT_MENU, self.OpenFile,
                        id = xrc.XRCID(u'Open'))
        self.frame.Bind(wx.EVT_MENU, self.ShowStyleDialog,
                                id = xrc.XRCID(u'DrawingStyle'))
        self.frame.Bind(wx.EVT_MENU, self.LR,
                                id = xrc.XRCID(u'LR'))
        self.frame.Bind(wx.EVT_MENU, self.Descriptive,
                                id = xrc.XRCID(u'DescStats'))
        aboutDialog = self.res.LoadDialog(self.frame, u'AboutDialog')
        self.frame.Bind(wx.EVT_MENU, lambda x: aboutDialog.ShowModal(),
                                id = xrc.XRCID(u'About'))
        self.frame.SetDimensions(int(self.props[(u'main-window',
                                                 u'x-position')]),
                                 int(self.props[(u'main-window',
                                                 u'y-position')]),
                                 int(self.props[(u'main-window',
                                                 u'x-size')]),
                                 int(self.props[(u'main-window',
                                                 u'y-size')]))
        self.frame.Show()
        self.result = ui.Result(self.frame, self.props)
        # self.result.text = xrc.XRCCTRL(self.results, u'ResultText')
        # self.result.graph = xrc.XRCCTRL(self.results, u'ResultGraph')
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
            None
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

    def LR(self, e):
        analyst = analysis.LinearRegression()
        if analyst.LoadData(self.main_grid.GetSelectedCellsList('N')):
            self.result.text.Clear()
            if analyst.Calculate():
                analyst.PrintResult(self.result.text)
                self.result.graph.DrawGrid()
                style = graphics.Style(self.props)
                analyst.DoDrawing(self.result.graph, style)
                self.result.Show()

    def Descriptive(self, e):
        analyst = analysis.BasicStatistics()
        if analyst.LoadData(self.main_grid.GetSelectedCellsList('N')):
            self.result.text.Clear()
            if analyst.Calculate():
                analyst.PrintResult(self.result.text)

if __name__ == '__main__':
    app = PSI(False)
    app.MainLoop()
