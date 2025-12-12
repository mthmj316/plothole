# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 14:40:56 2025

@author: mthoma
"""
import json
from observers import UIObserver
import file_access as fs
import os.path


class StoryModel(UIObserver):
    
    def __init__(self, ui, base_dir):
        
        self.base_dir = base_dir
        self.ui = ui
        self.ui.set_base_dir(base_dir)
        self.ui.register(self)
        self.fq_file_name = ""
     
    
    def onSave(self):
        
        alias = self.ui.get_alias()       

        if alias == "":
            self.ui.raise_error("Alias muss gesetzt sein!")
            return
        
        
        title = self.ui.get_title()
        accent = self.ui.get_accent()
        message = self.ui.get_message()
        basic_idea = self.ui.get_basic_idea()
        
        story_data_temp = {}        
        story_data_temp["alias"] = alias
        story_data_temp["title"] = title
        story_data_temp["accent"] = accent
        story_data_temp["message"] = message
        story_data_temp["basic_idea"] = basic_idea
        
        story_data = json.dumps(story_data_temp) 
        
        file_name = "".join(x for x in alias if x.isalnum())
                
        story_path = f"{self.base_dir}/{file_name}"
        self.fq_file_name = f"{story_path}/{file_name}.story"
        
        if not fs.exists(self.fq_file_name):            
            fs.create_dir(story_path)  
            
        fs.write(self.fq_file_name, story_data)
        
    
    def onDelete(self):        
        if len(self.fq_file_name) > 0:            
            dirname = os.path.dirname(self.fq_file_name)            
            fs.delete_folder(dirname)
            self.onClose()
        
    
    def onUpdate(self):
        # Not relevant
        pass
    
    def onLoad(self, file_name):
        
        if file_name is not None and len(file_name) > 0:
            self.fq_file_name = file_name
            
            data = json.loads(fs.read_from_file(self.fq_file_name, as_list=False))
            
            self.ui.set_alias(data.get('alias'))
            self.ui.set_title(data.get('title'))
            self.ui.set_accent(data.get('accent'))
            self.ui.set_message(data.get('message'))
            self.ui.set_basic_idea(data.get('basic_idea'))
    
    def onRevert(self):
        
        if len(self.fq_file_name) > 0:            
            self.onLoad(self.fq_file_name)
        else:
            self.onClose()
    
    def onClose(self):
        self.ui.set_alias("")
        self.ui.set_title("")
        self.ui.set_accent("")
        self.ui.set_message("")
        self.ui.set_basic_idea("")
        self.fq_file_name = ""