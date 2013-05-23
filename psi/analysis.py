#! /usr/bin/env python
#coding=utf-8

import scipy.stats
import numpy
import math


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
        canvas.DrawGrid()        
        data = numpy.sort(numpy.array(self.data, dtype=float))
        canvas.SetDrawingArea(0, len(data), min(data), max(data))
        width = canvas.size[0] - 2*canvas.margin[0]
        height = canvas.size[1] - 2*canvas.margin[1]
        canvas.SetStyle(style)
        for i in range(0, len(data)):
            canvas.PlotXY((i, data[i]))


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
        canvas.DrawGrid()
        width = canvas.size[0] - 2*canvas.margin[0]
        height = canvas.size[1] - 2*canvas.margin[1]
        (min_x, max_x, min_y, max_y) = math.RangeN(self.data)
        canvas.SetDrawingArea(min_x, max_x, min_y, max_y)
        canvas.SetStyle(style)
        x_0 = min_x
        y_0 = self.res['slope']*x_0 + self.res['intercept']
        x_1 = max_x
        y_1 = self.res['slope']*x_1 + self.res['intercept']
        canvas.DrawLine(
            int(2*canvas.margin[0] + (float(x_0) - min_x)*
                (width - 2*canvas.margin[0])/(max_x - min_x)),
            int(height - ((float(y_0) - min_y)*
                (height - 2*canvas.margin[1])/(max_y - min_y))),
            int(2*canvas.margin[0] + (float(x_1) - min_x)*
                (width - 2*canvas.margin[0])/(max_x - min_x)),
            int(height - ((float(y_1) - min_y)*
                (height - 2*canvas.margin[1])/(max_y - min_y))),
            color = style['line-color'], width = style['line-width'])
        canvas.PlotXYData(self.data)

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
