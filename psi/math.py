#! /usr/bin/env python
#coding=utf-8

import numpy


def RGYBMap(index):
    r = g = b = None
    if index >= 0 and index*255 <= 85:
        # r = 255, g from 0 to 255, b = 0
        r = 255
        g = 255 * index * 3
        b = 0
    if index*255 > 85 and index*255 <= 170:
        # r from 255 to 0, g = 255, b = 0
        r = 255 * (2 - index*3)
        g = 255
        b = 0
    if index*255 > 170 and index <= 1:
        # r = 0, g from 255 to 0, b from 0 to 255
        r = 0
        g = 255 * (3 - index*3)
        b = 255 - g
    return (r, g, b)

def RangeN(data):
    MinX = min(numpy.array(data[:len(data)/2], dtype=float))
    MaxX = max(numpy.array(data[:len(data)/2], dtype=float))
    MinY = min(numpy.array(data[len(data)/2:], dtype=float))
    MaxY = max(numpy.array(data[len(data)/2:], dtype=float))
    return (MinX, MaxX, MinY, MaxY)


class Map:

    def __init__(self, (min_x, max_x, min_y, max_y),
                       (left_map, right_map, bottom_map, top_map)):
        self.map = {}
        self.map['x0'] = left_map
        self.map['x1'] = right_map
        self.map['y0'] = bottom_map
        self.map['y1'] = top_map
        self.real = {}
        self.real['x0'] = min_x
        self.real['x1'] = max_x
        self.real['y0'] = min_y
        self.real['y1'] = max_y

    def SetMapSize(self, (left_map, right_map, bottom_map, top_map)):
        self.map['x0'] = left_map
        self.map['x1'] = right_map
        self.map['y0'] = bottom_map
        self.map['y1'] = top_map

    def SetRealSize(self, (min_x, max_x, min_y, max_y)):
        self.real['x0'] = min_x
        self.real['x1'] = max_x
        self.real['y0'] = min_y
        self.real['y1'] = max_y

    def MapPoint(self, (x, y)):
        real_width = self.real['x1'] - self.real['x0']
        map_width = self.map['x1'] - self.map['x0']
        real_height = self.real['y1'] - self.real['y0']
        map_height = self.map['y1'] - self.map['y0']
        mapx = self.map['x0'] + ((x - self.real['x0'])*map_width)/real_width
        mapy = self.map['y1'] - ((y - self.real['y0'])*map_height)/real_height
        return (mapx, mapy)

    def UnMap(self, (x, y)):
        reverse_map = Map(
            (self.map['x0'], self.map['x1'],
             self.map['y0'], self.map['y1']),
            (self.real['x0'], self.real['x1'],
             self.real['y0'], self.real['y1']))
        return reverse_map.MapPoint((x, y))

if __name__ == '__main__':
    data = ['4', '6', '7', '-0.4', '14', '-4.6', '2', '1.55']
    print u'Range of ', data
    print RangeN(data)

    real = (-10, 10, 10, 20)
    map = (0, 10, 0, 10)
    a = Map(real, map)
    print u'Mapping', real, u'onto', map
    for i in ((-10, 15), (0, 15), (10, 15), (0, 10), (0, 15), (0, 20)):
        print i, u'->', a.MapPoint(i)
    print u'Unmapping', real, u'from', map
    for i in ((1, 1), (0, 5), (5, 1), (7, 2)):
        print i, u'<-', a.UnMap(i)
