# -*- coding: utf-8 -*-
"""
Created on Tue Jan  6 18:28:58 2026

@author: mthoma
"""
from abc import abstractmethod
from inspect import currentframe
import logger as log
from observers import UIObserver
from plothole_types import PlotHoleType, UI_DISPLAY_TO_PLOTHOLE_TYPE_VALUE_MAP, PLOTHOLE_TYPE_VALUE_TO_UI_DISPLAY_MAP
import plothole_core as pc
from story_element_ui import __SEControls__ as sec
import helpers as hlp
import json
import file_access as fa
import pathlib
from plothole_core import SELECTED_SE

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
    def load(self):
        pass
        
    @abstractmethod
    def load_previous(self):
        pass

    @abstractmethod
    def load_next(self):
        pass
    
    @abstractmethod
    def load_overview(self):
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
        
        SELECTED_SE.select(self.get_plothole_type(), self.fq_file_name)

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
        self.after_save()
        
    def on_option_select(self, selected, secontrol):
        pass

class ChapterModel(StoryElementModel):
    
    def __init__(self, ui, overview_ui, base_dir):
        super().__init__(ui, overview_ui, base_dir)
        log.log_var(self, currentframe(), ("ui", ui), ("base_dir", base_dir))
        
    def on_open(self, _id):
        log.log_var(self, currentframe(),('_id',_id)) 
        self.this_story_element = hlp.get_chapter_by_alias(self.get_folder(), _id)
        self.fq_file_name = hlp.get_chapter_path_by_alias(self.get_folder(), _id)
        SELECTED_SE.select(PlotHoleType.PLOTHOLE, self.fq_file_name)  
        self.load()   

    def load_overview(self):
        log.log(self, currentframe())
        self.overview_ui.remove_all_overview_items()
        for chapter in sorted(hlp.get_all_chapters(self.get_folder(), as_dict=True), key=lambda x: x[sec.SEQUENTIAL_NO]):
            self.overview_ui.add_overview_item(chapter.get(sec.ALIAS), chapter.get(sec.TITLE))

    def load_previous(self):
        log.log(self, currentframe())        
        if self.this_story_element is not None:   
            if int(self.this_story_element.get(sec.SEQUENTIAL_NO)) > 1:
                self.load_next_seq(True)
    
    def load_next_seq(self, reverse):
        log.log_var(self, currentframe(), ('reverse',reverse))
        chapters = sorted(hlp.get_all_chapter(self.get_folder(), as_dict=True), key=lambda x: x[sec.SEQUENTIAL_NO], reverse=reverse)
        select_next = False
        for chapter in chapters:
            if select_next:
                self.overview_ui.on_item_select(chapter.get(sec.ALIAS))
                break
            if chapter.get(sec.SEQUENTIAL_NO) == self.this_story_element.get(sec.SEQUENTIAL_NO):
                select_next = True

    def load_next(self):
        log.log(self, currentframe())
        if self.this_story_element is not None:
            self.load_next_seq(False)

    def clear(self):
        log.log(self, currentframe())
        self.ui.set_sequential_no('1')
        self.ui.set_alias('')
        self.ui.set_title('')
        self.ui.set_content('')
        self.ui.enable_alias()
        super().clear()
        
    def get_plothole_type(self):
        log.log(self, currentframe())
        phtype = PlotHoleType.CHAPTER
        log.log_var(self, currentframe(), ("phtype", phtype))
        return phtype
    
    def get_folder(self):
        log.log(self, currentframe())
        folder = SELECTED_SE.get_selected_base(PlotHoleType.PART)
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
        
        sequential_no = self.ui.get_sequential_no()
        alias = self.ui.get_alias()
        title = self.ui.get_title()
        content = self.ui.get_content()
        
        chapter= {}
        chapter[sec.SEQUENTIAL_NO.value] = sequential_no.strip()
        chapter[sec.ALIAS.value] = alias.strip()
        chapter[sec.TITLE.value] = title.strip()
        chapter[sec.CONTENT.value] = content.strip()
        
        log.log_var(self, currentframe(), ("chapter", chapter))
        
        self.this_story_element = chapter
    
    def after_save(self):
        log.log(self, currentframe())
        self.ui.disable_alias()
        
        self.get_chapter_header()
    
    def load(self):
        log.log(self, currentframe())
        
        chapter = self.this_story_element
        self.ui.set_sequential_no(chapter.get(sec.SEQUENTIAL_NO))        
        self.ui.set_alias(chapter.get(sec.ALIAS))
        self.ui.set_title(chapter.get(sec.TITLE))
        self.ui.set_content(chapter.get(sec.CONTENT))
        
        self.ui.disable_alias()
        
        self.get_chapter_header()
        
    def get_chapter_header(self):
        log.log(self, currentframe())        
        part = hlp.get_book(SELECTED_SE.get_select(PlotHoleType.PART), as_dict=True)        
        self.ui.set_header(f"{part.get(sec.TITLE)} Kapitel: {self.this_story_element.get(sec.TITLE)} ({self.this_story_element.get(sec.SEQUENTIAL_NO)})")
  
         
    def on_new(self):
        log.log(self, currentframe())
        self.clear()
        story = hlp.get_book(SELECTED_SE.get_select(PlotHoleType.STORY), as_dict=True)       
        self.ui.set_header(f"Neues Kapitel für '{story.get(sec.TITLE)}'")           

    def on_raised(self): 
        log.log(self, currentframe())
        self.load_overview()
        story = hlp.get_book(SELECTED_SE.get_select(PlotHoleType.STORY), as_dict=True)  
        self.overview_ui.set_header(f"Kapitel von '{story.get(sec.TITLE)}'")


