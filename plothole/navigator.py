# -*- coding: utf-8 -*-
"""
Created on Tue Jan  6 18:42:30 2026

@author: mthoma
"""

from abc import ABC, abstractmethod
from inspect import currentframe
import logger as log

class NavigationPoint(ABC):
    
    @abstractmethod
    def add_navigator(self, navigator):
        pass
        
    @abstractmethod
    def remove_mavigator(self, navigator):
        pass
    
class Navigator(ABC):
    
    @abstractmethod
    def on_character(self):
        pass
        
    @abstractmethod
    def on_close(self):
        pass
         
    @abstractmethod       
    def on_delete(self):
        pass

    @abstractmethod
    def on_new(self):
        pass

    @abstractmethod
    def on_open(self, ph_type):
        pass
    
    @abstractmethod
    def on_plothole(self):
        pass
        
    @abstractmethod
    def on_previous(self):
        pass
        
    @abstractmethod
    def on_sub(self):
        pass
        
    @abstractmethod
    def on_top(self):
        pass