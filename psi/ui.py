#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx.grid
import gml


def ctrl(window, str_id):
    return wx.xrc.XRCCTRL(window, str_id)


class DataGrid (wx.grid.Grid):

    def __init__(self):
        self.PostCreate(wx.grid.PreGrid())
        self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)

    def OnCreate(self, evt):
        self.Unbind(wx.EVT_WINDOW_CREATE)
        self.SetDefaultCellAlignment(wx.ALIGN_RIGHT, wx.ALIGN_BOTTOM)
        sample_data = ((1, 2, 3, 4),
                       (5, 4.3, 7.6, 8.1),
                       (4.3, 1.2, 6.2, 4.1))
        for i in range(0, 3):
            for j in range(0, 4):
                self.SetCellValue(j, i, '{0}'.format(sample_data[i][j]))

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
        # Here is how to manage multiple selection:
        # try:
        #     for i in range(0, len(self.GetSelectionBlockTopLeft())):
        #         x1 = x0 = self.GetSelectionBlockTopLeft()[i][0]
        #         y1 = y0 = self.GetSelectionBlockTopLeft()[i][1]
        #         x1 = self.GetSelectionBlockBottomRight()[i][0]
        #         y1 = self.GetSelectionBlockBottomRight()[i][1]
        #         print u'({0}, {1}) -> ({2}, {3})'.format(x0, y0, x1, y1)
        # except IndexError:
        #     pass

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
            pass
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
        self.Res = wx.xrc.XmlResource(u'main_grid.xrc')
        Pre = wx.PreFrame()
        self.Res.LoadOnFrame(Pre, parent, u'ResultFrame')
        self.PostCreate(Pre)
        self.props = props
        self.SetDimensions(int(props[(u'results', u'x-position')]),
                           int(props[(u'results', u'y-position')]),
                           int(props[(u'results', u'x-size')]),
                           int(props[(u'results', u'y-size')]))
        self.text = ctrl(self, u'ResultText')
        self.graph = ctrl(self, u'ResultGraph')
        font = self.text.GetFont()
        font.SetEncoding(int(props[(u'results', u'text-encoding')]))
        font.SetFaceName(props[(u'results', u'text-face')])
        font.SetFamily(int(props[(u'results', u'text-family')]))
        font.SetPointSize(int(props[(u'results', u'text-point-size')]))
        font.SetStyle(int(props[(u'results', u'text-style')]))
        font.SetUnderlined(bool(props[(u'results', u'text-underlined')]))
        font.SetWeight(int(props[(u'results', u'text-weight')]))
        self.text.SetFont(font)
        font = self.graph.GetFont()
        font.SetEncoding(int(props[(u'results', u'graph-encoding')]))
        font.SetFaceName(props[(u'results', u'graph-face')])
        font.SetFamily(int(props[(u'results', u'graph-family')]))
        font.SetPointSize(int(props[(u'results', u'graph-point-size')]))
        font.SetStyle(int(props[(u'results', u'graph-style')]))
        font.SetUnderlined(bool(props[(u'results', u'graph-underlined')]))
        font.SetWeight(int(props[(u'results', u'graph-weight')]))
        self.graph.SetStyle(gml.Style(props))
        self.graph.SetFont(font)
        ctrl(self, u'ButtonOK').Bind(wx.EVT_LEFT_UP, self.Close)

    def Close(self, event):
        (x, y) = self.GetPosition()
        self.props[(u'results', u'x-position')] = x
        self.props[(u'results', u'y-position')] = y
        (w, h) = self.GetSize()
        self.props[(u'results', u'x-size')] = w
        self.props[(u'results', u'y-size')] = h
        self.props.Save()
        self.Hide()


