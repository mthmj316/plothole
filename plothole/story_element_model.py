# -*- coding: utf-8 -*-
"""
Created on Tue Jan  6 18:28:58 2026

@author: mthoma
"""
from abc import abstractmethod
from inspect import currentframe
import logger as log
from observers import UIObserver
import plothole_types as pt
import plothole_core as pc
from story_element_ui import __SEControls__ as sec
import helpers as hlp
import json
import file_access as fa
import pathlib
import relation_desolver as rd

class StoryElementModel(UIObserver):
    
    def __init__(self, ui, overview_ui, base_dir, tree_view, parent_model):
        log.log_var(self, currentframe(), ("ui", ui), ("overview_ui", overview_ui), ("base_dir", base_dir), ("parent_model", parent_model))
        self.base_dir = base_dir
        self.ui = ui
        self.overview_ui = overview_ui
        self.ui.register(self)
        self.overview_ui.register(self)
        self.this_story_element = None
        self.tree_view = tree_view
        self.parent_model = parent_model
        self.treeview_selection = None
    
    @abstractmethod
    def get_plothole_type(self):
        '''
        Returns the plothole type for the correspondings story element model.
        -------
        None
        '''
        pass

    def get_id(self, from_ui):
        '''
        Returns either the alias of the current active story element
        or if from_ui == True the value of the ui input field 'Alias'.
        
        None is returned if from_ui == True and there is no active story element.
        '''
        
        log.log_var(self, currentframe(),('from_ui',from_ui))
        _id = ''
        
        if from_ui:
            _id = self.ui.get_alias()
        else:
            
            active_story_element = self.get_active_story_element()
            
            if active_story_element is not None:
                _id = active_story_element.get(sec.ALIAS)
        
        log.log_var(self, currentframe(), ("_id", _id))
        return _id
    
    def get_id_name(self):
        '''
        Returns the name of the id attribute of the story element.
        By default alias is returned.
        '''
        log.log(self, currentframe())
        name = 'Alias'
        log.log_var(self, currentframe(), ("name", name))
        return name
    
    def prepare_save(self):
        '''
        Is called before save and update.
        
        Create a new this_story_element dictionary, fetches the data from the ui, and, if not None,
        writes the ui value to the corresponding entry of the dictionary.
        '''
        log.log_var(self, currentframe())
        
        alias = self.ui.get_alias()
        content = self.ui.get_content()
        genre = self.ui.get_genre() 
        message = self.ui.get_message()
        note = self.ui.get_note()
        sequential_no = self.ui.get_sequential_no()
        title = self.ui.get_title()
        tone = self.ui.get_tone()
        xtension_0 = self.ui.get_xtension(sec.XTENSION_0)
        xtension_1 = self.ui.get_xtension(sec.XTENSION_1)
        xtension_2 = self.ui.get_xtension(sec.XTENSION_2)
        xtension_3 = self.ui.get_xtension(sec.XTENSION_3)
        xtension_4 = self.ui.get_xtension(sec.XTENSION_4)
        xtension_5 = self.ui.get_xtension(sec.XTENSION_5)
        xtension_6 = self.ui.get_xtension(sec.XTENSION_6)
        xtension_7 = self.ui.get_xtension(sec.XTENSION_7)
        xtension_8 = self.ui.get_xtension(sec.XTENSION_8)
        xtension_9 = self.ui.get_xtension(sec.XTENSION_9)        
        
        self.this_story_element= {}
        
        if alias is not None:
            self.this_story_element[sec.ALIAS.value] = alias.strip()
        
        if content is not None:
            self.this_story_element[sec.CONTENT.value] = content.strip()
        
        if genre is not None:
            self.this_story_element[sec.GENRE.value] = genre.strip()
        
        if message is not None:
            self.this_story_element[sec.MESSAGE.value] = message.strip()
        
        if note is not None:
            self.this_story_element[sec.NOTE.value] = note.strip()
        
        if sequential_no is not None:
            self.this_story_element[sec.SEQUENTIAL_NO.value] = sequential_no.strip()
        
        if title is not None:
            self.this_story_element[sec.TITLE.value] = title.strip()
        
        if tone is not None:
            self.this_story_element[sec.TONE.value] = tone.strip()
        
        if xtension_0 is not None:
            self.this_story_element[sec.XTENSION_0.value] = xtension_0.strip()
        
        if xtension_1 is not None:
            self.this_story_element[sec.XTENSION_1.value] = xtension_1.strip()
        
        if xtension_2 is not None:
            self.this_story_element[sec.XTENSION_2.value] = xtension_2.strip()
        
        if xtension_3 is not None:
            self.this_story_element[sec.XTENSION_3.value] = xtension_3.strip()
        
        if xtension_4 is not None:
            self.this_story_element[sec.XTENSION_4.value] = xtension_4.strip()
        
        if xtension_5 is not None:
            self.this_story_element[sec.XTENSION_5.value] = xtension_5.strip()
        
        if xtension_6 is not None:
            self.this_story_element[sec.XTENSION_6.value] = xtension_6.strip()
        
        if xtension_7 is not None:
            self.this_story_element[sec.XTENSION_7.value] = xtension_7.strip()
        
        if xtension_8 is not None:
            self.this_story_element[sec.XTENSION_8.value] = xtension_8.strip()
        
        if xtension_9 is not None:
            self.this_story_element[sec.XTENSION_9.value] = xtension_9.strip()
        
        log.log_var(self, currentframe(), ("this_story_element", self.this_story_element))
    

    def after_save(self):
        '''
        Is called after save and update.
        
        Disables the ui field alias and sets the header by calling the set_header() function.
        '''
        log.log_var(self, currentframe())
        self.ui.disable_alias()        
        self.set_header()
    
    def load(self, element):
        '''
        Loads the data in element dictionary  into the corresponding ui field.
        '''        
        log.log(self, currentframe())
        
        self.ui.set_alias(element.get(sec.ALIAS))
        self.ui.set_content(element.get(sec.CONTENT))
        self.ui.set_genre(element.get(sec.GENRE))
        self.ui.set_message(element.get(sec.MESSAGE))
        self.ui.set_note(element.get(sec.NOTE))
        self.ui.set_sequential_no(element.get(sec.SEQUENTIAL_NO))        
        self.ui.set_title(element.get(sec.TITLE))
        self.ui.set_tone(element.get(sec.TONE))
        self.ui.set_xtension(sec.XTENSION_0, element.get(sec.XTENSION_0))
        self.ui.set_xtension(sec.XTENSION_1, element.get(sec.XTENSION_1))
        self.ui.set_xtension(sec.XTENSION_2, element.get(sec.XTENSION_2))
        self.ui.set_xtension(sec.XTENSION_3, element.get(sec.XTENSION_3))
        self.ui.set_xtension(sec.XTENSION_4, element.get(sec.XTENSION_4))
        self.ui.set_xtension(sec.XTENSION_5, element.get(sec.XTENSION_5))
        self.ui.set_xtension(sec.XTENSION_6, element.get(sec.XTENSION_6))
        self.ui.set_xtension(sec.XTENSION_7, element.get(sec.XTENSION_7))
        self.ui.set_xtension(sec.XTENSION_8, element.get(sec.XTENSION_8))
        self.ui.set_xtension(sec.XTENSION_9, element.get(sec.XTENSION_8))
        
        self.ui.disable_alias()        
        self.set_header()
        

    def load_previous(self):
        '''
        If the squence no is available in the this_story_element object
        and sequence no is > 1 the load_next_seq function with parameter 
        reverse == True.

        Returns
        -------
        None
        '''
        log.log(self, currentframe())        
        if self.this_story_element is not None:   
            if int(self.this_story_element.get(sec.SEQUENTIAL_NO)) > 1:
                self.load_next_seq(True)

    def load_next(self):
        '''
        If the squence no is available in the this_story_element object
        the load_next_seq function with parameter reverse == False.

        Returns
        -------
        None
        '''
        log.log(self, currentframe())
        if self.this_story_element is not None:
            self.load_next_seq(False)
    
    def load_overview(self):
        '''
        Loads the story elements for the currently selceted parent element.

        Returns
        -------
        None
        '''        
        log.log(self, currentframe())
        # delete the current overview content
        self.overview_ui.remove_all_overview_items()
        
        active_parent_element = self.parent_model.get_active_story_element()
        parent_folder = pathlib.Path(active_parent_element.get(sec.PATH)).parent
        
        ptype = pc.CHILD_PLOTHOLE_TYPE.get(active_parent_element.get(sec.PTYPE.value))
        
        elements = hlp.get_all(parent_folder, ptype ,as_dict=True)
        
        for element in sorted(elements, key=lambda x: x[sec.SEQUENTIAL_NO]):
            self.overview_ui.add_overview_item(element.get(sec.PATH), element.get(sec.TITLE))
       
    def clear(self):
        '''
        Clears all input fields.
        '''
        log.log(self, currentframe())
        self.ui.set_alias('')
        self.ui.set_content('')
        self.ui.set_genre('')
        self.ui.set_message('')
        self.ui.set_note('')
        self.ui.set_sequential_no('')        
        self.ui.set_title('')
        self.ui.set_tone('')
        self.ui.set_xtension(sec.XTENSION_0, '')
        self.ui.set_xtension(sec.XTENSION_1, '')
        self.ui.set_xtension(sec.XTENSION_2, '')
        self.ui.set_xtension(sec.XTENSION_3, '')
        self.ui.set_xtension(sec.XTENSION_4, '')
        self.ui.set_xtension(sec.XTENSION_5, '')
        self.ui.set_xtension(sec.XTENSION_6, '')
        self.ui.set_xtension(sec.XTENSION_7, '')
        self.ui.set_xtension(sec.XTENSION_8, '')
        self.ui.set_xtension(sec.XTENSION_9, '')
        self.this_story_element = None
        self.fq_file_name = ''
        self.treeview_selection = None
        
    def get_fq_file_name(self):
        '''
        Returns the fully qualified path of the currently selected story element.

        Returns
        -------
        String
        '''
        log.log(self, currentframe())
        
        active_story_element = self.get_active_story_element()
        fq_file_name = None
        
        if active_story_element is not None:
            fq_file_name = active_story_element.get(sec.PATH)
            
        
        log.log_var(self, currentframe(),('fq_file_name', fq_file_name))
        return fq_file_name
    
    def get_file_name(self):
        '''
        Returns the file name without extension
        of the story element which is about to be saved.
        
        Hint: The file name is actually just the alias of the story element

        Returns
        -------
        TYPE
            DESCRIPTION.
        '''
        log.log(self, currentframe())
        file_name = self.get_id(False)
        log.log_var(self, currentframe(),('file_name',file_name))
        return file_name     
    
    def on_close(self):
        '''
        Close means always that currently the story element ui is visible
        If a treeview selection is displayed the ui is cleared, and, if
        this_story_element is not None the ui is filled with its data.
        If no treeview selection active it will load the overview.
        
        The overview is also loaded if treeview selection is active but 
        this_story_element is None.

        Returns
        -------
        None
        '''
        log.log(super, currentframe())
        self.clear()

        if self.treeview_selection is None:
            self.load_overview()
        else:
            self.treeview_selection = None
            if self.this_story_element is not None:
                self.load(self.this_story_element)
            else:
                self.load_overview()
                
    
    def on_character(self):
        '''
        Not yet needed

        Returns
        -------
        None
        '''
        log.log(self, currentframe(), 'not relevant')
    
    def on_delete(self):
        '''
        Deletes the currently active story elemet.
        Either this_story_element or the treeview_selection is deleted
        
        After deletion the ui is cleared.

        Returns
        -------
        None
        '''
        log.log(self, currentframe())
        
        active_story_element = self.get_active_story_element()
        log.log_var(self, currentframe(), ('active_story_element',active_story_element))
        
        if active_story_element is not None:
           pc.delete_story_element(active_story_element)
           self.tree_view.update_tree_view()
            
        self.clear()

    def on_new(self):
        '''
        Just calls the clear function.

        Returns
        -------
        None
        '''
        log.log(self, currentframe())
        self.clear()

    def on_next(self):
        '''
        Just calls the load_nextfunction 

        Returns
        -------
        None
        '''
        log.log(self, currentframe())
        self.load_next()

    def on_open(self, fq_filename, ph_type=None):
        '''
        Opens the story element for the given fq_filename.       

        Parameters
        ----------
        fq_filename : String
            The fully qualified file name of the story element which must be opened.
        ph_type : PlotHoleType, optional
            Type of the story element which must be opened. (not needed anymore)

        Returns
        -------
        None
        '''
        log.log_var(self, currentframe(),('fq_filename',fq_filename), ('ph_type',ph_type))
        
        self.this_story_element = hlp.get(fq_filename, as_dict=True)
        log.log_var(self, currentframe(),('this_story_element',self.this_story_element))
        
        self.load(self.this_story_element)  
        self.tree_view.

    def on_plothole(self):
        '''
        Not yet implemented.
        '''        
        log.log(self, currentframe(), 'not relevant')

    def on_previous(self):
        '''
        Just calls the load_previous function.

        Returns
        -------
        None
        '''
        log.log(self, currentframe())
        self.load_previous()

    def on_revert(self):
        '''
        Loads the stored data of the currently active story eleement into the ui.
        All unsaved changes will be lost. 

        Returns
        -------
        None
        '''
        log.log(self, currentframe())
        self.load(self.treeview_selection if self.treeview_selection is not None else self.this_story_element)

    def on_save(self):
        log.log(self, currentframe())
        
        if self.this_story_element is not None:
            self.on_update()
            return
            
        _id = self.get_id(True)
        
        if _id == '':
            self.ui.raise_error(f"{self.get_id_name()} muss gesetzt sein.")
            return
        
        if hlp.exists_alias(self.get_overview_folder(), _id):
            self.ui.raise_error(f"{_id} existiert bereits!")
            return
        
        self.prepare_save()
        
        data = json.dumps(self.this_story_element)        
        file_name = "".join(x for x in self.get_file_name() if x.isalnum())
        path = f"{self.get_overview_folder()}/{file_name}"
        self.fq_file_name = f"{path}/{file_name}.{self.get_plothole_type().value}"  
        
        log.log_var(self, currentframe(), ("fq_file_name", self.fq_file_name))

        if not fa.exists(self.fq_file_name):            
            fa.create_dir(path)  
             
        fa.write(self.fq_file_name, data)
        
        self.tree_view.update_tree_view()
        
        self.after_save()
        rd.desolve(self.base_dir)
        
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
        self.tree_view.update_tree_view()
        self.after_save()
        rd.desolve(self.base_dir)
        
    def on_option_select(self, selected, secontrol):
        pass
    
    def on_treeview_select(self, path):
        log.log_var(self, currentframe(), ("path", path))
        self.fq_file_name = path
        element = hlp.get(path, as_dict=True)
        
        self.treeview_selection = element
        
        self.load(element)

    def set_header(self):
        """
        Sets the of the ui user interface.
        The following cases are covered:
            1.: New story element creation:
                This means no this_story_element/treeview_selection is None -> Generic header: e.g. "Neues Buch"
            2.: Story elements is displayed:
                This means get_active_story_element returns the active story element -> specific header: "2. Buch: Die Zwei Türme"
                Template: <squence nr>. <story element ui representation>: <story element title>
                If no sequence nr is avaialable:
                Template: <story element ui representation>: <story element title>
        """        
        log.log_var(self, currentframe())
        
        active_story_element = self.get_active_story_element()
        
        header = ""
        ptype = self.get_plothole_type()
        ptype4ui = pt.PLOTHOLE_TYPE_VALUE_TO_UI_DISPLAY_MAP.get(ptype)
        
        if active_story_element is not None:
            # Create specific header
            
            sequence_no = active_story_element.get(sec.SEQUENTIAL_NO)
            log.log_var(self, currentframe(), ('sequence_no',sequence_no))
            
            sequence_part = ''
            if sequence_no is not None:
                sequence_part = f"{sequence_no}. "
                
            header = f"{sequence_part}{ptype4ui}: {active_story_element.get(sec.TITLE)}"
            
        else:
            # create genric header
            header = f"Neue(s) {ptype4ui}"

        self.ui.set_header(header)

    def get_active_story_element(self):
        """
        Returns the this_story_element object if the treeview_selection is None
        """
        log.log(self, currentframe())
        
        if self.treeview_selection is not None:
            log.log(self, currentframe(), 'treeview_selection is returned')
            return self.treeview_selection
        elif self.this_story_element is not None:
            log.log(self, currentframe(), 'this_story_element is returned')
            return self.this_story_element
        else:
            log.log(self, currentframe(), 'None is returned')
            return None
        

