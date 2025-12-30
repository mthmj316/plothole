# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 14:40:56 2025

@author: mthoma
"""
import json
from observers import UIObserver
import file_access as fs

import helpers as h
import plothole_core  as pcore
from inspect import currentframe
import logger as log

class StoryOverviewModel(UIObserver):
    
    def __init__(self, ui, base_dir):
        log.log_var(self, currentframe(), ("ui", ui), ("base_dir", base_dir))
        self.ui = ui
        self.base_dir = base_dir
        
        self.__load_aliases__()
        
    def __load_aliases__(self):
        log.log(self, currentframe())
        for alias in h.get_all_aliases(self.base_dir):
            self.ui.create_story_button(alias)
    
    def onClose(self):
        log.log(self, currentframe())
    
    def onDelete(self):
        log.log(self, currentframe())
    
    def onLoad(self, file_path):
        log.log_var(self, currentframe(), ("file_path", file_path))
    
    def onRevert(self):
        log.log(self, currentframe())
    
    def onSave(self):
        log.log(self, currentframe())
    
    def onUpdate(self):
        log.log(self, currentframe())
    
    def onSelect(self, selected, _type):
        pass
    
    def onDisplay(self, origin):
        log.log_var(self, currentframe(), ("origin", origin))
        if self.ui == origin:
            pass

class StoryModel(UIObserver):
    
    def __init__(self, ui, base_dir):
        log.log_var(self, currentframe(), ("ui", ui), ("base_dir", base_dir))
        self.base_dir = base_dir
        self.ui = ui
        self.ui.set_base_dir(base_dir)
        self.ui.register(self)
        self.fq_file_name = ""
        self.story = None
    
    def onSave(self):
        log.log(self, currentframe())
        
        if self.story is not None:
            self.onUpdate()
            return
        
        alias = self.ui.get_alias()  
        log.log_var(self, currentframe(), ("alias", alias))     

        if alias == "":
            self.ui.raise_error("Alias muss gesetzt sein!")
            return
        elif h.exists_alias(self.base_dir, alias):
            self.ui.raise_error("Alias existiert bereits!")
            return
        
        title = self.ui.get_title()
        accent = self.ui.get_accent()
        genre = self.ui.get_genre()
        message = self.ui.get_message()
        basic_idea = self.ui.get_basic_idea()
        
        self.story = {}        
        self.story["alias"] = alias
        self.story["title"] = title
        self.story["accent"] = accent
        self.story["genre"] = genre
        self.story["message"] = message
        self.story["basic_idea"] = basic_idea  
        log.log_var(self, currentframe(), ("story", self.story))
        
        story_data = json.dumps(self.story) 
        
        file_name = "".join(x for x in alias if x.isalnum())
                
        story_path = f"{self.base_dir}/{file_name}"
        self.fq_file_name = f"{story_path}/{file_name}.story"  
        log.log_var(self, currentframe(), ("fq_file_name", self.fq_file_name))
        
        if not fs.exists(self.fq_file_name):            
            fs.create_dir(story_path)  
            
        fs.write(self.fq_file_name, story_data)
        
        self.ui.disable_alias()
        
    
    def onDelete(self):
        log.log(self, currentframe())
        if len(self.fq_file_name) > 0:            
            pcore.delete_story(self.base_dir, self.story.get('alias'))
            self.onClose()
        
    
    def onUpdate(self):
        log.log(self, currentframe())
        
        title = self.ui.get_title()
        accent = self.ui.get_accent()
        genre = self.ui.get_genre()
        message = self.ui.get_message()
        basic_idea = self.ui.get_basic_idea()
        
        self.story["title"] = title
        self.story["accent"] = accent
        self.story["genre"] = genre
        self.story["message"] = message
        self.story["basic_idea"] = basic_idea
        
        story_data = json.dumps(self.story)
        fs.write(self.fq_file_name, story_data)
        
        self.updateUI()
                        
    def updateUI(self):
        log.log(self, currentframe())
        self.ui.set_alias(self.story.get('alias'))
        self.ui.set_title(self.story.get('title'))
        self.ui.set_accent(self.story.get('accent'))
        self.ui.set_genre(self.story.get('genre'))
        self.ui.set_message(self.story.get('message'))
        self.ui.set_basic_idea(self.story.get('basic_idea'))
      
    def onLoad(self, file_name):
        log.log_var(self, currentframe(), ("file_name", file_name))
        
        if file_name is not None and len(file_name) > 0:            
            self.fq_file_name = file_name            
            self.story = h.get_story(self.fq_file_name, as_dict=True)
            self.updateUI()
            self.ui.disable_alias()
    
    def onRevert(self): 
        log.log(self, currentframe())       
        if len(self.fq_file_name) > 0:            
            self.onLoad(self.fq_file_name)
        else:
            self.onClose()
    
    def onClose(self):
        log.log(self, currentframe())
        
        self.ui.set_alias("")
        self.ui.set_title("")
        self.ui.set_accent("")
        self.ui.set_genre("")
        self.ui.set_message("")
        self.ui.set_basic_idea("")
        self.ui.enable_alias()
        self.fq_file_name = ""
        self.story = None
    
    def onSelect(self, selected, _type): 
        log.log_var(self, currentframe(), ("selected", selected), ("_type", _type))
    
    def onDisplay(self, origin):
        log.log_var(self, currentframe(), ("origin", origin))
        if self.ui == origin:
            pass