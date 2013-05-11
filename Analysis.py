#! /usr/bin/env python
#coding=utf-8

import scipy.stats
import numpy
import Math


class BasicStatistics:

    def __init__(self):
        print u'Calculating basic parameters...'

    def LoadData(self, data):
        self.Data = data
        for Value in self.Data:
            try:
                Value = float(Value)
            except ValueError:
                print u'Error: bad value {0}'.format(Value)
                return False
        return True

    def Calculate(self):
        self.Data = numpy.array(self.Data, dtype = float)
        self.Res = {}
        self.Res['min'] = numpy.nanmin(self.Data)
        self.Res['max'] = numpy.nanmax(self.Data)
        self.Res['mean'] = numpy.mean(self.Data)
        self.Res['median'] = numpy.median(self.Data)
        self.Res['std'] = numpy.std(self.Data)
        self.Res['var'] = numpy.var(self.Data)
        return True

    def PrintResult(self, text):
        text.AppendText(u'Data range: {0} --'.format(self.Res['min']))
        text.AppendText(u"{0}\n".format(self.Res['max']))
        text.AppendText(u"Mean: {0}\n".format(self.Res['mean']))
        text.AppendText(u"Median: {0}\n".format(self.Res['median']))
        text.AppendText(u"Standard deviation: {0}\n".format(self.Res['std']))
        text.AppendText(u"Variance: {0}\n".format(self.Res['var']))


class LinearRegression:

    def __init__(self):
        print u'Linear regression...'

    def LoadData(self, data):
        self.Data = data
        self.Size = len(self.Data)
        if self.Size % 2 == 1:
            print "Error: bad sample size"
            return False
        for Value in self.Data:
            try:
                Value = float(Value)
            except ValueError:
                print "Error: bad value {0} ".format(Value)
                return False
        return True

    def Calculate(self):
        N = self.Size/2
        self.Res = {}
        self.Res['slope'], self.Res['intercept'],\
        self.Res['r_value'], self.Res['p_value'], self.Res['std_err'] =\
        scipy.stats.linregress(numpy.array(self.Data[:N], dtype = float),
                               numpy.array(self.Data[N:], dtype = float))
        return True

    def DoDrawing(self, canvas, style):
        width = canvas.size[0] - 2*canvas.margin[0]
        height = canvas.size[1] - 2*canvas.margin[1]
        (minX, maxX, minY, maxY) = Math.RangeN(self.Data)
        X0 = minX
        Y0 = self.Res['slope']*X0 + self.Res['intercept']
        X1 = maxX
        Y1 = self.Res['slope']*X1 + self.Res['intercept']
        canvas.DrawLine(
            int(2*canvas.margin[0] + (float(X0) - minX)*
                (width - 2*canvas.margin[0])/(maxX - minX)),
            int(height - ((float(Y0) - minY)*
                (height - 2*canvas.margin[1])/(maxY - minY))),
            int(2*canvas.margin[0] + (float(X1) - minX)*
                (width - 2*canvas.margin[0])/(maxX - minX)),
            int(height - ((float(Y1) - minY)*
                (height - 2*canvas.margin[1])/(maxY - minY))),
            color = style['dots_color'], width = style['line_width'])
        canvas.PlotXYData(self.Data, color = style['line_color'],
            radius = style['dots_radius'])

    def PrintResult(self, text):
        summary = "Y = {0:.2}*X + {1:.2}\n".format(self.Res['slope'],
                                                   self.Res['intercept'])
        text.AppendText(summary)
        text.AppendText(u"Slope: {0}\n".format(self.Res['slope']))
        text.AppendText(u"Intercept: {0}\n".format(self.Res['intercept']))
        text.AppendText(u"R-value: {0}\n".format(self.Res['r_value']))
        text.AppendText(u"P value: {0}\n".format(self.Res['p_value']))
        text.AppendText(u"Standard Error: {0}\n".format(self.Res['std_err']))


class SmirnoffTest:

    def __init__(self):
        print "Using Kolmogorov-Smirnov Test..."

    def LoadData(self, data):
        self.Data = data
        self.Size = len(self.Data)
        if self.Size % 2 == 1:
            print "Error: bad sample size"
            return False
        for Record in self.Data:
            for Value in Record:
                try:
                    float(Value)
                except ValueError:
                    # print "Error: bad value {0} at {1}, {2}".
                    # format(Value, idx1, idx2)
                    print "Error: bad value {0} ".format(Value)
                    return False
        return True

    def Calculate(self):
        return 1