class SceneModel(StoryElementModel):
    
    def __init__(self, ui, overview_ui, base_dir, tree_view, parent_model):
        super().__init__(ui, overview_ui, base_dir, tree_view, parent_model)
        log.log_var(self, currentframe(), ("ui", ui), ("base_dir", base_dir), ("parent_model", parent_model))  
    
    def load_next_seq(self, reverse):
        log.log_var(self, currentframe(), ('reverse',reverse))
        scenes = sorted(hlp.get_all_scenes(self.get_overview_folder(), as_dict=True), key=lambda x: x[sec.SEQUENTIAL_NO], reverse=reverse)
        select_next = False
        for scene in scenes:
            if select_next:
                self.overview_ui.on_item_select(scene.get(sec.ALIAS))
                break
            if scene.get(sec.SEQUENTIAL_NO) == self.this_story_element.get(sec.SEQUENTIAL_NO):
                select_next = True
        
    def get_plothole_type(self):
        log.log(self, currentframe())
        phtype = pt.PlotHoleType.SCENE
        log.log_var(self, currentframe(), ("phtype", phtype))
        return phtype        

    def on_raised(self): 
        log.log(self, currentframe())
                
        selected_parent = self.parent_model.get_fq_file_name()        
        log.log_var(self, currentframe(),('selected_parent', selected_parent))  
        
        chapter = hlp.get(selected_parent, as_dict=True)
        
        self.load_overview()
        self.overview_ui.set_header(f"Szenen von '{chapter.get(sec.TITLE)}'")
        
    def on_treeview_select(self, path):
        log.log_var(self, currentframe(), ("path", path))
        
        if path.endswith('.scene'):
            super().on_treeview_select(path)

