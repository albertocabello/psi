#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
from wx import grid


class DataGrid (wx.grid.Grid):

    def __init__(self):
        print 'Init DataGrid...'
        p = grid.PreGrid()
        self.PostCreate(p)
        self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)

    def OnCreate(self, evt):
        self.Unbind(wx.EVT_WINDOW_CREATE)
        self.SetDefaultCellAlignment(wx.ALIGN_RIGHT, wx.ALIGN_BOTTOM)

    def LoadCSV(self, filename, separator = ','):
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