class PlotholeModel(StoryElementModel):
    
    def __init__(self, ui, overview_ui, base_dir):
        super().__init__(ui, overview_ui, base_dir)
        log.log_var(self, currentframe(), ("ui", ui), ("base_dir", base_dir))
        
    def on_option_select(self, selected, secontrol):
        log.log_var(self, currentframe(), ("selected", selected), ("secontrol", secontrol))        
        if secontrol == sec.SEQUENTIAL_NO:
            self.load_classifications(UI_DISPLAY_TO_PLOTHOLE_TYPE_VALUE_MAP.get(selected))
    
    def load_classifications(self, ph_type_str):
        log.log_var(self, currentframe(), ('ph_type_str',ph_type_str))
        
        ph_type = PlotHoleType(ph_type_str)
        
        titles = []
        selected_item = None
        if ph_type != PlotHoleType.STORY:
            selected_story_path = SELECTED_SE.get_selected_base(PlotHoleType.STORY)        
            se_items = hlp.get_all(selected_story_path, ph_type.value, as_dict=True)

            for item in sorted(se_items, key=lambda x: x[sec.TITLE]):
                titles.append(self.create_classification_optmenu_entry(item))
            selected_item = 0
        self.ui.set_options(titles, selected_item, sec.GENRE)
    
    def create_classification_optmenu_entry(self, item):
        log.log_var(self, currentframe(),('item',item))
        entry = f"{item.get(sec.TITLE)} [{item.get(sec.ALIAS)}]"
        log.log_var(self, currentframe(),('entry',entry))
        return entry
        
    def on_open(self, _id):
        log.log_var(self, currentframe(),('_id',_id)) 
        self.this_story_element = hlp.get_plothole_by_alias(self.get_folder(), _id)
        self.fq_file_name = hlp.get_plothole_path_by_alias(self.get_folder(), _id)
        SELECTED_SE.select(PlotHoleType.PLOTHOLE, self.fq_file_name)  
        self.load()   

    def load_overview(self):
        log.log(self, currentframe())
        self.overview_ui.remove_all_overview_items()
        for plothole in sorted(hlp.get_all_plotholes(self.get_folder(), as_dict=True), key=lambda x: x[sec.TITLE]):
            self.overview_ui.add_overview_item(plothole.get(sec.ALIAS), plothole.get(sec.TITLE))

    def load_previous(self):
        log.log(self, currentframe())        
        if self.this_story_element is not None:   
            if int(self.this_story_element.get(sec.SEQUENTIAL_NO)) > 1:
                self.load_next_seq(True)
    
    def load_next_seq(self, reverse):
        log.log_var(self, currentframe(), ('reverse',reverse))
        parts = sorted(hlp.get_all_parts(self.get_folder(), as_dict=True), key=lambda x: x[sec.SEQUENTIAL_NO], reverse=reverse)
        select_next = False
        for part in parts:
            if select_next:
                self.overview_ui.on_item_select(part.get(sec.ALIAS))
                break
            if part.get(sec.SEQUENTIAL_NO) == self.this_story_element.get(sec.SEQUENTIAL_NO):
                select_next = True

    def load_next(self):
        log.log(self, currentframe())
        if self.this_story_element is not None:
            self.load_next_seq(False)

    def clear(self):
        log.log(self, currentframe())
        self.ui.set_sequential_no('Geschichte')
        self.ui.set_alias('')
        self.ui.set_title('')
        self.load_classifications(PlotHoleType.STORY.value)
        self.ui.set_message('')
        self.ui.set_content('')
        self.ui.enable_alias()
        super().clear()
        
    def get_plothole_type(self):
        log.log(self, currentframe())
        phtype = PlotHoleType.PLOTHOLE
        log.log_var(self, currentframe(), ("phtype", phtype))
        return phtype
    
    def get_folder(self):
        log.log(self, currentframe())
        # folder == parent folder of the part -> book folder
        folder = f"{SELECTED_SE.get_selected_base(PlotHoleType.STORY)}/plotholes"
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
        
        classification_level = self.ui.get_sequential_no()
        alias = self.ui.get_alias()
        title = self.ui.get_title()
        classification = self.get_classification_alias()
        message = self.ui.get_message()
        content = self.ui.get_content()
        
        plothole = {}
        plothole[sec.SEQUENTIAL_NO.value] = UI_DISPLAY_TO_PLOTHOLE_TYPE_VALUE_MAP.get(classification_level.strip())
        plothole[sec.ALIAS.value] = alias.strip()
        plothole[sec.TITLE.value] = title.strip()
        plothole[sec.GENRE.value] = classification.strip()
        plothole[sec.MESSAGE.value] = message.strip()
        plothole[sec.CONTENT.value] = content.strip()
        
        log.log_var(self, currentframe(), ("plothole", plothole))
        
        self.this_story_element = plothole
    
    def get_classification_alias(self):
        log.log_var(self, currentframe())
        classification_level = self.ui.get_sequential_no()
        classification_alias = None
        
        if classification_level == 'Geschichte':
            selected_story = SELECTED_SE.get_select(PlotHoleType.STORY)
            classification_alias = hlp.get_story(selected_story, as_dict=True).get(sec.ALIAS)
        else:
            classification_alias = self.extract_alias()
        
        log.log_var(self, currentframe(),('classification_alias',classification_alias))
        return classification_alias
    
    def extract_alias(self):
        log.log(self, currentframe())
        
        selected_classification = self.ui.get_genre()
        sub_strs = selected_classification.split('[')
        
        alias = [p.split(']')[0] for p in sub_strs if ']' in p][0]
        log.log_var(self, currentframe(),('alias',alias))
        return alias
        
        
    def after_save(self):
        log.log(self, currentframe())
        self.ui.disable_alias()
        
        # self.get_part_header()
    
    def load(self):
        log.log(self, currentframe())
        
        self.load_classifications(PlotHoleType.STORY.value)
        plothole = self.this_story_element
        
        # selected 'Betrifft' 
        classification_type = plothole.get(sec.SEQUENTIAL_NO)
        log.log_var(self, currentframe(), ('classification_type',classification_type))        
        self.ui.set_sequential_no(PLOTHOLE_TYPE_VALUE_TO_UI_DISPLAY_MAP.get(classification_type))
        
        self.ui.set_alias(plothole.get(sec.ALIAS))
        self.ui.set_title(plothole.get(sec.TITLE))
        
        if PlotHoleType(plothole.get(sec.SEQUENTIAL_NO)) != PlotHoleType.STORY:
            classification_object = hlp.get_by_alias(
                SELECTED_SE.get_selected_base(PlotHoleType.STORY), 
                plothole.get(sec.GENRE), 
                plothole.get(sec.SEQUENTIAL_NO))
            
            classification = self.create_classification_optmenu_entry(classification_object)
            
            # get for the selected 'Betrifft' the corresponding choises
            story_path = SELECTED_SE.get_selected_base(PlotHoleType.STORY)
            log.log_var(self, currentframe(), ('story_path',story_path))
            classification_choises = hlp.get_all(story_path, classification_type, as_dict=True)
            
            titles = []
            for choise in sorted(classification_choises, key=lambda x: x[sec.TITLE]):
                titles.append(self.create_classification_optmenu_entry(choise))
            selected_item = 0
            self.ui.set_options(titles, selected_item, sec.GENRE)
            self.ui.set_genre(classification)
        
        
        self.ui.set_message(plothole.get(sec.MESSAGE))
        self.ui.set_content(plothole.get(sec.CONTENT))
        
        self.ui.disable_alias()
        
        # self.get_part_header()
         
    def on_new(self):
        log.log(self, currentframe())
        self.clear()
        story = hlp.get_book(SELECTED_SE.get_select(PlotHoleType.STORY), as_dict=True)       
        self.ui.set_header(f"Neues Plothole für '{story.get(sec.TITLE)}'")           

    def on_raised(self): 
        log.log(self, currentframe())
        self.load_overview()
        story = hlp.get_book(SELECTED_SE.get_select(PlotHoleType.STORY), as_dict=True)  
        self.overview_ui.set_header(f"Plotholes von '{story.get(sec.TITLE)}'")