class ChapterModel(StoryElementModel):
    
    def __init__(self, ui, overview_ui, base_dir, tree_view, parent_model):
        super().__init__(ui, overview_ui, base_dir, tree_view, parent_model)
        log.log_var(self, currentframe(), ("ui", ui), ("base_dir", base_dir), ("parent_model", parent_model))
    
    def load_next_seq(self, reverse):
        log.log_var(self, currentframe(), ('reverse',reverse))
        chapters = sorted(hlp.get_all_chapters(self.get_overview_folder(), as_dict=True), key=lambda x: x[sec.SEQUENTIAL_NO], reverse=reverse)
        select_next = False
        for chapter in chapters:
            if select_next:
                self.overview_ui.on_item_select(chapter.get(sec.ALIAS))
                break
            if chapter.get(sec.SEQUENTIAL_NO) == self.this_story_element.get(sec.SEQUENTIAL_NO):
                select_next = True
        
    def get_plothole_type(self):
        log.log(self, currentframe())
        phtype = pt.PlotHoleType.CHAPTER
        log.log_var(self, currentframe(), ("phtype", phtype))
        return phtype        

    def on_raised(self): 
        log.log_var(self, currentframe())
        
        selected_parent = self.parent_model.get_fq_file_name()        
        log.log_var(self, currentframe(),('selected_parent', selected_parent))  
        
        part = hlp.get(selected_parent, as_dict=True)
        
        self.load_overview()
        self.overview_ui.set_header(f"Kapitel von '{part.get(sec.TITLE)}'")
        
    def on_treeview_select(self, path):
        log.log_var(self, currentframe(), ("path", path))
        
        if path.endswith('.chapter'):
            super().on_treeview_select(path)

