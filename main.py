#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
from wx import xrc
from wx import grid
import Analysis
import Graphics
import Properties
import PSIui


class PSI(wx.App):

    def OnInit(self):
        self.props = Properties.XMLProperties()
        self.props.Open('properties.xml')
        self.res = xrc.XmlResource(u'mainGrid.xrc')
        self.frame = self.res.LoadFrame(None, u'MainFrame')
        self.mainGrid = xrc.XRCCTRL(self.frame, u'MainGrid')
        self.mainGrid.CreateGrid(1000, 26)
        self.mainGrid.EnableDragRowSize(False)
        self.mainGrid.EnableDragColSize(False)
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
        self.frame.SetDimensions(int(self.props.GetProperty(u'main-window',
                                                            u'x-position')),
                                 int(self.props.GetProperty(u'main-window',
                                                            u'y-position')),
                                 int(self.props.GetProperty(u'main-window',
                                                            u'x-size')),
                                 int(self.props.GetProperty(u'main-window',
                                                            u'y-size')))
        self.frame.Show()
        self.results = PSIui.Result(self.frame, self.props)
        self.ResultText = xrc.XRCCTRL(self.results, u'ResultText')
        self.ResultGraph = xrc.XRCCTRL(self.results, u'ResultGraph')
        self.results.Show()
        return True

    def PrintSelectedCells(self, e):
        print 'Printing selected cells:'
        for i in self.mainGrid.GetSelectedCellsList('N'):
            print i

    def ShowStyleDialog(self, e):
        styleDialog = PSIui.StyleDialog(self.frame, self.props)
        self.ResultText.SetFont(styleDialog.newFont)
        styleDialog.Destroy()

    def Close(self, e):
        print 'Closing application...'
        (x, y) = self.frame.GetPosition()
        self.props.SetProperty(u'main-window', u'x-position', x)
        self.props.SetProperty(u'main-window', u'y-position', y)
        (w, h) = self.frame.GetSize()
        self.props.SetProperty(u'main-window', u'x-size', w)
        self.props.SetProperty(u'main-window', u'y-size', h)
        self.props.Save()
        try:
            self.results.Close(False)
        except:
            # Results window could have been closed before
            None
        self.frame.Close(False)

    def OpenFile(self, e):
        print 'About to open file...'
        fd = wx.FileDialog(None, style = wx.OPEN,
                           wildcard = 'CSV files (.csv)|*.csv')
        if fd.ShowModal() == wx.ID_OK:
            # sd = self.res.LoadDialog(None, 'OpenDialog')
            # sd.ShowModal()
            sv = wx.SingleChoiceDialog(None, 'Separator',
                                       'Choose a separator',
                                        choices = [',', ';', ':'])
            if sv.ShowModal() == wx.ID_OK:
                path = fd.GetPath()
                self.mainGrid.LoadCSV(path,
                                      separator = sv.GetStringSelection())
                sv.Destroy()

    def LR(self, e):
        analyst = Analysis.LinearRegression()
        if analyst.LoadData(self.mainGrid.GetSelectedCellsList('N')):
            self.ResultText.Clear()
            if analyst.Calculate():
                analyst.PrintResult(self.ResultText)
                self.ResultGraph.DrawGrid()
                style = Graphics.Style(self.props)
                analyst.DoDrawing(self.ResultGraph, style)
                self.results.Show()

    def Descriptive(self, e):
        analyst = Analysis.BasicStatistics()
        if analyst.LoadData(self.mainGrid.GetSelectedCellsList('N')):
            self.ResultText.Clear()
            if analyst.Calculate():
                analyst.PrintResult(self.ResultText)

if __name__ == '__main__':
    app = PSI(False)
    app.MainLoop()
