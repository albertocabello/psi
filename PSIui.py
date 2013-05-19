#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
from wx import grid
from wx import xrc
import Graphics


class DataGrid (wx.grid.Grid):

    def __init__(self):
        # p = grid.PreGrid()
        self.PostCreate(grid.PreGrid())
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
        Cells = []
        try:
            y0 = x0 = self.GetSelectionBlockTopLeft()[0][0]
            y1 = x1 = self.GetSelectionBlockTopLeft()[0][1]
            y0 = self.GetSelectionBlockBottomRight()[0][0]
            y1 = self.GetSelectionBlockBottomRight()[0][1]
            if (orientation == 'Z'):
                for i in range(x0, y0 + 1):
                    for j in range(x1, y1 + 1):
                        Cells.append(self.GetCellValue(i, j))
            elif (orientation == 'N'):
                for j in range(x1, y1 + 1):
                    for i in range(x0, y0 + 1):
                        Cells.append(self.GetCellValue(i, j))
        except IndexError:
            None
        return Cells

    def GetSelectedCellsArray(self, orientation = 'Rows'):
        """
        Returns selected cells as an array of arrays (rows, or columns
        if orientation = 'Cols').
        """
        Cells = []
        try:
            y0 = x0 = self.GetSelectionBlockTopLeft()[0][0]
            y1 = x1 = self.GetSelectionBlockTopLeft()[0][1]
            y0 = self.GetSelectionBlockBottomRight()[0][0]
            y1 = self.GetSelectionBlockBottomRight()[0][1]
            if (orientation == 'Rows'):
                for i in range(x0, y0 + 1):
                    Row = []
                    for j in range(x1, y1 + 1):
                        Row.append(self.GetCellValue(i, j))
                    Cells.append(Row)
            elif (orientation == 'Cols'):
                for j in range(x1, y1 + 1):
                    Col = []
                    for i in range(x0, y0 + 1):
                        Col.append(self.GetCellValue(i, j))
                    Cells.append(Col)
        except IndexError:
            None
        return Cells


class Result (wx.Frame):

    def __init__(self, parent, props):
        self.Res = xrc.XmlResource(u'mainGrid.xrc')
        Pre = wx.PreFrame()
        self.Res.LoadOnFrame(Pre, parent, u'ResultFrame')
        self.PostCreate(Pre)
        self.props = props
        self.SetDimensions(int(props[(u'results', u'x-position')]),
                           int(props[(u'results', u'y-position')]),
                           int(props[(u'results', u'x-size')]),
                           int(props[(u'results', u'y-size')]))
        font = xrc.XRCCTRL(self, u'ResultText').GetFont()
        font.SetEncoding(int(props[(u'results', u'text-encoding')]))
        font.SetFaceName(props[(u'results', u'text-face')])
        font.SetFamily(int(props[(u'results', u'text-family')]))
        font.SetPointSize(int(props[(u'results', u'text-point-size')]))
        font.SetStyle(int(props[(u'results', u'text-style')]))
        font.SetUnderlined(bool(props[(u'results', u'text-underlined')]))
        font.SetWeight(int(props[(u'results', u'text-weight')]))
        xrc.XRCCTRL(self, u'ResultText').SetFont(font)
        font = xrc.XRCCTRL(self, u'ResultGraph').GetFont()
        font.SetEncoding(int(props[(u'results', u'graph-encoding')]))
        font.SetFaceName(props[(u'results', u'graph-face')])
        font.SetFamily(int(props[(u'results', u'graph-family')]))
        font.SetPointSize(int(props[(u'results', u'graph-point-size')]))
        font.SetStyle(int(props[(u'results', u'graph-style')]))
        font.SetUnderlined(bool(props[(u'results', u'graph-underlined')]))
        font.SetWeight(int(props[(u'results', u'graph-weight')]))
        xrc.XRCCTRL(self, u'ResultGraph').SetStyle(Graphics.Style(props))
        xrc.XRCCTRL(self, u'ResultGraph').SetFont(font)
        xrc.XRCCTRL(self, u'ButtonOK').Bind(wx.EVT_LEFT_UP, self.Close)

    def Close(self, event):
        (x, y) = self.GetPosition()
        self.props[(u'results', u'x-position')] = x
        self.props[(u'results', u'y-position')] = y
        (w, h) = self.GetSize()
        self.props[(u'results', u'x-size')] = w
        self.props[(u'results', u'y-size')] = h
        self.props.Save()
        wx.Frame.Close(self, False)


