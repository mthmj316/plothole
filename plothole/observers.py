# -*- coding: utf-8 -*-
"""
Created on Thu Dec 11 15:04:21 2025

@author: mthoma
"""

from abc import ABC
from abc import abstractmethod

class UIObservable(ABC):
    
    @abstractmethod
    def register(self, uiobserver):
        """
        register an observer of type Observer

        Returns
        -------
        None.

        """
        
    @abstractmethod
    def unregister(self, uiobserver):
        """
        register an observer of type Observer

        Returns
        -------
        None.

        """

class UIObserver(ABC):
        
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
    def on_next(self):
        pass
        
    @abstractmethod
    def on_open(self):
        pass
        
    @abstractmethod
    def on_plothole(self):
        pass
        
    @abstractmethod
    def on_previous(self):
        pass
        
    @abstractmethod
    def on_revert(self):
        pass
        
    @abstractmethod
    def on_save(self):
        pass
        
    @abstractmethod
    def on_sub(self):
        pass
        
    @abstractmethod
    def on_top(self):
        pass
         
    @abstractmethod       
    def on_update(self):
        pass