class PlotholeModel(StoryElementModel):
    
    def __init__(self, ui, overview_ui, base_dir, story_model, tree_view):
        super().__init__(ui, overview_ui, base_dir, tree_view, None)
        log.log_var(self, currentframe(), ("ui", ui), ("base_dir", base_dir), ("story_model", story_model))
        self.story_model = story_model
        
    def on_option_select(self, selected, secontrol):
        log.log_var(self, currentframe(), ("selected", selected), ("secontrol", secontrol))        
        if secontrol == sec.SEQUENTIAL_NO:
            self.load_classifications(pt.UI_DISPLAY_TO_PLOTHOLE_TYPE_VALUE_MAP.get(selected))
    
    def load_classifications(self, ph_type_str):
        log.log_var(self, currentframe(), ('ph_type_str',ph_type_str))
        
        ph_type = pt.PlotHoleType(ph_type_str)
        
        titles = []
        selected_item = None
        if ph_type != pt.PlotHoleType.STORY:
            selected_story_path = pathlib.Path(self.story_model.get_fq_file_name()).parent        
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
        self.this_story_element = hlp.get_plothole_by_alias(self.get_overview_folder(), _id)
        self.fq_file_name = hlp.get_plothole_path_by_alias(self.get_overview_folder(), _id)
        self.load()   

    def load_overview(self):
        log.log(self, currentframe())
        self.overview_ui.remove_all_overview_items()
        for plothole in sorted(hlp.get_all_plotholes(self.get_overview_folder(), as_dict=True), key=lambda x: x[sec.TITLE]):
            self.overview_ui.add_overview_item(plothole.get(sec.ALIAS), plothole.get(sec.TITLE))
    
    def load_next_seq(self, reverse):
        log.log_var(self, currentframe(), ('reverse',reverse))
        parts = sorted(hlp.get_all_parts(self.get_overview_folder(), as_dict=True), key=lambda x: x[sec.SEQUENTIAL_NO], reverse=reverse)
        select_next = False
        for part in parts:
            if select_next:
                self.overview_ui.on_item_select(part.get(sec.ALIAS))
                break
            if part.get(sec.SEQUENTIAL_NO) == self.this_story_element.get(sec.SEQUENTIAL_NO):
                select_next = True
        
    def get_plothole_type(self):
        log.log(self, currentframe())
        phtype = pt.PlotHoleType.PLOTHOLE
        log.log_var(self, currentframe(), ("phtype", phtype))
        return phtype
    
    def get_folder(self):
        log.log(self, currentframe())
        story_folder = pathlib.Path(self.story_model.get_fq_file_name()).parent
        folder = f"{story_folder}/plotholes"
        log.log_var(self, currentframe(), ("folder", folder))
        return folder
    
    def prepare_save(self):
        log.log_var(self, currentframe())
        
        classification_level = self.ui.get_sequential_no()
        alias = self.ui.get_alias()
        title = self.ui.get_title()
        classification = self.get_classification_alias()
        message = self.ui.get_message()
        content = self.ui.get_content()
        
        plothole = {}
        plothole[sec.SEQUENTIAL_NO.value] = pt.DISPLAY_TO_PLOTHOLE_TYPE_VALUE_MAP.get(classification_level.strip())
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
            selected_story = self.story_model.get_fq_file_name()
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
        
        self.load_classifications(pt.PlotHoleType.STORY.value)
        plothole = self.this_story_element
        
        # selected 'Betrifft' 
        classification_type = plothole.get(sec.SEQUENTIAL_NO)
        log.log_var(self, currentframe(), ('classification_type',classification_type))        
        self.ui.set_sequential_no(pt.PLOTHOLE_TYPE_VALUE_TO_UI_DISPLAY_MAP.get(classification_type))
        
        self.ui.set_alias(plothole.get(sec.ALIAS))
        self.ui.set_title(plothole.get(sec.TITLE))
        
        if pt.PlotHoleType(plothole.get(sec.SEQUENTIAL_NO)) != pt.PlotHoleType.STORY:
            classification_object = hlp.get_by_alias(
                plothole.get(sec.GENRE), 
                plothole.get(sec.SEQUENTIAL_NO),
                pt.PlotHoleType.PLOTHOLE)
            
            classification = self.create_classification_optmenu_entry(classification_object)
            
            # get for the selected 'Betrifft' the corresponding choises
            story_path = pathlib.Path(self.story_model.get_fq_file_name()).parent
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
        story = hlp.get_book(self.story_model.get_fq_file_name(), as_dict=True)       
        self.ui.set_header(f"Neues Plothole für '{story.get(sec.TITLE)}'")           

    def on_raised(self): 
        log.log(self, currentframe())
        self.load_overview()
        story = hlp.get_book(self.story_model.get_fq_file_name(), as_dict=True)  
        self.overview_ui.set_header(f"Plotholes von '{story.get(sec.TITLE)}'")
        
    def on_treeview_select(self, path):
        log.log_var(self, currentframe(), ("path", path))
        pass

