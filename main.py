#!/usr/bin/python
# -*- coding: utf-8 -*-
import wx
from wx import xrc
from wx import grid
import PSIui
import Analysis


class PSI(wx.App):

    def OnInit(self):
        self.res = xrc.XmlResource('mainGrid.xrc')
        self.frame = self.res.LoadFrame(None, 'mainFrame')
        self.mainGrid = xrc.XRCCTRL(self.frame, 'mainGrid')
        self.mainGrid.CreateGrid(1000, 26)
        self.mainGrid.EnableDragRowSize(False)
        self.mainGrid.EnableDragColSize(False)
        self.frame.Bind(wx.EVT_MENU, self.PrintSelectedCells,
                        id = xrc.XRCID('Print'))
        self.frame.Bind(wx.EVT_MENU, self.Close,
                        id = xrc.XRCID('Quit'))
        self.frame.Bind(wx.EVT_MENU, self.OpenFile,
                        id = xrc.XRCID('Open'))
        self.frame.Bind(wx.EVT_MENU, self.DoLR,
                        id = xrc.XRCID('LR'))
        self.frame.SetSize((600, 450))
        self.frame.Show()
        self.ResultDialog = self.res.LoadDialog(None, 'ResultDialog')
        self.ResultText = xrc.XRCCTRL(self.ResultDialog, 'ResultText')
        return True

    def PrintSelectedCells(self, e):
        print 'Printing selected cells:'
        for i in self.mainGrid.GetSelectedCellsList('N'):
            print i

    def Close(self, e):
        print 'Closing application...'
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
            summary = "Y = {0:.2}*X + {1:.2}".format(Result['slope'],
                                                     Result['intercept'])
            self.ResultText.AppendText(summary)
            self.ResultDialog.Show()

if __name__ == '__main__':
    app = PSI(False)
    app.MainLoop()
