#! /usr/bin/env python
#coding=utf-8

import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure

import wx


class ResultGraph (wx.ScrolledWindow):

    def __init__(self, parent=None):
        pre = wx.PreScrolledWindow()
        self.PostCreate(pre)
        self.fig = Figure((5, 5))
        self.Bind(wx.EVT_WINDOW_CREATE, self.__post_init)

    def __post_init(self, event):
        self.SetScrollbars(5, 5, 90, 90)
        self.canvas = FigureCanvas(self, id=wx.ID_ANY, figure=self.fig)
        self.Unbind(wx.EVT_WINDOW_CREATE)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def Clear(self):
        self.fig.clf()

    def Draw(self):
        try:
            self.canvas.draw()
        except AttributeError: # if canvas still doesn't exist
            pass

    def OnPaint(self, event):
        self.canvas.draw()

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

    def __setitem__(self, name, value):
        self.style[name] = value

    def GetStyle(self):
        return self.style
