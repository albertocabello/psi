#!/usr/bin/python
# -*- coding: utf-8 -*-
import wx
from wx import xrc
from wx import grid
import Analysis
import Graphics
import Math
import Properties
import PSIui


class PSI(wx.App):

    def OnInit(self):
        self.props = Properties.XMLProperties()
        self.props.Open('properties.xml')
        self.res = xrc.XmlResource(u'mainGrid.xrc')
        self.frame = self.res.LoadFrame(None, u'mainFrame')
        self.AboutDialog = self.res.LoadDialog(self.frame, u'AboutDialog')
        self.mainGrid = xrc.XRCCTRL(self.frame, u'mainGrid')
        self.mainGrid.CreateGrid(1000, 26)
        self.mainGrid.EnableDragRowSize(False)
        self.mainGrid.EnableDragColSize(False)
        self.frame.Bind(wx.EVT_MENU, self.PrintSelectedCells,
                        id = xrc.XRCID(u'Print'))
        self.frame.Bind(wx.EVT_MENU, self.Close,
                        id = xrc.XRCID(u'Quit'))
        self.frame.Bind(wx.EVT_MENU, self.OpenFile,
                        id = xrc.XRCID(u'Open'))
        self.frame.Bind(wx.EVT_MENU, self.DoLR,
                        id = xrc.XRCID(u'LR'))
        self.frame.Bind(wx.EVT_MENU, lambda x: self.AboutDialog.Show(),
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

    def DoLR(self, e):
        print 'Linear Regression:'
        analyst = Analysis.LinearRegression()
        if analyst.LoadData(self.mainGrid.GetSelectedCellsList('N')):
            self.ResultText.Clear()
            Result = analyst.Calculate()
            summary = "Y = {0:.2}*X + {1:.2}\n".format(Result['slope'],
                                                       Result['intercept'])
            self.ResultText.AppendText(summary)
            for i in Result.keys():
                self.ResultText.AppendText("{0}: {1}\n".format(i, Result[i]))
            self.ResultGraph.DrawGrid()
            style = {}
            style['dots_color'] = wx.Color(128, 128, 0)
            style['dots_radius'] = 3
            style['line_color'] = wx.Color(128, 0, 128)
            style['line_width'] = 2
            analyst.DoDrawing(self.ResultGraph, style)
            self.results.Show()

if __name__ == '__main__':
    app = PSI(False)
    app.MainLoop()
