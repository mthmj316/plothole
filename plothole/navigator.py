# -*- coding: utf-8 -*-
"""
Created on Tue Jan  6 18:42:30 2026

@author: mthoma
"""

from abc import ABC, abstractmethod
from inspect import currentframe
import logger as log
from plothole_types import PlotHoleType

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
    
class NavigatorInstance(ABC):
    
    def __init__(self, start_frame, ui_frames_dict, ui_overview_frames_dict):
        log.log_var(self, currentframe(), ("start_frame", start_frame), 
                    ("ui_frames_dict", ui_frames_dict), 
                    ("ui_overview_frames_dict", ui_overview_frames_dict))
        
        self.current_frame, self.ui_frames_dict, self.ui_overview_frames_dict = start_frame, ui_frames_dict, ui_overview_frames_dict
        self.current_ph_type = None
    
    def on_character(self):
        pass
        
    def on_close(self):
        log.log(self, currentframe())
        if  self.current_ph_type == PlotHoleType.STORY:
            # you are currently on the story ui frame
            # and you want to change back to the story overview frame
            next_frame = self.ui_overview_frames_dict.get(PlotHoleType.STORY)
            next_frame.tkraise(aboveThis=self.current_frame)
            self.current_frame = next_frame            
            self.current_ph_type = None
            
         
    def on_delete(self):
        pass

    def on_new(self):
        log.log(self, currentframe())
        if self.current_ph_type is None:
            # You are on story overview ui and a story must be created
            next_frame = self.ui_frames_dict.get(PlotHoleType.STORY)
            next_frame.tkraise(aboveThis=self.current_frame)
            self.current_frame = next_frame
            self.current_ph_type = PlotHoleType.STORY

    def on_open(self, ph_type):
        log.log_var(self, currentframe(), ("ph_type", ph_type))
        
        if self.current_ph_type is None and ph_type == PlotHoleType.STORY:
            # You are on story overview ui and a story has been selected
            next_frame = self.ui_frames_dict.get(PlotHoleType.STORY)
            next_frame.tkraise(aboveThis=self.current_frame)
            self.current_frame = next_frame
        
        self.current_ph_type = ph_type
    
    def on_plothole(self):
        pass
        
    def on_previous(self):
        pass
        
    def on_sub(self):
        pass
        
    def on_top(self):
        pass