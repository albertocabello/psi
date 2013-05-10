#! /usr/bin/env python
#coding=utf-8

import scipy.stats
import numpy
import Math


class LinearRegression:

    def __init__(self):
        print "Using linear regression..."

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
        return self.Res

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
