# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 11:45:34 2025

@author: mthoma
"""
import enum

FILE_EXTENSIONS_DUMP = {    
    'story': 'storydump',
    'book': 'bookdump',
    'part': 'partdump',
    'chapter': 'chapterdump',
    'scene': 'scenedump',
    'panel': 'paneldump',
    'plothole': 'plotholedump',
    'character': 'characterdump'
    }

class PlotHoleType(enum.StrEnum):    
    STORY = 'story'
    BOOK = 'book'
    PART = 'part'
    CHAPTER = 'chapter'
    SCENE = 'scene'
    PANEL = 'panel'
    PLOTHOLE = 'plothole'
    CHARATCTER = 'character'
    
    @classmethod
    def length(cls):
        return len(PlotHoleType)
    
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
    
    @classmethod
    def __ordinals(cls):
        return {
            name: PlotHoleType.length() - idx
            for idx, name in enumerate(PlotHoleType.list())
        }
 
    @classmethod
    def plotholtype_by_ordinal(cls, ordinal):
        for name, idx in cls.__ordinals().items():
            # print(f"{name} -> {idx}")
            if ordinal == idx:
                return PlotHoleType[name.upper()]
        return None

    def ordinal(self):
        return PlotHoleType.__ordinals().get(self)
    
    def __lt__(self, other):
        self_ordinal = self.ordinal()
        other_ordinal = other.ordinal()
        return self_ordinal < other_ordinal
    
    def __gt__(self, other):
        self_ordinal = self.ordinal()
        other_ordinal = other.ordinal()
        return self_ordinal > other_ordinal

PLOTHOLE_TYPE_VALUE_TO_UI_DISPLAY_MAP = {
    'story': 'Geschichte',
    'book': 'Buch',
    'part': 'Teil',
    'chapter': 'Kapitel',
    'scene': 'Szene',
    'panel': 'Panel',
    'plothole': 'Plothole',
    'character': 'Charakter'
    }
    

UI_DISPLAY_TO_PLOTHOLE_TYPE_VALUE_MAP = {
    'Geschichte': 'story',
    'Buch': 'book',
    'Teil': 'part',
    'Kapitel': 'chapter',
    'Szene': 'scene',
    'Panel': 'panel',
    'Plothole': 'plothole',
    'Charakter': 'character'
    }

CHILD_PLOTHOLE_TYPE = {
    'story': 'book',
    'book': 'part',
    'part': 'chapter',
    'chapter': 'scene',
    'scene': 'panel',
    'panel': None
    }

PARENT_PLOTHOLE_TYPE = {
    'panel': 'scene',
    'scene': 'chapter',
    'chapter': 'part',
    'part': 'book',
    'book': 'story',
    'story': None
    }
    
if __name__ == '__main__':

    print(PlotHoleType.PART.__lt__(PlotHoleType.BOOK))
    print(PlotHoleType.PART.__lt__(PlotHoleType.PLOTHOLE))
    
    print(PlotHoleType.plotholtype_by_ordinal(5))
    print(PlotHoleType.plotholtype_by_ordinal(9))
    print(PlotHoleType.plotholtype_by_ordinal(2))
    
  
    