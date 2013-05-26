#! /usr/bin/env python
#coding=utf-8

import wx

"""
class Graph:

    def __init__(self):
        self.objects = []

    def Clean(self):
        self.objects = []

    def Circle(self, cx=0, cy=0, r=1):
        self.objects.append({'shape': 'circle', ))

    def Line(self):
    def Line(self):
    def Line(self):
    def Point(self):
    def Rectangle(self):
    def Text(self):"""


class ResultGraph(wx.ScrolledWindow):

    def __init__(self):
        pre = wx.PreScrolledWindow()
        res = wx.xrc.XmlResource(u'main_grid.xrc')
        self.pos = (0, 0)
        self.margin = (10, 10)
        self.size = (450, 450)
        self.PostCreate(pre)
        self.Bind(wx.EVT_PAINT, self.__post_init)

    def __on_paint(self, event):
        dc = self.Init()
        self.Show()

    def __post_init(self, event):
        self.pos = (0, 0)
        self.size = (450, 450)
        self.SetScrollbars(5, 5, 90, 90)
        self.__on_paint(event)
        self.Unbind(wx.EVT_PAINT)
        self.Bind(wx.EVT_PAINT, self.__on_paint)

    def Init(self):
        """
        Returns a PaintDC, creating a Bitmap for it when needed.
        Make drawing operations on the return value of Init().
        """
        try:
            dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)
        except AttributeError:
            self.buffer = wx.EmptyBitmap(self.size[0], self.size[1])
            dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)
            dc.Clear()
            dc.SetBrush(wx.Brush('white'))
            dc.SetPen(wx.Pen('black', 2))
        return dc

    def DrawCircle(self, x, y, color=None, radius=None):
        dc = self.Init()
        if color is None:
            color = self.style['dots-color']
        if radius is None:
            radius = self.style['dots-radius']
        dc.SetPen(wx.Pen(color, 1))
        dc.SetBrush(wx.Brush(color))
        dc.DrawCircle(x, y, radius)
        print x, y

    def DrawGrid(self, color='black', width=1, x_ticks=10, y_ticks=10):
        dc = self.Init()
        dc.Clear()
        dc.SetPen(wx.Pen(color, width))
        width = self.size[0] - 2*self.margin[0]
        height = self.size[1] - 2*self.margin[1]
        dc.DrawRectangle(self.margin[0], self.margin[1], width, height)
        if x_ticks > 0:
            for i in range(20, self.size[0] - self.margin[0], 50):
                dc.DrawLine(i, self.size[1] - self.margin[1],
                            i, self.size[1] - self.margin[1] + 5)
        if y_ticks > 0:
            for i in range(30, self.size[1] - self.margin[1], 50):
                dc.DrawLine(self.margin[0] - 5, i, self.margin[0], i)

    def DrawLine(self, x0, y0, x1, y1, color='black', width=1):
        dc = self.Init()
        dc.SetPen(wx.Pen(color, width))
        dc.DrawLine(x0, y0, x1, y1)

    def DrawPoint(self, x, y, color=None, radius=None, label=None):
        dc = self.Init()
        if color is None:
            color = self.style['dots-color']
        if radius is None:
            radius = self.style['dots-radius']
        dc.SetPen(wx.Pen(color, 1))
        if label is not None:
            dc.SetFont(self.GetFont())
            dc.DrawText(u'{0}, {1}'.format(x, y), x, y)
        if radius == 0:
            dc.DrawPoint(x, y)
        else:
            self.DrawCircle(x, y, color=color, radius=radius)

    def PlotXY(self, point, color=None, radius=None, label=None):
        width = self.size[0] - 2*self.margin[0]
        height = self.size[1] - 2*self.margin[1]
        x = int(2*self.margin[0] + (float(point[0]) - self.minX)*
                (width - 2*self.margin[0])/(self.maxX - self.minX))
        y = int(2*self.margin[1] + (float(point[1]) - self.minY)*
                (height - 2*self.margin[1])/(self.maxY - self.minY))
        self.DrawPoint(x, y, color=color, radius=radius, label=label)

    def PlotXYData(self, data, color=None, radius=None, label=None):
        for i in range(0, len(data)/2):
            x = data[i]
            y = data[i + len(data)/2]
            self.PlotXY((x, y), color=color, radius=radius, label=label)
        self.PlotXY((x, y), color=color, radius=radius, label=label)

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
        r = int(properties[('style', 'dots-color-r')])
        g = int(properties[('style', 'dots-color-g')])
        b = int(properties[('style', 'dots-color-b')])
        self.style['dots-color'] = wx.Color(r, g, b)
        radius = int(properties[('style', 'dots-radius')])
        self.style['dots-radius'] = radius
        r = int(properties[('style', 'line-color-r')])
        g = int(properties[('style', 'line-color-g')])
        b = int(properties[('style', 'line-color-b')])
        self.style['line-color'] = wx.Color(r, g, b)
        width = int(properties[('style', 'line-width')])
        self.style['line-width'] = width

    def __getitem__(self, name):
        return self.style[name]

    def GetStyle(self):
        return self.style
