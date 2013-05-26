#! /usr/bin/env python
#coding=utf-8

import numpy
import math
import matplotlib
import scipy.stats
import wx


class BasicStatistics:

    def LoadData(self, data):
        self.data = data
        for value in self.data:
            try:
                value = float(value)
            except ValueError:
                print u'Error: bad value {0}'.format(value)
                return False
        return True

    def Calculate(self):
        self.data = numpy.array(self.data, dtype = float)
        self.res = {}
        self.res['min'] = numpy.nanmin(self.data)
        self.res['max'] = numpy.nanmax(self.data)
        self.res['mean'] = numpy.mean(self.data)
        self.res['median'] = numpy.median(self.data)
        self.res['std'] = numpy.std(self.data)
        self.res['var'] = numpy.var(self.data)
        return True

    def PrintResult(self, text):
        text.AppendText(u'Data range: {0} - '.format(self.res['min']))
        text.AppendText(u"{0}\n".format(self.res['max']))
        text.AppendText(u"Mean: {0}\n".format(self.res['mean']))
        text.AppendText(u"Median: {0}\n".format(self.res['median']))
        text.AppendText(u"Standard deviation: {0}\n".format(self.res['std']))
        text.AppendText(u"Variance: {0}\n".format(self.res['var']))

    def DoDrawing(self, canvas, style):
        data = numpy.sort(numpy.array(self.data, dtype=float))
        indexes = range(1, len(self.data) + 1)
        canvas.Clear()
        canvas.axes = canvas.fig.add_subplot(111,
          xlim=(1, len(self.data)), ylim=(self.res['min'], self.res['max']))
        line = matplotlib.lines.Line2D(indexes, data,
          lw=int(style['line-width']), ls='-',
          color=style['line-color'].GetAsString(wx.C2S_HTML_SYNTAX),
          marker='o', ms=2*int(style['dots-radius']),
          mfc=style['dots-color'].GetAsString(wx.C2S_HTML_SYNTAX),
          mew=0)
        canvas.axes.add_line(line)
        canvas.Draw()


class HeatMap:

    def LoadData(self, data):
        self.data = data
        self.size = len(self.data)
        self.x_range = {}
        self.y_range = {}
        self.z_range = {}
        if self.size % 3 != 0:
            print "Error: bad sample size"
            return False
        for value in self.data:
            try:
                value = float(value)
            except ValueError:
                print "Error: bad value {0} ".format(value)
                # return False
        return True

    def Calculate(self):
        n = self.size/3
        self.x_range[0] = min(numpy.array(self.data[:n], dtype = float))
        self.x_range[1] = max(numpy.array(self.data[:n], dtype = float))
        self.y_range[0] = min(numpy.array(self.data[n:n*2], dtype = float))
        self.y_range[1] = max(numpy.array(self.data[n:n*2], dtype = float))
        self.z_range[0] = min(numpy.array(self.data[n*2:], dtype = float))
        self.z_range[1] = max(numpy.array(self.data[n*2:], dtype = float))
        return True

    def DoDrawing(self, canvas, style):
        canvas.Clear()
        (min_x, max_x) = (self.x_range[0], self.x_range[1])
        (min_y, max_y) = (self.y_range[0], self.y_range[1])
        (min_z, max_z) = (self.z_range[0], self.z_range[1])
        canvas.axes = canvas.fig.add_subplot(111,
          xlim=(min_x, max_x), ylim=(min_y, max_y))
        for i in range(0, len(self.data)/3):
            x = float(self.data[i])
            y = float(self.data[i + len(self.data)/3])
            z = float(self.data[i + 2*len(self.data)/3])
            z_color = math.RYGBMap((z - min_z)/(max_z - min_z))
            color = (z_color[0]/255, z_color[1]/255, z_color[2]/255)
            # TODO: make this a real heat map (via scatter plot).
            line = matplotlib.lines.Line2D((x, x), (y, y), ls='None',
              color=color, marker='o', ms=2*int(style['dots-radius']),
              mfc=color, mew=0)
            canvas.axes.add_line(line)
        canvas.Draw()

    def PrintResult(self, text):
        pass


class LinearRegression:

    def LoadData(self, data):
        self.data = data
        self.size = len(self.data)
        if self.size % 2 == 1:
            print "Error: bad sample size"
            return False
        for value in self.data:
            try:
                value = float(value)
            except ValueError:
                print "Error: bad value {0} ".format(value)
                return False
        return True

    def Calculate(self):
        n = self.size/2
        self.res = {}
        self.res['slope'], self.res['intercept'],\
        self.res['r_value'], self.res['p_value'], self.res['std_err'] =\
        scipy.stats.linregress(numpy.array(self.data[:n], dtype = float),
                               numpy.array(self.data[n:], dtype = float))
        return True

    def DoDrawing(self, canvas, style):
        canvas.Clear()
        (min_x, max_x, min_y, max_y) = math.RangeN(self.data)
        x_0 = min_x
        y_0 = self.res['slope']*x_0 + self.res['intercept']
        x_1 = max_x
        y_1 = self.res['slope']*x_1 + self.res['intercept']
        canvas.Clear()
        canvas.axes = canvas.fig.add_subplot(111,
          xlim=(min_x, max_x), ylim=(min_y, max_y))
        line = matplotlib.lines.Line2D((x_0, x_1), (y_0, y_1),
          lw=int(style['line-width']), ls='-',
          color=style['line-color'].GetAsString(wx.C2S_HTML_SYNTAX))
        canvas.axes.add_line(line)
        n = self.size/2
        indexes = numpy.array(self.data[:n], dtype = float)
        data = numpy.array(self.data[n:], dtype = float)
        line = matplotlib.lines.Line2D(indexes, data, ls='None',
          color=style['line-color'].GetAsString(wx.C2S_HTML_SYNTAX),
          marker='o', ms=2*int(style['dots-radius']),
          mfc=style['dots-color'].GetAsString(wx.C2S_HTML_SYNTAX),
          mew=0)
        canvas.axes.add_line(line)
        canvas.Draw()

    def PrintResult(self, text):
        summary = "Y = {0:.2}*X + {1:.2}\n".format(self.res['slope'],
                                                   self.res['intercept'])
        text.AppendText(summary)
        text.AppendText(u"Slope: {0}\n".format(self.res['slope']))
        text.AppendText(u"Intercept: {0}\n".format(self.res['intercept']))
        text.AppendText(u"R-value: {0}\n".format(self.res['r_value']))
        text.AppendText(u"P value: {0}\n".format(self.res['p_value']))
        text.AppendText(u"Standard Error: {0}\n".format(self.res['std_err']))


class SmirnoffTest:

    def __init__(self):
        print "Using Kolmogorov-Smirnov Test..."

    def LoadData(self, data):
        self.data = data
        self.size = len(self.data)
        if self.size % 2 == 1:
            print "Error: bad sample size"
            return False
        for record in self.data:
            for value in record:
                try:
                    float(value)
                except ValueError:
                    # print "Error: bad value {0} at {1}, {2}".
                    # format(Value, idx_1, idx2)
                    print "Error: bad value {0} ".format(value)
                    return False
        return True

    def Calculate(self):
        return 1
