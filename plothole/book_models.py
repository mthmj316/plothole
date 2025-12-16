# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 14:40:56 2025

@author: mthoma
"""
import json
from observers import UIObserver
import file_access as fs
import helpers as h
import pathlib

from plothole_types import PlotHoleType

class BookModel(UIObserver):
    
    def __init__(self, ui, base_dir):
        self.ui = ui
        self.base_dir = base_dir  
        self.selected_story_fqname = ''
        self.book_path = ''
        self.fq_file_name = ''
        self.ui.register(self)
        self.book = None
    
    def onClose(self):
        pass
    
    def onDelete(self):
        pass
    
    def onLoad(self, file_path):
        pass
    
    def onRevert(self):
        pass
    
    def onSave(self):
        
        if self.book is not None:
            self.onUpdate()
            return
        
        alias = self.ui.get_alias()       

        if alias == "":
            self.ui.raise_error("Alias muss gesetzt sein!")
            return
        if h.exists_alias(self.book_path, alias, 'book'):
            self.ui.raise_error("Alias existiert bereits!")
            return
        
        title = self.ui.get_title()
        accent = self.ui.get_accent()
        message = self.ui.get_message()
        basic_idea = self.ui.get_basic_idea()
        
        self.story = {} 
        self.story["parent"] = self.selected_story
        self.story["alias"] = alias
        self.story["title"] = title
        self.story["accent"] = accent
        self.story["message"] = message
        self.story["basic_idea"] = basic_idea
        
        story_data = json.dumps(self.story) 
        
        if not fs.exists(self.book_path):            
            fs.create_dir(self.book_path)  
            
        file_name = "".join(x for x in alias if x.isalnum())
        self.fq_file_name = f"{self.book_path}/{file_name}.book"
            
        fs.write(self.fq_file_name, story_data)
        
        self.ui.disable_alias()
    
    def onUpdate(self):
        pass
    
    def onSelect(self, selected, _type):
        if _type == PlotHoleType.STORY:
            self.selected_story = selected
            self.selected_story_fqname = h.get_path_for_alias(self.base_dir, selected) 
            self.book_path = f"{pathlib.Path(self.selected_story_fqname).parent}/book"     
            self.ui.set_header(f"Neues Buch für: {selected}")
            
    def onDisplay(self, origin):        
        if self.ui == origin:
            self.ui.set_alias("")
            self.ui.set_title("")
            self.ui.set_accent("")
            self.ui.set_message("")
            self.ui.set_basic_idea("")
            self.ui.enable_alias()
            self.fq_file_name = ""
            self.book = None
    
class BookOverviewModel(UIObserver):
    
    def __init__(self, ui, base_dir):
        self.ui = ui
        self.base_dir = base_dir  
        self.selected_story_fqname = ''
        self.book_path = ''
        
        self.ui.register(self)
        
    def __load_aliases__(self):        
        if len(self.book_path) > 0:
            for alias in h.get_all_aliases(self.book_path, extension='book'):
                self.ui.create_book_button(alias)
    
    def onClose(self):
        pass
    
    def onDelete(self):
        pass
    
    def onLoad(self, file_path):
        pass
    
    def onRevert(self):
        pass
    
    def onSave(self):
        pass
    
    def onUpdate(self):
        pass
    
    def onSelect(self, selected, _type):
        if _type == PlotHoleType.STORY:
            self.selected_story = selected
            self.selected_story_fqname = h.get_path_for_alias(self.base_dir, selected) 
            self.book_path = f"{pathlib.Path(self.selected_story_fqname).parent}/book"    
            self.ui.set_header(f"Bücher: {selected}")   
            self.__load_aliases__()
            
    def onDisplay(self, origin):        
        if self.ui == origin:
            self.ui.remove_all_book_buttons()
            self.__load_aliases__()