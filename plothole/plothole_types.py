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
    'page': 'pagedump',
    'panel': 'paneldump',
    'plothole': 'plotholedump'
    }

class PlotHoleType(enum.IntEnum):    
    STORY = 0
    BOOK = 1
    PART = 2
    CHAPTER = 3
    SCENE = 4
    PAGE = 5
    PANEL = 6
    PLOTHOLE = 7