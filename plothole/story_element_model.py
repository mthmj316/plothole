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
import pathlib

class StoryElementModel(UIObserver):
    
    def __init__(self, ui, overview_ui, base_dir):
        log.log_var(self, currentframe(), ("ui", ui), ("overview_ui", overview_ui), ("base_dir", base_dir))
        self.base_dir = base_dir
        self.ui = ui
        self.overview_ui = overview_ui
        self.ui.register(self)
        self.overview_ui.register(self)
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
        
    @abstractmethod
    def load_previous():
        pass

    @abstractmethod
    def load_next():
        pass
    
    @abstractmethod
    def load_overview():
        pass
        
    def clear(self):
        log.log(self, currentframe())        
        self.this_story_element = None
        self.fq_file_name = ''
        
    def get_file_name(self):
        log.log(super, currentframe())
        file_name = self.get_id(False)
        log.log_var(self, currentframe(),('file_name',file_name))
        return file_name     
    
    def on_close(self):
        log.log(self, currentframe())
        self.clear()
        # close means always that currently the story element ui is visible
        # it is changed to the corresponding overview frame
        # hence reload all story elements
        self.load_overview()
    
    def on_character(self):
        log.log(self, currentframe(), 'not relevant')
    
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
        self.clear()

    def on_next(self):
        log.log(self, currentframe())
        self.load_next()

    @abstractmethod
    def on_open(self, _id, ph_type=None):
        pass

    def on_plothole(self):
        log.log(self, currentframe(), 'not relevant')

    def on_previous(self):
        log.log(self, currentframe())
        self.load_previous()

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
        log.log(self, currentframe(), 'not relevant')

    def on_top(self):
        log.log(self, currentframe())
        self.clear()
        
    def on_update(self):
        log.log(self, currentframe())        
        self.prepare_save()
        data = json.dumps(self.this_story_element)
        fa.write(self.fq_file_name, data)

class BookModel(StoryElementModel):
    
    def __init__(self, ui, overview_ui, base_dir):
        super().__init__(ui, overview_ui, base_dir)
        log.log_var(self, currentframe(), ("ui", ui), ("base_dir", base_dir))
        self.story_fq_path = ''
    
    def on_open(self, _id, ph_type=None):
        log.log_var(self, currentframe(),('_id',_id),('ph_type',ph_type)) 
        
        if ph_type == PlotHoleType.STORY:
            # a story is selected -> get the story path
            self.story_fq_path = hlp.get_story_path_by_alias(self.base_dir, _id)
            log.log_var(self, currentframe(),('story_path',self.story_fq_path))
            # and load all book
            self.load_overview()
            #set the header
            story = hlp.get_story(self.story_fq_path, as_dict=True)  
            self.overview_ui.set_header(f"Bücher von {story.get(sec.TITLE)}")
        elif ph_type == PlotHoleType.BOOK:
            self.this_story_element = hlp.get_story_by_alias(self.get_folder(), _id)
            self.fq_file_name = hlp.get_story_path_by_alias(self.get_folder(), _id)
            self.load()
        else:
            pass #nothing to do   

    def load_overview(self):
        log.log(self, currentframe())
        self.overview_ui.remove_all_overview_items()
        for story in sorted(hlp.get_all_books(self.get_folder(), as_dict=True), key=lambda x: x[sec.SEQUENTIAL_NO]):
            self.overview_ui.add_overview_item(story.get(sec.ALIAS), story.get(sec.TITLE))

    def load_previous(self):
        log.log(self, currentframe())        
        if self.this_story_element is not None:   
            if self.this_story_element.get(sec.SEQUENTIAL_NO) > 1:
                self.load_next_seq(True)
    
    def load_next_seq(self, reverse):
        log.log_var(self, currentframe(), ('reverse',reverse))
        books = sorted(hlp.get_all_boos(self.get_folder(), as_dict=True), key=lambda x: x[sec.SEQUENTIAL_NO], reverse=reverse)
        select_next = False
        for book in books:
            if select_next:
                self.overview_ui.on_item_select(book.get(sec.ALIAS))
                break
            if book.get(sec.SEQUENTIAL_NO) == self.this_story_element.get(sec.SEQUENTIAL_NO):
                select_next = True

    def load_next(self):
        log.log(self, currentframe())
        if self.this_story_element is not None:
            self.load_next_seq(False)

    def clear(self):
        log.log(self, currentframe())
        self.ui.set_sequential_no('')
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
        phtype = PlotHoleType.BOOK
        log.log_var(self, currentframe(), ("phtype", phtype))
        return phtype
    
    def get_folder(self):
        log.log(self, currentframe())
        folder = pathlib.Path(self.story_fq_path).parent 
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
        log.log_var(self, currentframe())
        
        squential_no = self.ui.get_sequential_no()
        alias = self.ui.get_alias()
        title = self.ui.get_title()
        tone = self.ui.get_tone()
        genre = self.ui.get_genre()
        message = self.ui.get_message()
        content = self.ui.get_content()
        
        book = {}
        book[sec.SEQUENTIAL_NO.value] = squential_no.strip()
        book[sec.ALIAS.value] = alias.strip()
        book[sec.TITLE.value] = title.strip()
        book[sec.TONE.value] = tone.strip()
        book[sec.GENRE.value] = genre.strip()
        book[sec.MESSAGE.value] = message.strip()
        book[sec.CONTENT.value] = content.strip()
        
        log.log_var(self, currentframe(), ("book", book))
        
        self.this_story_element = book
        
    def after_save(self):
        log.log(self, currentframe())
        self.ui.disable_alias()
        
        story = hlp.get_story(self.story_path, as_dict=True)        
        self.ui.set_header(f"Buch: {self.this_story_element.get(sec.TITLE)} von {story.get(sec.TITLE)}")
    
    def load(self):
        log.log(self, currentframe())
        book = self.this_story_element
        
        self.ui.set_sequential_no(book.get(sec.SEQUENTIAL_NO))
        self.ui.set_alias(book.get(sec.ALIAS))
        self.ui.set_title(book.get(sec.TITLE))
        self.ui.set_tone(book.get(sec.TONE))
        self.ui.set_genre(book.get(sec.GENRE))
        self.ui.set_message(book.get(sec.MESSAGE))
        self.ui.set_content(book.get(sec.CONTENT))
        
        self.ui.disable_alias()
        
        story = hlp.get_story(self.story_path, as_dict=True)        
        self.ui.set_header(f"Buch: {self.this_story_element.get(sec.TITLE)} von {story.get(sec.TITLE)}")
         
            