class PartModel(StoryElementModel):
    
    def __init__(self, ui, overview_ui, base_dir, tree_view, parent_model):
        super().__init__(ui, overview_ui, base_dir, tree_view, parent_model)
        log.log_var(self, currentframe(), ("ui", ui), ("base_dir", base_dir), ("parent_model", parent_model))
    
    def load_next_seq(self, reverse):
        log.log_var(self, currentframe(), ('reverse',reverse))
        parts = sorted(hlp.get_all_parts(self.get_overview_folder(), as_dict=True), key=lambda x: x[sec.SEQUENTIAL_NO], reverse=reverse)
        select_next = False
        for part in parts:
            if select_next:
                self.overview_ui.on_item_select(part.get(sec.ALIAS))
                break
            if part.get(sec.SEQUENTIAL_NO) == self.this_story_element.get(sec.SEQUENTIAL_NO):
                select_next = True
        
    def get_plothole_type(self):
        log.log(self, currentframe())
        phtype = pt.PlotHoleType.PART
        log.log_var(self, currentframe(), ("phtype", phtype))
        return phtype

    def on_raised(self): 
        log.log_var(self, currentframe())
        
        selected_parent = self.parent_model.get_fq_file_name()        
        log.log_var(self, currentframe(),('selected_parent', selected_parent))  
        
        book = hlp.get(selected_parent, as_dict=True)
        
        self.load_overview()
        self.overview_ui.set_header(f"Teile von '{book.get(sec.TITLE)}'")
        
    def on_treeview_select(self, path):
        log.log_var(self, currentframe(), ("path", path))
        
        if path.endswith('.part'):
            super().on_treeview_select(path)

