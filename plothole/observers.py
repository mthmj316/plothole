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
    def onSave(self):
        """
        Is called in case of a save event

        Returns
        -------
        None.

        """

    @abstractmethod    
    def onUpdate(self):
        """
        Is called in case of a update event

        Returns
        -------
        None.

        """
   
    @abstractmethod
    def onDelete(self):
        """
        Is called in case of a delete event

        Returns
        -------
        None.

        """
        
    @abstractmethod
    def onLoad(self, file_path):
        """
        Is called in case of a delete event
        Returns
        -------
        None.
        """

    @abstractmethod
    def onRevert(self):
        """
        Is called in case of a delete event
        Returns
        -------
        None.
        """
        
    @abstractmethod
    def onClose(self):
        """
        Is called in case of a delete event
        Returns
        -------
        None.
        """