class PartModel(StoryElementModel):
    
    def __init__(self, ui, overview_ui, base_dir):
        super().__init__(ui, overview_ui, base_dir)
        log.log_var(self, currentframe(), ("ui", ui), ("base_dir", base_dir))
    
    def on_open(self, _id):
        log.log_var(self, currentframe(),('_id',_id)) 
        self.this_story_element = hlp.get_part_by_alias(self.get_folder(), _id)
        self.fq_file_name = hlp.get_part_path_by_alias(self.get_folder(), _id)
        SELECTED_SE.select(PlotHoleType.PART, self.fq_file_name)  
        self.load()   

    def load_overview(self):
        log.log(self, currentframe())
        self.overview_ui.remove_all_overview_items()
        for part in sorted(hlp.get_all_parts(self.get_folder(), as_dict=True), key=lambda x: x[sec.SEQUENTIAL_NO]):
            self.overview_ui.add_overview_item(part.get(sec.ALIAS), part.get(sec.TITLE))

    def load_previous(self):
        log.log(self, currentframe())        
        if self.this_story_element is not None:   
            if int(self.this_story_element.get(sec.SEQUENTIAL_NO)) > 1:
                self.load_next_seq(True)
    
    def load_next_seq(self, reverse):
        log.log_var(self, currentframe(), ('reverse',reverse))
        parts = sorted(hlp.get_all_parts(self.get_folder(), as_dict=True), key=lambda x: x[sec.SEQUENTIAL_NO], reverse=reverse)
        select_next = False
        for part in parts:
            if select_next:
                self.overview_ui.on_item_select(part.get(sec.ALIAS))
                break
            if part.get(sec.SEQUENTIAL_NO) == self.this_story_element.get(sec.SEQUENTIAL_NO):
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
        phtype = PlotHoleType.PART
        log.log_var(self, currentframe(), ("phtype", phtype))
        return phtype
    
    def get_folder(self):
        log.log(self, currentframe())
        # folder == parent folder of the part -> book folder
        folder = pathlib.Path(SELECTED_SE.get_select(PlotHoleType.BOOK)).parent 
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
        
        part = {}
        part[sec.SEQUENTIAL_NO.value] = squential_no.strip()
        part[sec.ALIAS.value] = alias.strip()
        part[sec.TITLE.value] = title.strip()
        part[sec.TONE.value] = tone.strip()
        part[sec.GENRE.value] = genre.strip()
        part[sec.MESSAGE.value] = message.strip()
        part[sec.CONTENT.value] = content.strip()
        
        log.log_var(self, currentframe(), ("part", part))
        
        self.this_story_element = part
        
    def after_save(self):
        log.log(self, currentframe())
        self.ui.disable_alias()
        
        self.get_part_header()
    
    def load(self):
        log.log(self, currentframe())
        part = self.this_story_element
        
        self.ui.set_sequential_no(part.get(sec.SEQUENTIAL_NO))
        self.ui.set_alias(part.get(sec.ALIAS))
        self.ui.set_title(part.get(sec.TITLE))
        self.ui.set_tone(part.get(sec.TONE))
        self.ui.set_genre(part.get(sec.GENRE))
        self.ui.set_message(part.get(sec.MESSAGE))
        self.ui.set_content(part.get(sec.CONTENT))
        
        self.ui.disable_alias()
        
        self.get_part_header()
  
    def get_part_header(self):
        log.log(self, currentframe())        
        book = hlp.get_book(SELECTED_SE.get_select(PlotHoleType.BOOK), as_dict=True)        
        self.ui.set_header(f"Buch: {book.get(sec.TITLE)} {self.this_story_element.get(sec.SEQUENTIAL_NO)}. Teil: {self.this_story_element.get(sec.TITLE)}")
         
    def on_new(self):
        log.log(self, currentframe())
        self.clear()
        book = hlp.get_book(SELECTED_SE.get_select(PlotHoleType.BOOK), as_dict=True)       
        self.ui.set_header(f"Neuer Teil für '{book.get(sec.TITLE)}'")           

    def on_raised(self): 
        log.log_var(self, currentframe())
        self.load_overview()
        book = hlp.get_book(SELECTED_SE.get_select(PlotHoleType.BOOK), as_dict=True)  
        self.overview_ui.set_header(f"Teile von '{book.get(sec.TITLE)}'")

