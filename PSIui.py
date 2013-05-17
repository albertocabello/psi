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
        self.SetDimensions(int(props.GetProperty(u'results',
                                                 u'x-position')),
                           int(props.GetProperty(u'results',
                                                 u'y-position')),
                           int(props.GetProperty(u'results',
                                                 u'x-size')),
                           int(props.GetProperty(u'results',
                                                 u'y-size')))
        font = xrc.XRCCTRL(self, u'ResultText').GetFont()
        font.SetEncoding(int(props.GetProperty(u'results', u'encoding')))
        font.SetFaceName(props.GetProperty(u'results', u'face'))
        font.SetFamily(int(props.GetProperty(u'results', u'family')))
        font.SetPointSize(int(props.GetProperty(u'results', u'point-size')))
        font.SetStyle(int(props.GetProperty(u'results', u'style')))
        font.SetUnderlined(bool(props.GetProperty(u'results', u'underlined')))
        font.SetWeight(int(props.GetProperty(u'results', u'weight')))
        xrc.XRCCTRL(self, u'ResultText').SetFont(font)
        xrc.XRCCTRL(self, u'ButtonOK').Bind(wx.EVT_LEFT_UP, self.Close)

    def Close(self, event):
        (x, y) = self.GetPosition()
        self.props.SetProperty(u'results', u'x-position', x)
        self.props.SetProperty(u'results', u'y-position', y)
        (w, h) = self.GetSize()
        self.props.SetProperty(u'results', u'x-size', w)
        self.props.SetProperty(u'results', u'y-size', h)
        self.props.Save()
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
        font = xrc.XRCCTRL(self, u'LabelFontStyle').GetFont()
        font.SetEncoding(int(props.GetProperty(u'results', u'encoding')))
        font.SetFaceName(props.GetProperty(u'results', u'face'))
        font.SetFamily(int(props.GetProperty(u'results', u'family')))
        font.SetPointSize(int(props.GetProperty(u'results', u'point-size')))
        font.SetStyle(int(props.GetProperty(u'results', u'style')))
        font.SetUnderlined(bool(props.GetProperty(u'results', u'underlined')))
        font.SetWeight(int(props.GetProperty(u'results', u'weight')))
        xrc.XRCCTRL(self, u'LabelFontStyle').SetFont(font)
        self.newFont = font
        xrc.XRCCTRL(self, u'ButtonFontStyle').Bind(wx.EVT_LEFT_UP, self.SelectNewFont)
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
            props.SetProperty(u'results', u'encoding', self.newFont.GetEncoding())
            props.SetProperty(u'results', u'face', self.newFont.GetFaceName())
            props.SetProperty(u'results', u'family', self.newFont.GetFamily())
            props.SetProperty(u'results', u'point-size', self.newFont.GetPointSize())
            props.SetProperty(u'results', u'style', self.newFont.GetStyle())
            props.SetProperty(u'results', u'underlined', self.newFont.GetUnderlined())
            props.SetProperty(u'results', u'weight', self.newFont.GetWeight())
            props.Save()

    def SelectNewFont(self, e):
            Data = wx.FontData()
            Data.SetInitialFont(xrc.XRCCTRL(self, u'LabelFontStyle').GetFont())
            Dialog = wx.FontDialog(self, Data)
            if Dialog.ShowModal() == wx.ID_OK:
                self.newFont = Dialog.GetFontData().GetChosenFont()
                xrc.XRCCTRL(self, u'LabelFontStyle').SetFont(self.newFont)
            Dialog.Destroy()
