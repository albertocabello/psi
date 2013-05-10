#!/usr/bin/python
# -*- coding: utf-8 -*-

import lxml.etree
from xml.etree.ElementTree import ElementTree


class XMLProperties:

    def Open(self, filename):
        try:
            self.filename = filename
            self.properties = lxml.etree.parse(filename)
            self.root = self.properties.getroot()
            return True
        except IOError:
            return False

    def Save(self, filename = None):
        try:
            if filename == None:
                filename = self.filename
            writer = ElementTree(self.root)
            writer.write(filename, encoding = 'utf-8')
            return True
        except IOError:
            return False

    def GetProperty(self, component, name):
        return self.root.findtext('component[@id="' + component + '"]/' + name)

    def SetProperty(self, component, name, value):
        node = self.root.find('component[@id="' + component + '"]/' + name)
        node.text = format(value)
        return node

if __name__ == '__main__':
    x = XMLProperties()
    x.Open("properties.xml")
    print x.GetProperty(u'main-window', u'x-size')
    print 'Property: ', x.SetProperty(u'main-window', u'x-size', 342).text
    x.Save("properties2.xml")
