#! /usr/bin/env python
#coding=utf-8

import scipy.stats
import numpy


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
        Res = {}
        for i in ( 'slope', 'intercept', 'r_value', 'p_value', 'std_err'):
            Res[i] = ''
        Res['slope'], Res['intercept'],\
        Res['r_value'], Res['p_value'], Res['std_err'] =\
        scipy.stats.linregress(numpy.array(self.Data[:N], dtype = float),
                               numpy.array(self.Data[N:], dtype = float))
        return Res

    def DoDrawing(self, Style):
        return


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
