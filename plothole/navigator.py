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
        self.frame_before_plothole = None
        self.ph_type_before_plothole = None
        self.before_character = None
    
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

        elif self.current_ph_type == PlotHoleType.BOOK and event_source_ph_type == PlotHoleType.PART:
            # You are on part overview and the close button has been pressed.
            next_frame = self.ui_frames_dict.get(PlotHoleType.BOOK)
            next_frame.tkraise(aboveThis=self.current_frame)
            self.current_frame = next_frame
            self.current_ph_type = PlotHoleType.BOOK  
            
        elif self.current_ph_type == PlotHoleType.PART and event_source_ph_type == PlotHoleType.PART:
            # You are on part ui and the close button has been pressed.
            # No part is selected -> book selected
            next_frame = self.ui_overview_frames_dict.get(PlotHoleType.PART)
            next_frame.tkraise(aboveThis=self.current_frame)
            self.current_frame = next_frame
            self.current_ph_type = PlotHoleType.BOOK  

        elif self.current_ph_type == PlotHoleType.PART and event_source_ph_type == PlotHoleType.CHAPTER:
            # You are on chapter overview ui and the close button has been pressed.
            next_frame = self.ui_frames_dict.get(PlotHoleType.PART)
            next_frame.tkraise(aboveThis=self.current_frame)
            self.current_frame = next_frame
            self.current_ph_type = PlotHoleType.PART

        elif self.current_ph_type == PlotHoleType.CHAPTER and event_source_ph_type == PlotHoleType.CHAPTER:
            # You are on chapter ui and the close button has been pressed.
            next_frame = self.ui_overview_frames_dict.get(PlotHoleType.CHAPTER)
            next_frame.tkraise(aboveThis=self.current_frame)
            self.current_frame = next_frame
            self.current_ph_type = PlotHoleType.PART
            
        elif self.current_ph_type != PlotHoleType.PLOTHOLE and event_source_ph_type == PlotHoleType.PLOTHOLE:
            # You are on plothole overview ui and close has been clicked.
            next_frame = self.frame_before_plothole
            next_frame.tkraise(aboveThis=self.current_frame)
            self.current_frame = next_frame
            self.current_ph_type = self.ph_type_before_plothole
            self.ph_type_before_plothole = None
            
        elif self.current_ph_type == PlotHoleType.PLOTHOLE and event_source_ph_type == PlotHoleType.PLOTHOLE:
            # You are on plothole ui and close has been clicked.
            next_frame = self.ui_overview_frames_dict.get(PlotHoleType.PLOTHOLE)
            next_frame.tkraise(aboveThis=self.current_frame)
            self.current_frame = next_frame
            self.current_ph_type = self.ph_type_before_plothole
            
        # elif self.current_ph_type == PlotHoleType.SCENE and event_source_ph_type == PlotHoleType.CHAPTER:
        #     # You are on scene overview ui and close button has been clicked.
        #     next_frame = self.ui_frames_dict.get(PlotHoleType.CHAPTER)
        #     next_frame.tkraise(aboveThis=self.current_frame)
        #     self.current_frame = next_frame
        #     self.current_ph_type = PlotHoleType.CHAPTER
            
        elif self.current_ph_type == PlotHoleType.SCENE and event_source_ph_type == PlotHoleType.SCENE:
            # You are on scene ui and close button has been clicked.
            next_frame = self.ui_overview_frames_dict.get(PlotHoleType.SCENE)
            next_frame.tkraise(aboveThis=self.current_frame)
            self.current_frame = next_frame
            self.current_ph_type = PlotHoleType.CHAPTER

        elif self.current_ph_type == PlotHoleType.CHAPTER and event_source_ph_type == PlotHoleType.SCENE:
            # You are on scene overview ui and close button has been clicked.
            next_frame = self.ui_frames_dict.get(PlotHoleType.CHAPTER)
            next_frame.tkraise(aboveThis=self.current_frame)
            self.current_frame = next_frame
            self.current_ph_type = PlotHoleType.CHAPTER
            
    def on_delete(self):
        pass

    def on_new(self, event_source_ph_type):
        log.log_var(self, currentframe(), ('event_source_ph_type',event_source_ph_type))
        
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
            
        elif event_source_ph_type is PlotHoleType.PART:
            # you are on the part overview and want to create a new part
            next_frame = self.ui_frames_dict.get(PlotHoleType.PART)
            next_frame.tkraise(aboveThis=self.current_frame)
            self.current_frame = next_frame
            self.current_ph_type = event_source_ph_type
        
        elif event_source_ph_type is PlotHoleType.CHAPTER:
            # you are on the chapter overview and the new button has been pressed.
            next_frame = self.ui_frames_dict.get(PlotHoleType.CHAPTER)
            next_frame.tkraise(aboveThis=self.current_frame)
            self.current_frame = next_frame
            self.current_ph_type = event_source_ph_type
            
        elif event_source_ph_type is PlotHoleType.PLOTHOLE:
            # you are on the plothole overview and want to create a new plothole
            next_frame = self.ui_frames_dict.get(PlotHoleType.PLOTHOLE)
            next_frame.tkraise(aboveThis=self.current_frame)
            self.current_frame = next_frame
            self.current_ph_type = event_source_ph_type

        elif event_source_ph_type is PlotHoleType.SCENE:
            # you are on the scene overview and the new button has been pressed.
            next_frame = self.ui_frames_dict.get(PlotHoleType.SCENE)
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
            self.current_ph_type = event_source_ph_type
            
        elif self.current_ph_type == PlotHoleType.STORY and event_source_ph_type == PlotHoleType.STORY:
            # You are on story ui (story is selected) and the books button has been pressed
            next_frame = self.ui_overview_frames_dict.get(PlotHoleType.BOOK)
            next_frame.tkraise(aboveThis=self.current_frame)
            self.current_frame = next_frame
            self.current_ph_type = event_source_ph_type
        
        elif self.current_ph_type == PlotHoleType.STORY and event_source_ph_type == PlotHoleType.BOOK:
            # You are on story ui (story is selected) and the books button has been pressed
            next_frame = self.ui_frames_dict.get(PlotHoleType.BOOK)
            next_frame.tkraise(aboveThis=self.current_frame)
            self.current_frame = next_frame
            self.current_ph_type = event_source_ph_type       
            
        elif self.current_ph_type == PlotHoleType.BOOK and event_source_ph_type == PlotHoleType.PART:
            # You are on part overview ui (book is selected) and a part has been double clicked.
            next_frame = self.ui_frames_dict.get(PlotHoleType.PART)
            next_frame.tkraise(aboveThis=self.current_frame)
            self.current_frame = next_frame
            self.current_ph_type = event_source_ph_type
            
        elif self.current_ph_type == PlotHoleType.PART and event_source_ph_type == PlotHoleType.CHAPTER:
            # You are on chapter overview ui and a chapter has been double clicked.
            next_frame = self.ui_frames_dict.get(PlotHoleType.CHAPTER)
            next_frame.tkraise(aboveThis=self.current_frame)
            self.current_frame = next_frame
            self.current_ph_type = event_source_ph_type
            
        elif self.current_ph_type != PlotHoleType.PLOTHOLE and event_source_ph_type == PlotHoleType.PLOTHOLE:
            # You are on plothole overview ui and a plothole shall be edited
            # self.frame_before_plothole = self.current_frame
            # self.ph_type_before_plothole = self.current_ph_type
            
            next_frame = self.ui_frames_dict.get(PlotHoleType.PLOTHOLE)
            next_frame.tkraise(aboveThis=self.current_frame)
            self.current_frame = next_frame
            self.current_ph_type = event_source_ph_type
            
            # log.log_var(self, currentframe(), ("current_frame", self.current_frame))
            # log.log_var(self, currentframe(), ("frame_before_plothole", self.frame_before_plothole))
 
        elif self.current_ph_type == PlotHoleType.CHAPTER and event_source_ph_type == PlotHoleType.SCENE:
            # You are on scene overview ui and a scene has been double clicked.
            next_frame = self.ui_frames_dict.get(PlotHoleType.SCENE)
            next_frame.tkraise(aboveThis=self.current_frame)
            self.current_frame = next_frame
            self.current_ph_type = event_source_ph_type
    
    def on_plothole(self):
        log.log(self, currentframe())
        
        log.log_var(self, currentframe(), ("current_frame", self.current_frame))
        log.log_var(self, currentframe(), ("current_ph_type", self.current_ph_type))
        
        self.frame_before_plothole = self.current_frame
        self.ph_type_before_plothole = self.current_ph_type
        log.log_var(self, currentframe(), ("frame_before_plothole", self.frame_before_plothole))
        log.log_var(self, currentframe(), ("ph_type_before_plothole", self.ph_type_before_plothole))

        # self.current_ph_type = PlotHoleType.PLOTHOLE
        next_frame = self.ui_overview_frames_dict.get(PlotHoleType.PLOTHOLE)
        next_frame.tkraise(aboveThis=self.current_frame)
        self.current_frame = next_frame
            
        
    def on_previous(self):
        pass
        
    def on_sub(self):
        log.log(self, currentframe())
        
        log.log_var(self, currentframe(), ("current_frame", self.current_frame))
        log.log_var(self, currentframe(), ("current_ph_type", self.current_ph_type))
        
        if self.current_ph_type is PlotHoleType.STORY:
            # You are on the story ui and want to change to book overview ui
            next_frame = self.ui_overview_frames_dict.get(PlotHoleType.BOOK)
            log.log_var(self, currentframe(), ("next_frame", next_frame))
            next_frame.tkraise(aboveThis=self.current_frame)
            self.current_frame = next_frame
            # It shouldn't really be necessary, but better safe than sorry.
            self.current_ph_type = PlotHoleType.STORY
            
        if self.current_ph_type is PlotHoleType.BOOK:
            # You are on the book ui and want to change to part overview ui
            next_frame = self.ui_overview_frames_dict.get(PlotHoleType.PART)
            log.log_var(self, currentframe(), ("next_frame", next_frame))
            next_frame.tkraise(aboveThis=self.current_frame)
            self.current_frame = next_frame
            # It shouldn't really be necessary, but better safe than sorry.
            self.current_ph_type = PlotHoleType.BOOK
            
        if self.current_ph_type is PlotHoleType.PART:
            # You are on the part ui and want to change to chapter overview ui
            next_frame = self.ui_overview_frames_dict.get(PlotHoleType.CHAPTER)
            log.log_var(self, currentframe(), ("next_frame", next_frame))
            next_frame.tkraise(aboveThis=self.current_frame)
            self.current_frame = next_frame
            # It shouldn't really be necessary, but better safe than sorry.
            self.current_ph_type = PlotHoleType.PART

        elif self.current_ph_type == PlotHoleType.CHAPTER:
            # You are on chapter ui and the scene button has been pressed.
            next_frame = self.ui_overview_frames_dict.get(PlotHoleType.SCENE)
            log.log_var(self, currentframe(), ("next_frame", next_frame))
            next_frame.tkraise(aboveThis=self.current_frame)
            self.current_frame = next_frame
            # self.current_ph_type = ... not needed to be set
        
    def on_top(self):
        log.log(self, currentframe())
        # Always change to the story overview 
        next_frame = self.ui_overview_frames_dict.get(PlotHoleType.STORY)
        next_frame.tkraise(aboveThis=self.current_frame)
        self.current_frame = next_frame            
        self.current_ph_type = None