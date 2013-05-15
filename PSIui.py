#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
from wx import grid
from wx import xrc
import Graphics


class DataGrid (wx.grid.Grid):

    def __init__(self):
        p = grid.PreGrid()
        self.PostCreate(p)
        self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)

    def OnCreate(self, evt):
        self.Unbind(wx.EVT_WINDOW_CREATE)
        self.SetDefaultCellAlignment(wx.ALIGN_RIGHT, wx.ALIGN_BOTTOM)

    def LoadCSV(self, filename, separator = ','):
        """
        Load values stored in file 'filename' separated by commas (or
        optional parameter 'separator').
        """
        with open(filename) as f:
            i = 0
            print 'Loading file %s' % filename
            while 1:
                l = f.readline()
                if not l:
                    break
                l = l.rstrip('\n')
                j = 0
                for x in l.rsplit(separator):
                    self.SetCellValue(i, j, x)
                    j = j + 1
                i = i + 1

    def GetSelectedCellsList(self, orientation = 'Z'):
        """
        Returns selected cells as an array of values ordered by rows
        (or by columns if orientation = 'N').
        """
        cells = []
        try:
            y0 = x0 = self.GetSelectionBlockTopLeft()[0][0]
            y1 = x1 = self.GetSelectionBlockTopLeft()[0][1]
            y0 = self.GetSelectionBlockBottomRight()[0][0]
            y1 = self.GetSelectionBlockBottomRight()[0][1]
            if (orientation == 'Z'):
                for i in range(x0, y0 + 1):
                    for j in range(x1, y1 + 1):
                        cells.append(self.GetCellValue(i, j))
            elif (orientation == 'N'):
                for j in range(x1, y1 + 1):
                    for i in range(x0, y0 + 1):
                        cells.append(self.GetCellValue(i, j))
        except IndexError:
            None
        return cells

    def GetSelectedCellsArray(self, orientation = 'Rows'):
        """
        Returns selected cells as an array of arrays (rows, or columns
        if orientation = 'Cols').
        """
        cells = []
        try:
            y0 = x0 = self.GetSelectionBlockTopLeft()[0][0]
            y1 = x1 = self.GetSelectionBlockTopLeft()[0][1]
            y0 = self.GetSelectionBlockBottomRight()[0][0]
            y1 = self.GetSelectionBlockBottomRight()[0][1]
            if (orientation == 'Rows'):
                for i in range(x0, y0 + 1):
                    row = []
                    for j in range(x1, y1 + 1):
                        row.append(self.GetCellValue(i, j))
                    cells.append(row)
            elif (orientation == 'Cols'):
                for j in range(x1, y1 + 1):
                    col = []
                    for i in range(x0, y0 + 1):
                        col.append(self.GetCellValue(i, j))
                    cells.append(col)
        except IndexError:
            None
        return cells


class Result (wx.Frame):

    def __init__(self, parent, properties):
        self.res = xrc.XmlResource(u'mainGrid.xrc')
        # pre = wx.PreDialog()
        # self.res.LoadOnDialog(pre, parent, u'ResultDialog')
        # self.PostCreate(pre)
        pre = wx.PreFrame()
        self.res.LoadOnFrame(pre, parent, u'ResultFrame')
        self.PostCreate(pre)
        self.properties = properties
        self.SetDimensions(int(properties.GetProperty(u'results',
                                                      u'x-position')),
                           int(properties.GetProperty(u'results',
                                                      u'y-position')),
                           int(properties.GetProperty(u'results',
                                                      u'x-size')),
                           int(properties.GetProperty(u'results',
                                                      u'y-size')))
        font = wx.Font(8, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Monospace')
        xrc.XRCCTRL(self, u'ResultText').SetFont(font)
        xrc.XRCCTRL(self, u'ButtonOK').Bind(wx.EVT_LEFT_UP, self.Close)

    def Close(self, event):
        (x, y) = self.GetPosition()
        self.properties.SetProperty(u'results', u'x-position', x)
        self.properties.SetProperty(u'results', u'y-position', y)
        (w, h) = self.GetSize()
        self.properties.SetProperty(u'results', u'x-size', w)
        self.properties.SetProperty(u'results', u'y-size', h)
        self.properties.Save()
        wx.Frame.Close(self, False)


class StyleDialog(wx.Dialog):

    def __init__(self, parent, props):
        self.res = xrc.XmlResource(u'mainGrid.xrc')
        pre = wx.PreDialog()
        self.res.LoadOnDialog(pre, parent, u'StyleDialog')
        self.PostCreate(pre)
        radius = props.GetProperty('style', 'dots-radius')
        xrc.XRCCTRL(self, u'DotsRadius').SetValue(int(radius))
        self.dots_r = props.GetProperty('style', 'dots-color-r')
        self.dots_g = props.GetProperty('style', 'dots-color-g')
        self.dots_b = props.GetProperty('style', 'dots-color-b')
        color = wx.Color(int(self.dots_r), int(self.dots_g), int(self.dots_b))
        DotsColorCtrl = xrc.XRCCTRL(self, u'DotsColor')
        DotsColorCtrl.SetColour(color)
        width = props.GetProperty('style', 'line-width')
        xrc.XRCCTRL(self, u'LineWidth').SetValue(int(width))
        LineColorCtrl = xrc.XRCCTRL(self, u'LineColor')
        self.line_r = props.GetProperty('style', 'line-color-r')
        self.line_g = props.GetProperty('style', 'line-color-g')
        self.line_b = props.GetProperty('style', 'line-color-b')
        color = wx.Color(int(self.line_r), int(self.line_g), int(self.line_b))
        LineColorCtrl.SetColour(color)
        if self.ShowModal() == wx.ID_OK:
            self.dots_r = DotsColorCtrl.GetColour().Red()
            self.dots_g = DotsColorCtrl.GetColour().Green()
            self.dots_b = DotsColorCtrl.GetColour().Blue()
            props.SetProperty('style', 'dots-color-r', self.dots_r)
            props.SetProperty('style', 'dots-color-g', self.dots_g)
            props.SetProperty('style', 'dots-color-b', self.dots_b)
            radius = xrc.XRCCTRL(self, u'DotsRadius').GetValue()
            self.line_r = LineColorCtrl.GetColour().Red()
            self.line_g = LineColorCtrl.GetColour().Green()
            self.line_b = LineColorCtrl.GetColour().Blue()
            props.SetProperty('style', 'dots-radius', radius)
            props.SetProperty('style', 'line-color-r', self.line_r)
            props.SetProperty('style', 'line-color-g', self.line_g)
            props.SetProperty('style', 'line-color-b', self.line_b)
            width = xrc.XRCCTRL(self, u'LineWidth').GetValue()
            props.SetProperty('style', 'line-width', width)
