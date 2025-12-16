# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 11:45:34 2025

@author: mthoma
"""
import enum

class PlotHoleType(enum.IntEnum):    
    STORY = 0
    BOOK = 1
    PART = 2
    CHAPTER = 3
    SCENE = 4
    PAGE = 5
    PANEL = 6