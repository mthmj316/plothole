# -*- coding: utf-8 -*-
"""
Created on Tue Jan  6 18:28:58 2026

@author: mthoma
"""
from abc import abstractmethod
from inspect import currentframe
import logger as log
from observers import UIObserver
from plothole_types import PlotHoleType
import plothole_core as pc
from story_element_ui import __SEControls__ as sec
import helpers as hlp
import json
import file_access as fa

class StoryElementModel(UIObserver):
    
    def __init__(self, ui, base_dir):
        log.log_var(self, currentframe(), ("ui", ui), ("base_dir", base_dir))
        self.base_dir = base_dir
        self.ui = ui
        self.ui.register(self)
        self.this_story_element = None
        self.fq_file_name = ''
        
    def clear(self):
        log.log(self, currentframe())        
        self.this_story_element = None
        self.fq_file_name = ''
    
    @abstractmethod
    def get_plothole_type(self):
        pass
    
    @abstractmethod
    def get_folder(self):
        pass
    
    @abstractmethod
    def get_id(self, from_ui):
        pass
    
    @abstractmethod
    def get_id_name(self):
        pass
    
    @abstractmethod
    def prepare_save(self):
        pass
    
    @abstractmethod
    def after_save(self):
        pass
    
    @abstractmethod
    def load():
        pass
    
    def get_file_name(self):
        log.log(super, currentframe())
        file_name = self.get_id(False)
        log.log_var(self, currentframe(),('file_name',file_name))
        return file_name     
    
    def on_close(self):
        log.log(self, currentframe())
        self.clear()
    
    def on_character(self):
        pass
    
    def on_delete(self):
        log.log(super, currentframe())
        _id = self.get_id(False)
        if _id is not None:        
            folder = self.get_folder()
            phtype = self.get_plothole_type()
            pc.delete(folder, _id, phtype)
        self.clear()

    def on_new(self):
        log.log(self, currentframe())

    def on_next(self):
        log.log(self, currentframe())

    def on_open(self):
        log.log(self, currentframe())

    def on_plothole(self):
        log.log(self, currentframe())

    def on_previous(self):
        log.log(self, currentframe())

    def on_revert(self):
        log.log(self, currentframe())
        self.load()

    def on_save(self):
        log.log(self, currentframe())
        
        if self.this_story_element is not None:
            self.on_update()
            return
            
        _id = self.get_id(True)
        
        if _id == '':
            self.ui.raise_error(f"{self.get_id_name()} muss gesetzt sein.")
            return
        
        if hlp.exists_alias(self.get_folder(), _id):
            self.ui.raise_error(f"{_id} existiert bereits!")
            return
        
        self.prepare_save()
        
        data = json.dumps(self.this_story_element)        
        file_name = "".join(x for x in self.get_file_name() if x.isalnum())
        path = f"{self.get_folder()}/{file_name}"
        self.fq_file_name = f"{path}/{file_name}.{self.get_plothole_type().value}"  
        
        log.log_var(self, currentframe(), ("fq_file_name", self.fq_file_name))

        if not fa.exists(self.fq_file_name):            
            fa.create_dir(path)  
             
        fa.write(self.fq_file_name, data)
         
        self.after_save()

    def on_sub(self):
        log.log(self, currentframe())

    def on_top(self):
        log.log(self, currentframe())
        
    def on_update(self):
        log.log(self, currentframe())

class StoryModel(StoryElementModel):
    
    def __init__(self, ui, base_dir):
        super().__init__(ui, base_dir)
        log.log_var(self, currentframe(), ("ui", ui), ("base_dir", base_dir))
        
    def clear(self):
        log.log(self, currentframe())
        self.ui.set_alias('')
        self.ui.set_title('')
        self.ui.set_genre('')
        self.ui.set_tone('')
        self.ui.set_message('')
        self.ui.set_content('')
        self.ui.enable_alias()
        super().clear()
    
    def get_plothole_type(self):
        log.log(self, currentframe())
        phtype = PlotHoleType.STORY
        log.log_var(self, currentframe(), ("phtype", phtype))
        return phtype
    
    def get_folder(self):
        log.log(self, currentframe())
        folder = self.base_dir
        log.log_var(self, currentframe(), ("folder", folder))
        return folder
    
    def get_id(self, from_ui):
        log.log_var(self, currentframe(),('from_ui',from_ui))
        _id = ''
        
        if from_ui:
            _id = self.ui.get_alias()
        else:
            if self.this_story_element is not None:
                _id = self.this_story_element.get(sec.ALIAS)
        log.log_var(self, currentframe(), ("_id", _id))
        return _id
    
    def get_id_name(self):
        log.log(self, currentframe())
        name = 'Alias'
        log.log_var(self, currentframe(), ("name", name))
        return name
    
    def prepare_save(self):
        log.log(self, currentframe())
        
        alias = self.ui.get_alias()
        title = self.ui.get_title()
        tone = self.ui.get_tone()
        genre = self.ui.get_genre()
        message = self.ui.get_message()
        content = self.ui.get_content()
        
        story = {}        
        story[sec.ALIAS.value] = alias.strip()
        story[sec.TITLE.value] = title.strip()
        story[sec.TONE.value] = tone.strip()
        story[sec.GENRE.value] = genre.strip()
        story[sec.MESSAGE.value] = message.strip()
        story[sec.CONTENT.value] = content.strip()
        
        log.log_var(self, currentframe(), ("story", story))
        
        self.this_story_element = story
        
    def after_save(self):
        log.log(self, currentframe())
        self.ui.disable_alias()
        
    def load(self):
        log.log(self, currentframe())
        story = self.this_story_element
        
        self.ui.set_alias(story.get(sec.ALIAS))
        self.ui.set_title(story.get(sec.TITLE))
        self.ui.set_tone(story.get(sec.TONE))
        self.ui.set_genre(story.get(sec.GENRE))
        self.ui.set_message(story.get(sec.MESSAGE))
        self.ui.set_content(story.get(sec.CONTENT))
        