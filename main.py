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
        self.frame.SetDimensions(int(self.props.GetProperty(u'main-window',
                                                            u'x-position')),
                                 int(self.props.GetProperty(u'main-window',
                                                            u'y-position')),
                                 int(self.props.GetProperty(u'main-window',
                                                            u'x-size')),
                                 int(self.props.GetProperty(u'main-window',
                                                            u'y-size')))
        self.frame.Show()
        self.results = PSIui.ResultDialog(self.frame, self.props)
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
        self.results.Close(False)
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
            width = self.ResultGraph.size[0] - 2*self.ResultGraph.margin[0]
            height = self.ResultGraph.size[1] - 2*self.ResultGraph.margin[1]
            data = self.mainGrid.GetSelectedCellsList('N')
            print data
            (minX, maxX, minY, maxY) = Math.RangeN(data)
            X0 = minX
            Y0 = Result['slope']*X0 + Result['intercept']
            X1 = maxX
            Y1 = Result['slope']*X1 + Result['intercept']
            aqua = wx.Color(0, 128, 128)
            self.ResultGraph.DrawLine(
                int(2*self.ResultGraph.margin[0] + (float(X0) - minX)*
                    (width - 2*self.ResultGraph.margin[0])/(maxX - minX)),
                int(height - ((float(Y0) - minY)*
                    (height - 2*self.ResultGraph.margin[1])/(maxY - minY))),
                int(2*self.ResultGraph.margin[0] + (float(X1) - minX)*
                    (width - 2*self.ResultGraph.margin[0])/(maxX - minX)),
                int(height - ((float(Y1) - minY)*
                    (height - 2*self.ResultGraph.margin[1])/(maxY - minY))),
                color = aqua, width = 3)
            lightblue = wx.Color(160, 150, 255)
            self.ResultGraph.PlotXYData(data, color = lightblue, radius = 3)
            self.results.Show()

if __name__ == '__main__':
    app = PSI(False)
    app.MainLoop()
