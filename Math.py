#! /usr/bin/env python
#coding=utf-8

import numpy


def RangeN(data):
    MinX = min(numpy.array(data[:len(data)/2], dtype = float))
    MaxX = max(numpy.array(data[:len(data)/2], dtype = float))
    MinY = min(numpy.array(data[len(data)/2:], dtype = float))
    MaxY = max(numpy.array(data[len(data)/2:], dtype = float))
    return (MinX, MaxX, MinY, MaxY)

if __name__ == '__main__':
    data = ['4', '6', '7', '-0.4', '14', '-4.6', '2', '1.55']
    print RangeN(data)
