#!/usr/bin/env python
class structure():

    def __init__(self,type,contant):
        self._type=type
        self._contant=contant
    @property
    def type(self):
        return self._name
    @property
    def contant(self):
        return self._contant
    @type.setter
    def type(self,a):
        self._type=a

    @contant.setter
    def contant(self.b):
        self._contant=b

def main():
    a = structure()
