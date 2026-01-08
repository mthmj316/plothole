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
    def on_close(self, event_source_ph_type):
        pass
         
    @abstractmethod       
    def on_delete(self):
        pass

    @abstractmethod
    def on_new(self, event_source_ph_type):
        pass

    @abstractmethod
    def on_open(self, event_source_ph_type):
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
        
    def on_close(self, event_source_ph_type):
        log.log_var(self, currentframe(), ("event_source_ph_type", event_source_ph_type))
        
        log.log_var(self, currentframe(), ("current_frame", self.current_frame))
        log.log_var(self, currentframe(), ("current_ph_type", self.current_ph_type))
        
        if  self.current_ph_type == PlotHoleType.STORY and event_source_ph_type == PlotHoleType.STORY:
            # you are currently on the story ui frame
            # and you want to change back to the story overview frame
            next_frame = self.ui_overview_frames_dict.get(PlotHoleType.STORY)
            next_frame.tkraise(aboveThis=self.current_frame)
            self.current_frame = next_frame            
            self.current_ph_type = None # no story element is selected
            
        elif self.current_ph_type == PlotHoleType.STORY and event_source_ph_type == PlotHoleType.BOOK:
            # you are currently on the book overview frame
            # and the close button has been pressed
            # hence go back to story ui
            next_frame = self.ui_frames_dict.get(PlotHoleType.STORY)
            next_frame.tkraise(aboveThis=self.current_frame)
            self.current_frame = next_frame            
            self.current_ph_type = PlotHoleType.STORY
            
        elif self.current_ph_type == PlotHoleType.BOOK and event_source_ph_type == PlotHoleType.BOOK:
            # you are currently on the book ui frame
            # and the close button has been pressed
            # hence go back to story ui
            next_frame = self.ui_overview_frames_dict.get(PlotHoleType.BOOK)
            next_frame.tkraise(aboveThis=self.current_frame)
            self.current_frame = next_frame            
            self.current_ph_type = PlotHoleType.STORY
         
    def on_delete(self):
        pass

    def on_new(self, event_source_ph_type):
        log.log(self, currentframe())
        
        log.log_var(self, currentframe(), ("current_frame", self.current_frame))
        log.log_var(self, currentframe(), ("current_ph_type", self.current_ph_type))
        
        if self.current_ph_type is None:
            # You are on story overview ui and a story must be created
            next_frame = self.ui_frames_dict.get(PlotHoleType.STORY)
            next_frame.tkraise(aboveThis=self.current_frame)
            self.current_frame = next_frame
            self.current_ph_type = PlotHoleType.STORY
        elif event_source_ph_type is PlotHoleType.BOOK:
            # you are on the book overview and want to change to the book ui
            next_frame = self.ui_frames_dict.get(PlotHoleType.BOOK)
            next_frame.tkraise(aboveThis=self.current_frame)
            self.current_frame = next_frame
            self.current_ph_type = event_source_ph_type

    def on_open(self, event_source_ph_type):
        log.log_var(self, currentframe(), ("event_source_ph_type", event_source_ph_type))
        
        log.log_var(self, currentframe(), ("current_frame", self.current_frame))
        log.log_var(self, currentframe(), ("current_ph_type", self.current_ph_type))
        
        if self.current_ph_type is None and event_source_ph_type == PlotHoleType.STORY:
            # You are on story overview ui and a story has been selected
            next_frame = self.ui_frames_dict.get(PlotHoleType.STORY)
            next_frame.tkraise(aboveThis=self.current_frame)
            self.current_frame = next_frame
            self.current_ph_type = PlotHoleType.STORY
            
        elif self.current_ph_type == PlotHoleType.STORY and event_source_ph_type == PlotHoleType.STORY:
            # You are on story ui (story is selected) and the books button has been pressed
            next_frame = self.ui_overview_frames_dict.get(PlotHoleType.BOOK)
            next_frame.tkraise(aboveThis=self.current_frame)
            self.current_frame = next_frame
            self.current_ph_type = PlotHoleType.STORY
        
        elif self.current_ph_type == PlotHoleType.STORY and event_source_ph_type == PlotHoleType.BOOK:
            # You are on story ui (story is selected) and the books button has been pressed
            next_frame = self.ui_frames_dict.get(PlotHoleType.BOOK)
            next_frame.tkraise(aboveThis=self.current_frame)
            self.current_frame = next_frame
            self.current_ph_type = PlotHoleType.BOOK       
    
    def on_plothole(self):
        pass
        
    def on_previous(self):
        pass
        
    def on_sub(self):
        log.log(self, currentframe())
        if self.current_ph_type is PlotHoleType.STORY:
            # You are on the story ui and want to change to book overview ui
            next_frame = self.ui_overview_frames_dict.get(PlotHoleType.BOOK)
            next_frame.tkraise(aboveThis=self.current_frame)
            self.current_frame = next_frame
            # It shouldn't really be necessary, but better safe than sorry.
            self.current_ph_type = PlotHoleType.STORY
        
    def on_top(self):
        log.log(self, currentframe())
        # Always change to the story overview 
        next_frame = self.ui_overview_frames_dict.get(PlotHoleType.STORY)
        next_frame.tkraise(aboveThis=self.current_frame)
        self.current_frame = next_frame            
        self.current_ph_type = None