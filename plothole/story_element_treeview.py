# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 10:35:18 2026

@author: mthoma
"""

import helpers as hlp
from tkinter import ttk
from inspect import currentframe
import logger as log
from story_element_ui import __SEControls__ as sec
import pathlib
from observers import UIObservable

import plothole_types as ptypes
import plothole_core as ptcore

class StoryElementTreeview(UIObservable):
    
    def __init__(self, path_repros, tree_container):
        
        self.path_repros = path_repros
        self.tree_container = tree_container
        self.observers = []
        self.last_element_id = '<start>'
        
        self.treeview = self.create_tree_view(self.tree_container)
        self.treeview.bind('<<TreeviewSelect>>', self.on_select)
        self.treeview.bind('<Double-1>', self.on_double_click)
        self.navi = None

    def navigator(self, navi):
        log.log_var(self, currentframe(), ("navi", navi))
        self.navi = navi
        
        
    def register(self, uiobserver):
        log.log_var(self, currentframe(), ("uiobserver", uiobserver))
        self.observers.append(uiobserver)
        
    def unregister(self, uiobserver):
        log.log_var(self, currentframe(), ("uiobserver", uiobserver))
        self.observers.pop(self.observers.index(uiobserver))
        
    def on_double_click(self, event):
        log.log_var(self, currentframe(), ("event", event))
        selection = self.treeview.focus()
        
        log.log_var(self, currentframe(), ("selection", selection))
        
        for observer in self.observers:
            observer.on_treeview_select(selection)
        self.navigate(selection)    
        
     
    def navigate(self, selection):
        log.log_var(self, currentframe(), ("selection", selection))
        
        ptype = ptcore.get_ptype_for_path(selection)
        log.log_var(self, currentframe(), ("selection", selection))
        
        self.navi.on_tree_select(ptype)
     
    def on_select(self, event):
        log.log_var(self, currentframe(), ("event", event))
        
        selection = self.treeview.selection()
        log.log_var(self, currentframe(), ("selection", selection))

    
    def append_children(self, tree, parent_ui, parent_path, parent_ptype):
        
        child_ptype = ptypes.CHILD_PLOTHOLE_TYPE.get(parent_ptype)
        
        if child_ptype is not None:        
            for element in sorted(hlp.get_all(parent_path, child_ptype, as_dict=True), key=lambda x: x[sec.SEQUENTIAL_NO.value]):
                
                path = hlp.get_path_for_alias(parent_path, element.get(sec.ALIAS), child_ptype)
                ptype_display = ptypes.PLOTHOLE_TYPE_VALUE_TO_UI_DISPLAY_MAP.get(child_ptype)
                
                tree_view_ui = tree.insert(parent_ui, "end", text=element.get(sec.TITLE), values=(ptype_display), iid=path)
                
                folder = pathlib.Path(path).parent
                
                self.append_children(tree, tree_view_ui, folder, ptypes.PlotHoleType(child_ptype))
                
    
    def create_tree_view(self, tree_container):
        
        tree = ttk.Treeview(tree_container)
        
        # Spalten definieren
        tree["columns"] = ("Type")
        
        # Erste Spalte (#0) = Baumspalte
        tree.heading("#0", text="Element")
        tree.column("#0", width=150)
        
        # Weitere Spalten
        tree.heading("Type", text="Type")
        tree.column("Type", width=80)

        tree.pack(fill='both', expand=True)
        
        for story in sorted(hlp.get_all_stories(self.path_repros, as_dict=True), key=lambda x: x[sec.TITLE.value]):
            
            log.log_var(self, currentframe(), ("story", story))
            
            path = hlp.get_story_path_by_alias(self.path_repros, story.get(sec.ALIAS))
            ptype = ptcore.get_ptype_for_path(path)
            ptype_display = ptypes.PLOTHOLE_TYPE_VALUE_TO_UI_DISPLAY_MAP.get(ptype)
            
            
            tree_view_ui = tree.insert("", "end", text=story.get(sec.TITLE), values=(ptype_display), iid=path)
            folder = pathlib.Path(path).parent
            
            
            self.append_children(tree, tree_view_ui, folder, ptypes.PlotHoleType.STORY)
        
        tree.pack(fill="both", expand=True, padx=5, pady=5)   
        
        return tree