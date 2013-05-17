#! /usr/bin/env python
#coding=utf-8

import wx
from wx import xrc


class ResultGraph(wx.ScrolledWindow):

    def __init__(self):
        pre = wx.PreScrolledWindow()
        res = xrc.XmlResource(u'mainGrid.xrc')
        self.pos = (0, 0)
        self.margin = (10, 10)
        self.size = (450, 450)
        self.PostCreate(pre)
        self.Bind(wx.EVT_PAINT, self.PostInit)

    def PostInit(self, event):
        self.pos = (0, 0)
        self.size = (450, 450)
        self.SetScrollbars(5, 5, 90, 90)
        self.OnPaint(event)
        self.Unbind(wx.EVT_PAINT)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def Init(self):
        try:
            dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)
        except AttributeError:
            self.buffer = wx.EmptyBitmap(self.size[0], self.size[1])
            dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)
            dc.Clear()
            dc.SetBrush(wx.Brush('white'))
            dc.SetPen(wx.Pen('black', 2))
        return dc

    def OnPaint(self, event):
        dc = self.Init()
        self.Show()

    def DrawCircle(self, x, y):
        dc = self.Init()
        color = self.style['dots-color']
        radius = self.style['dots-radius']
        dc.SetPen(wx.Pen(color, 1))
        dc.SetBrush(wx.Brush(color))
        dc.DrawCircle(x, y, radius)

    def DrawGrid(self, color = 'black', width = 2, ticks = '10'):
        dc = self.Init()
        dc.Clear()
        dc.SetPen(wx.Pen(color, width))
        width = self.size[0] - 2*self.margin[0]
        height = self.size[1] - 2*self.margin[1]
        dc.DrawRectangle(self.margin[0], self.margin[1], width, height)
        if ticks > 0:
            for i in range(30, self.size[1] - self.margin[1], 50):
                dc.DrawLine(20, i, 24, i)
            for i in range(20, self.size[0] - self.margin[0], 50):
                dc.DrawLine(i, self.size[1] - self.margin[1],
                            i, self.size[1] - self.margin[1] + 5)

    def DrawLine(self, x0, y0, x1, y1, color = 'black', width = 1):
        dc = self.Init()
        dc.SetPen(wx.Pen(color, width))
        dc.DrawLine(x0, y0, x1, y1)

    def DrawPoint(self, x, y):
        dc = self.Init()
        color = self.style['dots-color']
        radius = self.style['dots-radius']
        dc.SetPen(wx.Pen(color, 1))
        if radius == 0:
            dc.DrawPoint(x, y)
        else:
            self.DrawCircle(x, y)

    def PlotXY(self, point):
        width = self.size[0] - 2*self.margin[0]
        height = self.size[1] - 2*self.margin[1]
        x = int(2*self.margin[0] + (float(point[0]) - self.minX)*
                (width - 2*self.margin[0])/(self.maxX - self.minX))
        y = int(2*self.margin[1] + (float(point[1]) - self.minY)*
                (height - 2*self.margin[1])/(self.maxY - self.minY))
        print x, y
        self.DrawPoint(x, y)

    def PlotXYData(self, data):
        for i in range(0, len(data)/2):
            x = data[i]
            y = data[i + len(data)/2]
            self.PlotXY((x, y))
        self.PlotXY((x, y))

    def SetDrawingArea(self, left, right, top, bottom):
        self.minX = left
        self.maxX = right
        self.minY = bottom
        self.maxY = top

    def SetMargin(self, x_margin, y_margin):
        self.margin[0] = x_margin
        self.margin[1] = y_margin

    def SetStyle(self, style):
        self.style = style


class Style:

    def __init__(self, properties):
        self.style = {}
        r = int(properties.GetProperty('style', 'dots-color-r'))
        g = int(properties.GetProperty('style', 'dots-color-g'))
        b = int(properties.GetProperty('style', 'dots-color-b'))
        self.style['dots-color'] = wx.Color(r, g, b)
        radius = int(properties.GetProperty('style', 'dots-radius'))
        self.style['dots-radius'] = radius
        r = int(properties.GetProperty('style', 'line-color-r'))
        g = int(properties.GetProperty('style', 'line-color-g'))
        b = int(properties.GetProperty('style', 'line-color-b'))
        self.style['line-color'] = wx.Color(r, g, b)
        width = int(properties.GetProperty('style', 'line-width'))
        self.style['line-width'] = width

    def __getitem__(self, name):
        return self.style[name]

    def GetStyle(self):
        return self.style
