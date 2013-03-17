#!/usr/bin/python
# -*- coding: utf-8 -*-


import lxml.etree

class XMLProperties:

    def New(self):
        return

    def Open(self, filename):
        self.properties = lxml.etree.parse('properties.xml')
        self.root = self.properties.getroot()
        return

    def Save(save):
        lxml.etree.tostring(self.root)
        return

    def GetProperty(self, component, name):
        return self.root.findtext('component[@id="' + component + '"]/' + name)

    def SetProperty(self, component, name, value):
        return