class BookModel(StoryElementModel):
    
    def __init__(self, ui, overview_ui, base_dir):
        super().__init__(ui, overview_ui, base_dir)
        log.log_var(self, currentframe(), ("ui", ui), ("base_dir", base_dir))
    
    def on_open(self, _id):
        log.log_var(self, currentframe(),('_id',_id))         
        self.this_story_element = hlp.get_book_by_alias(self.get_folder(), _id)
        self.fq_file_name = hlp.get_book_path_by_alias(self.get_folder(), _id)
        SELECTED_SE.select(PlotHoleType.BOOK, self.fq_file_name)  
        self.load()  

    def load_overview(self):
        log.log(self, currentframe())
        self.overview_ui.remove_all_overview_items()
        for book in sorted(hlp.get_all_books(self.get_folder(), as_dict=True), key=lambda x: x[sec.SEQUENTIAL_NO]):
            self.overview_ui.add_overview_item(book.get(sec.ALIAS), book.get(sec.TITLE))

    def load_previous(self):
        log.log(self, currentframe())        
        if self.this_story_element is not None:   
            if int(self.this_story_element.get(sec.SEQUENTIAL_NO)) > 1:
                self.load_next_seq(True)
    
    def load_next_seq(self, reverse):
        log.log_var(self, currentframe(), ('reverse',reverse))
        books = sorted(hlp.get_all_books(self.get_folder(), as_dict=True), key=lambda x: x[sec.SEQUENTIAL_NO], reverse=reverse)
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
        folder = pathlib.Path(SELECTED_SE.get_select(PlotHoleType.STORY)).parent 
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
        
        self.get_book_header()
    
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
        
        self.get_book_header()
  
    def get_book_header(self):
        log.log(self, currentframe())        
        story = hlp.get_story(SELECTED_SE.get_select(PlotHoleType.STORY), as_dict=True)        
        self.ui.set_header(f"{story.get(sec.TITLE)} {self.this_story_element.get(sec.SEQUENTIAL_NO)}. Buch: {self.this_story_element.get(sec.TITLE)}")
         
    def on_new(self):
        log.log(self, currentframe())
        self.clear()
        story = hlp.get_story(SELECTED_SE.get_select(PlotHoleType.STORY), as_dict=True)        
        self.ui.set_header(f"Neues Buch für '{story.get(sec.TITLE)}'")
    
    def on_raised(self): 
        log.log_var(self, currentframe())
        self.load_overview()
        story = hlp.get_story(SELECTED_SE.get_select(PlotHoleType.STORY), as_dict=True)  
        self.overview_ui.set_header(f"Bücher von '{story.get(sec.TITLE)}'")

class StoryModel(StoryElementModel):
    
    def __init__(self, ui, overview_ui, base_dir):
        super().__init__(ui, overview_ui, base_dir)
        log.log_var(self, currentframe(), ("ui", ui), ("base_dir", base_dir))

    def on_open(self, _id):
        log.log_var(self, currentframe(),('_id',_id))
        self.this_story_element = hlp.get_story_by_alias(self.get_folder(), _id)
        self.fq_file_name = hlp.get_story_path_by_alias(self.get_folder(), _id)
        SELECTED_SE.select(PlotHoleType.STORY, self.fq_file_name)
        self.load()       

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
        SELECTED_SE.select(PlotHoleType.STORY, self.fq_file_name)
    
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
        
    def on_raised(self): 
        log.log_var(self, currentframe())
        self.load_overview()
        SELECTED_SE.select(PlotHoleType.STORY, self.fq_file_name)