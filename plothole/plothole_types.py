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
    'plothole': 'plotholedump',
    'character': 'characterdump'
    }

class PlotHoleType(enum.StrEnum):    
    STORY = 'story'
    BOOK = 'book'
    PART = 'part'
    CHAPTER = 'chapter'
    SCENE = 'scene'
    PAGE = 'page'
    PANEL = 'panel'
    PLOTHOLE = 'plothole'
    CHARATCTER = 'character'