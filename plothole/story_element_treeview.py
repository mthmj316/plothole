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
import time

class StoryElementTreeview(UIObservable):
    
    def __init__(self, path_repros, tree_container):
        
        self.path_repros = path_repros
        self.tree_container = tree_container
        self.observers = []
        self.last_element_id = '<start>'
        self.tree_view_folding_state = {}
        self.tree = None
        self.treeview = self.create_tree_view(self.tree_container)
        self.treeview.bind('<<TreeviewSelect>>', self.on_select)
        self.treeview.bind('<Double-1>', self.on_double_click)
        self.treeview.bind('<<TreeviewOpen>>', self.on_open)
        self.treeview.bind('<<TreeviewClose>>', self.on_close)
        self.navi = None
        self.selected_item = None

    def update_tree_view(self):
        log.log(self, currentframe())
        self.create_tree_view(self.tree_container)
        
        #time.sleep(5)
        
        if self.selected_item is not None:
            self.tree.selection_set(self.selected_item)
            #self.tree.focus(self.selected_item)
        

    def on_open(self, event):
        log.log_var(self, currentframe(), ("event", event))
        item = self.treeview.focus()
        self.tree_view_folding_state[item] = True
        
    def on_close(self, event):
        log.log_var(self, currentframe(), ("event", event))
        item = self.treeview.focus()
        self.tree_view_folding_state[item] = False

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
        self.selected_item = selection

    
    def append_children(self, tree, parent_ui, parent_path, parent_ptype):
        
        child_ptype = ptypes.CHILD_PLOTHOLE_TYPE.get(parent_ptype)
        
        if child_ptype is not None:        
            for element in sorted(hlp.get_all(parent_path, child_ptype, as_dict=True), key=lambda x: x[sec.SEQUENTIAL_NO.value]):
                
                path = hlp.get_path_for_alias(parent_path, element.get(sec.ALIAS), child_ptype)
                ptype_display = ptypes.PLOTHOLE_TYPE_VALUE_TO_UI_DISPLAY_MAP.get(child_ptype)
                
                tree_view_ui = tree.insert(parent_ui, "end", text=element.get(sec.TITLE), values=(ptype_display), iid=path)
                
                folder = pathlib.Path(path).parent
                
                self.append_children(tree, tree_view_ui, folder, ptypes.PlotHoleType(child_ptype))
                
                if tree_view_ui in self.tree_view_folding_state:
                    self.tree.item(tree_view_ui, open=self.tree_view_folding_state.get(tree_view_ui))
    
    def create_tree_view(self, tree_container):
        
        if self.tree is not None:
            self.tree.delete(*self.tree.get_children())
        else:
            self.tree = ttk.Treeview(tree_container)
        
        # Spalten definieren
        self.tree["columns"] = ("Type")
        
        # Erste Spalte (#0) = Baumspalte
        self.tree.heading("#0", text="Element")
        self.tree.column("#0", width=150)
        
        # Weitere Spalten
        self.tree.heading("Type", text="Type")
        self.tree.column("Type", width=80)

        self.tree.pack(fill='both', expand=True)
        
        for story in sorted(hlp.get_all_stories(self.path_repros, as_dict=True), key=lambda x: x[sec.TITLE.value]):
            
            log.log_var(self, currentframe(), ("story", story))
            
            path = hlp.get_story_path_by_alias(self.path_repros, story.get(sec.ALIAS))
            ptype = ptcore.get_ptype_for_path(path)
            ptype_display = ptypes.PLOTHOLE_TYPE_VALUE_TO_UI_DISPLAY_MAP.get(ptype)
            
            
            tree_view_ui = self.tree.insert("", "end", text=story.get(sec.TITLE), values=(ptype_display), iid=path)
            folder = pathlib.Path(path).parent
            
            if tree_view_ui in self.tree_view_folding_state:
                self.tree.item(tree_view_ui, open=self.tree_view_folding_state.get(tree_view_ui))
            
            
            self.append_children(self.tree, tree_view_ui, folder, ptypes.PlotHoleType.STORY)
        
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)   
        
        return self.tree