class StyleDialog(wx.Dialog):

    def __init__(self, parent, props):
        self.res = wx.xrc.XmlResource(u'main_grid.xrc')
        pre = wx.PreDialog()
        self.res.LoadOnDialog(pre, parent, u'StyleDialog')
        self.PostCreate(pre)
        radius = props[('style', 'dots-radius')]
        ctrl(self, u'DotsRadius').SetValue(int(radius))
        self.dots_r = props[('style', 'dots-color-r')]
        self.dots_g = props[('style', 'dots-color-g')]
        self.dots_b = props[('style', 'dots-color-b')]
        color = wx.Color(int(self.dots_r), int(self.dots_g), int(self.dots_b))
        dots_color_ctrl = ctrl(self, u'DotsColor')
        dots_color_ctrl.SetColour(color)
        width = props[('style', 'line-width')]
        ctrl(self, u'LineWidth').SetValue(int(width))
        line_color_ctrl = ctrl(self, u'LineColor')
        self.line_r = props[('style', 'line-color-r')]
        self.line_g = props[('style', 'line-color-g')]
        self.line_b = props[('style', 'line-color-b')]
        color = wx.Color(int(self.line_r), int(self.line_g), int(self.line_b))
        line_color_ctrl.SetColour(color)
        self.result_text_label = ctrl(self, u'LabelResultsFontStyle')
        self.graph_text_label = ctrl(self, u'LabelGraphFontStyle')
        self.result_text_button = ctrl(self, u'ButtonResultsFontStyle')
        self.graph_text_button = ctrl(self, u'ButtonGraphFontStyle')
        font = self.result_text_label.GetFont()
        font.SetEncoding(int(props[(u'results', u'text-encoding')]))
        font.SetFaceName(props[(u'results', u'text-face')])
        font.SetFamily(int(props[(u'results', u'text-family')]))
        font.SetPointSize(int(props[(u'results', u'text-point-size')]))
        font.SetStyle(int(props[(u'results', u'text-style')]))
        font.SetUnderlined(bool(props[(u'results', u'text-underlined')]))
        font.SetWeight(int(props[(u'results', u'text-weight')]))
        self.result_text_label.SetFont(font)
        font = self.graph_text_label.GetFont()
        font.SetEncoding(int(props[(u'results', u'graph-encoding')]))
        font.SetFaceName(props[(u'results', u'graph-face')])
        font.SetFamily(int(props[(u'results', u'graph-family')]))
        font.SetPointSize(int(props[(u'results', u'graph-point-size')]))
        font.SetStyle(int(props[(u'results', u'graph-style')]))
        font.SetUnderlined(bool(props[(u'results', u'graph-underlined')]))
        font.SetWeight(int(props[(u'results', u'graph-weight')]))
        self.graph_text_label.SetFont(font)
        self.result_text_button.Bind(wx.EVT_LEFT_UP,
            lambda x: self.SelectNewFont(x, label = self.result_text_label))
        self.graph_text_button.Bind(wx.EVT_LEFT_UP,
            lambda x: self.SelectNewFont(x, label = self.graph_text_label))
        if self.ShowModal() == wx.ID_OK:
            self.dots_r = dots_color_ctrl.GetColour().Red()
            self.dots_g = dots_color_ctrl.GetColour().Green()
            self.dots_b = dots_color_ctrl.GetColour().Blue()
            props[('style', 'dots-color-r')] = self.dots_r
            props[('style', 'dots-color-g')] = self.dots_g
            props[('style', 'dots-color-b')] = self.dots_b
            radius = ctrl(self, u'DotsRadius').GetValue()
            self.line_r = line_color_ctrl.GetColour().Red()
            self.line_g = line_color_ctrl.GetColour().Green()
            self.line_b = line_color_ctrl.GetColour().Blue()
            props[('style', 'dots-radius')] = radius
            props[('style', 'line-color-r')] = self.line_r
            props[('style', 'line-color-g')] = self.line_g
            props[('style', 'line-color-b')] = self.line_b
            width = ctrl(self, u'LineWidth').GetValue()
            props[('style', 'line-width')] = width
            font = self.result_text_label.GetFont()
            props[(u'results', u'text-encoding')] = font.GetEncoding()
            props[(u'results', u'text-face')] = font.GetFaceName()
            props[(u'results', u'text-family')] = font.GetFamily()
            props[(u'results', u'text-point-size')] = font.GetPointSize()
            props[(u'results', u'text-style')] = font.GetStyle()
            props[(u'results', u'text-underlined')] = font.GetUnderlined()
            props[(u'results', u'text-weight')] = font.GetWeight()
            font = self.graph_text_label.GetFont()
            props[(u'results', u'graph-encoding')] = font.GetEncoding()
            props[(u'results', u'graph-face')] = font.GetFaceName()
            props[(u'results', u'graph-family')] = font.GetFamily()
            props[(u'results', u'graph-point-size')] = font.GetPointSize()
            props[(u'results', u'graph-style')] = font.GetStyle()
            props[(u'results', u'graph-underlined')] = font.GetUnderlined()
            props[(u'results', u'graph-weight')] = font.GetWeight()
            props.Save()

    def SelectNewFont(self, e, label):
            data = wx.FontData()
            data.SetInitialFont(label.GetFont())
            dialog = wx.FontDialog(self, data)
            if dialog.ShowModal() == wx.ID_OK:
                newFont = dialog.GetFontData().GetChosenFont()
                label.SetFont(newFont)
            dialog.Destroy()
