#!/usr/bin/python
# -*- coding: utf-8 -*-
import wx
from wx import xrc
from wx import grid
import PSIui
import Analysis
import Properties


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
        self.ResultDialog = self.res.LoadDialog(None, u'ResultDialog')
        self.ResultDialog.SetSize((300, 250))
        self.ResultText = xrc.XRCCTRL(self.ResultDialog, u'ResultText')
        font = wx.Font(8, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Monospace')
        self.ResultText.SetFont(font)
        return True

    def PrintSelectedCells(self, e):
        print 'Printing selected cells:'
        for i in self.mainGrid.GetSelectedCellsList('N'):
            print i

    def Close(self, e):
        print 'Closing application...'
        self.ResultDialog.Close()
        self.frame.Close()

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
            self.ResultDialog.Show()

if __name__ == '__main__':
    app = PSI(False)
    app.MainLoop()