class BookModel(StoryElementModel):
    
    def __init__(self, ui, overview_ui, base_dir, tree_view, parent_model):
        super().__init__(ui, overview_ui, base_dir, tree_view, parent_model)
        log.log_var(self, currentframe(), ("ui", ui), ("base_dir", base_dir), ("parent_model", parent_model))
    
    def load_next_seq(self, reverse):
        log.log_var(self, currentframe(), ('reverse',reverse))
        books = sorted(hlp.get_all_books(self.get_overview_folder(), as_dict=True), key=lambda x: x[sec.SEQUENTIAL_NO], reverse=reverse)
        select_next = False
        for book in books:
            if select_next:
                self.overview_ui.on_item_select(book.get(sec.ALIAS))
                break
            if book.get(sec.SEQUENTIAL_NO) == self.this_story_element.get(sec.SEQUENTIAL_NO):
                select_next = True
        
    def get_plothole_type(self):
        log.log(self, currentframe())
        phtype = pt.PlotHoleType.BOOK
        log.log_var(self, currentframe(), ("phtype", phtype))
        return phtype
  
    def get_book_header(self):
        log.log(self, currentframe())
    
    def on_raised(self): 
        log.log_var(self, currentframe())
        
        selected_parent = self.parent_model.get_fq_file_name()        
        log.log_var(self, currentframe(),('selected_parent', selected_parent))    
        
        story = hlp.get(selected_parent, as_dict=True)
        
        self.load_overview()
        self.overview_ui.set_header(f"Bücher von '{story.get(sec.TITLE)}'")
        
    def on_treeview_select(self, path):
        log.log_var(self, currentframe(), ("path", path))
        
        if path.endswith('.book'):
            super().on_treeview_select(path)