class StoryModel(StoryElementModel):
    
    def __init__(self, ui, overview_ui, base_dir):
        super().__init__(ui, overview_ui, base_dir)
        log.log_var(self, currentframe(), ("ui", ui), ("base_dir", base_dir))

    def on_open(self, _id, ph_type=None):
        log.log_var(self, currentframe(),('_id',_id),('ph_type',ph_type))
        
        # if ph_type=None -> load all stories into overview_ui
        # if ph_type=Story -> load story with the given _id (alias) into ui
        # if ph_type neither None nor Story -> do nothing
        if ph_type is None:
            self.load_overview()
        elif ph_type == PlotHoleType.STORY:
            self.this_story_element = hlp.get_story_by_alias(self.get_folder(), _id)
            self.fq_file_name = hlp.get_story_path_by_alias(self.get_folder(), _id)
            self.load()
        else:
            pass #nothing to do

    def load_overview(self):
        log.log(self, currentframe())
        self.overview_ui.remove_all_overview_items()
        for story in sorted(hlp.get_all_stories(self.get_folder(), as_dict=True), key=lambda x: x[sec.TITLE.value]):
            self.overview_ui.add_overview_item(story.get(sec.ALIAS), story.get(sec.TITLE))

    def load_previous(self):
        log.log(self, currentframe(), 'not relevant')
        

    def load_next(self):
        log.log(self, currentframe(), 'not relevant')
    
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
        log.log_var(self, currentframe())
        
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
        self.ui.set_header(f"Geschichte: {self.this_story_element.get(sec.TITLE)}")
        
    def load(self):
        log.log(self, currentframe())
        story = self.this_story_element
        
        self.ui.set_alias(story.get(sec.ALIAS))
        self.ui.set_title(story.get(sec.TITLE))
        self.ui.set_tone(story.get(sec.TONE))
        self.ui.set_genre(story.get(sec.GENRE))
        self.ui.set_message(story.get(sec.MESSAGE))
        self.ui.set_content(story.get(sec.CONTENT))
        
        self.ui.disable_alias()
        
        self.ui.set_header(f"Geschichte: {self.this_story_element.get(sec.TITLE)}")
        