class StyleDialog(wx.Dialog):

    def __init__(self, parent, props):
        self.res = xrc.XmlResource(u'mainGrid.xrc')
        pre = wx.PreDialog()
        self.res.LoadOnDialog(pre, parent, u'StyleDialog')
        self.PostCreate(pre)
        radius = props[('style', 'dots-radius')]
        xrc.XRCCTRL(self, u'DotsRadius').SetValue(int(radius))
        self.dots_r = props[('style', 'dots-color-r')]
        self.dots_g = props[('style', 'dots-color-g')]
        self.dots_b = props[('style', 'dots-color-b')]
        color = wx.Color(int(self.dots_r), int(self.dots_g), int(self.dots_b))
        DotsColorCtrl = xrc.XRCCTRL(self, u'DotsColor')
        DotsColorCtrl.SetColour(color)
        width = props[('style', 'line-width')]
        xrc.XRCCTRL(self, u'LineWidth').SetValue(int(width))
        LineColorCtrl = xrc.XRCCTRL(self, u'LineColor')
        self.line_r = props[('style', 'line-color-r')]
        self.line_g = props[('style', 'line-color-g')]
        self.line_b = props[('style', 'line-color-b')]
        color = wx.Color(int(self.line_r), int(self.line_g), int(self.line_b))
        LineColorCtrl.SetColour(color)
        self.ResultTextLabel = xrc.XRCCTRL(self, u'LabelResultsFontStyle')
        font = self.ResultTextLabel.GetFont()
        font.SetEncoding(int(props[(u'results', u'text-encoding')]))
        font.SetFaceName(props[(u'results', u'text-face')])
        font.SetFamily(int(props[(u'results', u'text-family')]))
        font.SetPointSize(int(props[(u'results', u'text-point-size')]))
        font.SetStyle(int(props[(u'results', u'text-style')]))
        font.SetUnderlined(bool(props[(u'results', u'text-underlined')]))
        font.SetWeight(int(props[(u'results', u'text-weight')]))
        self.ResultTextLabel.SetFont(font)
        self.GraphTextLabel = xrc.XRCCTRL(self, u'LabelGraphFontStyle')
        font = self.GraphTextLabel.GetFont()
        font.SetEncoding(int(props[(u'results', u'graph-encoding')]))
        font.SetFaceName(props[(u'results', u'graph-face')])
        font.SetFamily(int(props[(u'results', u'graph-family')]))
        font.SetPointSize(int(props[(u'results', u'graph-point-size')]))
        font.SetStyle(int(props[(u'results', u'graph-style')]))
        font.SetUnderlined(bool(props[(u'results', u'graph-underlined')]))
        font.SetWeight(int(props[(u'results', u'graph-weight')]))
        self.GraphTextLabel.SetFont(font)
        xrc.XRCCTRL(self, u'ButtonResultsFontStyle').Bind(wx.EVT_LEFT_UP,
            lambda x: self.SelectNewFont(x, label = u'LabelResultsFontStyle'))
        xrc.XRCCTRL(self, u'ButtonGraphFontStyle').Bind(wx.EVT_LEFT_UP,
            lambda x: self.SelectNewFont(x, label = u'LabelGraphFontStyle'))
        if self.ShowModal() == wx.ID_OK:
            self.dots_r = DotsColorCtrl.GetColour().Red()
            self.dots_g = DotsColorCtrl.GetColour().Green()
            self.dots_b = DotsColorCtrl.GetColour().Blue()
            props[('style', 'dots-color-r')] = self.dots_r
            props[('style', 'dots-color-g')] = self.dots_g
            props[('style', 'dots-color-b')] = self.dots_b
            radius = xrc.XRCCTRL(self, u'DotsRadius').GetValue()
            self.line_r = LineColorCtrl.GetColour().Red()
            self.line_g = LineColorCtrl.GetColour().Green()
            self.line_b = LineColorCtrl.GetColour().Blue()
            props[('style', 'dots-radius')] = radius
            props[('style', 'line-color-r')] = self.line_r
            props[('style', 'line-color-g')] = self.line_g
            props[('style', 'line-color-b')] = self.line_b
            width = xrc.XRCCTRL(self, u'LineWidth').GetValue()
            props[('style', 'line-width')] = width
            font = xrc.XRCCTRL(self, u'LabelResultsFontStyle').GetFont()
            props[(u'results', u'text-encoding')] = font.GetEncoding()
            props[(u'results', u'text-face')] = font.GetFaceName()
            props[(u'results', u'text-family')] = font.GetFamily()
            props[(u'results', u'text-point-size')] = font.GetPointSize()
            props[(u'results', u'text-style')] = font.GetStyle()
            props[(u'results', u'text-underlined')] = font.GetUnderlined()
            props[(u'results', u'text-weight')] = font.GetWeight()
            font = xrc.XRCCTRL(self, u'LabelGraphFontStyle').GetFont()
            props[(u'results', u'graph-encoding')] = font.GetEncoding()
            props[(u'results', u'graph-face')] = font.GetFaceName()
            props[(u'results', u'graph-family')] = font.GetFamily()
            props[(u'results', u'graph-point-size')] = font.GetPointSize()
            props[(u'results', u'graph-style')] = font.GetStyle()
            props[(u'results', u'graph-underlined')] = font.GetUnderlined()
            props[(u'results', u'graph-weight')] = font.GetWeight()
            props.Save()

    def SelectNewFont(self, e, label):
            Data = wx.FontData()
            Data.SetInitialFont(xrc.XRCCTRL(self, label).GetFont())
            Dialog = wx.FontDialog(self, Data)
            if Dialog.ShowModal() == wx.ID_OK:
                newFont = Dialog.GetFontData().GetChosenFont()
                xrc.XRCCTRL(self, label).SetFont(newFont)
            Dialog.Destroy()