class StoryModel(StoryElementModel):
    
    def __init__(self, ui, overview_ui, base_dir, tree_view, parent_model):
        super().__init__(ui, overview_ui, base_dir, tree_view, parent_model)
        log.log_var(self, currentframe(), ("ui", ui), ("base_dir", base_dir), ("parent_model", parent_model))

    # def on_open(self, _id):
    #     log.log_var(self, currentframe(),('_id',_id))
    #     self.fq_file_name = hlp.get_story_path_by_alias(self.get_overview_folder(), _id)
    #     log.log_var(self, currentframe(),('fq_file_name',self.fq_file_name))
        
    #     self.this_story_element = hlp.get_story_by_alias(self.get_ui_folder(), _id)
    #     log.log_var(self, currentframe(),('this_story_element',self.this_story_element))
        
    #     self.load()       

    def load_overview(self):
        log.log(self, currentframe())
        self.overview_ui.remove_all_overview_items()
        for story in sorted(hlp.get_all_stories(self.get_overview_folder(), as_dict=True), key=lambda x: x[sec.TITLE.value]):
            self.overview_ui.add_overview_item(story.get(sec.PATH), story.get(sec.TITLE))

    def load_previous(self):
        log.log(self, currentframe())
        # is not used for stories
        

    def load_next(self):
        log.log(self, currentframe())
        # is not used for stories
    
    def get_plothole_type(self):
        log.log(self, currentframe())
        phtype = pt.PlotHoleType.STORY
        log.log_var(self, currentframe(), ("phtype", phtype))
        return phtype
        
    def on_raised(self): 
        log.log_var(self, currentframe())
        self.load_overview()
        
    def on_treeview_select(self, path):
        log.log_var(self, currentframe(), ("path", path))
        if path.endswith('.story'):
            super().on_treeview_select(path)   
            
    def get_overview_folder(self):
        log.log(self, currentframe())
        folder = self.base_dir
        log.log_var(self, currentframe(), ("folder", folder))
        return folder