#! /usr/bin/env python
#coding=utf-8

import wx
from wx import xrc
import Math


class ResultGraph(wx.ScrolledWindow):

    def __init__(self):
        pre = wx.PreScrolledWindow()
        res = xrc.XmlResource(u'mainGrid.xrc')
        self.pos = (0, 0)
        self.margin = (0, 0)
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

    def DrawCircle(self, x, y, r, color = 'black', width = 1, fill = 'white'):
        dc = self.Init()
        dc.SetPen(wx.Pen(color, width))
        dc.SetBrush(wx.Brush(fill))
        dc.DrawCircle(x, y, r)

    def DrawGrid(self, margin = (20, 20),
                 color = 'black', width = 2, ticks = '10'):
        dc = self.Init()
        dc.Clear()
        self.margin = margin
        dc.SetPen(wx.Pen(color, width))
        width = self.size[0] - 2*margin[0]
        height = self.size[1] - 2*margin[1]
        dc.DrawRectangle(margin[0], margin[1], width, height)
        if ticks > 0:
            for i in range(30, self.size[1] - margin[1], 50):
                dc.DrawLine(20, i, 24, i)
            for i in range(20, self.size[0] - margin[0], 50):
                dc.DrawLine(i, self.size[1] - margin[1],
                            i, self.size[1] - margin[1] + 5)

    def DrawLine(self, x0, y0, x1, y1, color = 'black', width = 1):
        dc = self.Init()
        dc.SetPen(wx.Pen(color, width))
        dc.DrawLine(x0, y0, x1, y1)

    def DrawPoint(self, x, y, color = 'black', radius = 0):
        dc = self.Init()
        dc.SetPen(wx.Pen(color, 1))
        if radius == 0:
            dc.DrawPoint(x, y)
        else:
            self.DrawCircle(x, y, radius, color = color, fill = color)

    def PlotXYData(self, data, color = 'black', radius = 1):
        width = self.size[0] - 2*self.margin[0]
        height = self.size[1] - 2*self.margin[1]
        (minX, maxX, minY, maxY) = Math.RangeN(data)
        for i in range(0, len(data)/2):
            x = int(2*self.margin[0] + (float(data[i]) - minX)*
                    (width - 2*self.margin[0])/(maxX - minX))
            y = int(height - ((float(data[i + len(data)/2]) - minY)*
                    (height - 2*self.margin[1])/(maxY - minY)))
            self.DrawPoint(x, y, color, radius)
        self.DrawPoint(x, y, color, radius)
