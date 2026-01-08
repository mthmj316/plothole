# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 19:06:24 2026

@author: mthoma
"""
import tkinter as tk
from observers import UIObservable
from tkinter import font as tkFont
from tkinter import scrolledtext as stxt
from tkinter import StringVar
from tkinter import messagebox as mb
from inspect import currentframe
import logger as log
import enum
from navigator import NavigationPoint
from story_element_ui import __SEControls__
from story_element_ui import __SEConfiguration__
from plothole_types import PlotHoleType

class StoryElementOverview(tk.Frame, UIObservable, NavigationPoint):
    
    def __init__(self, root, conf, ph_type, *args, **kwargs):
        super().__init__(root, *args, **kwargs)       
        log.log_var(self, currentframe(),("root", root), ("conf", conf), ("ph_type", ph_type), ("args", args), ("kwargs", kwargs))
        self.root = root
        self.ph_type = ph_type
        self.grid_columnconfigure(0, weight=1)       
        self.observers = []
        self.navigators = []
        self.labels = {}        
        self.controls = {}
        self.se_lables = {}
        
        self.configure_header(conf)
        self.configure_actions(conf)
        
    def add_overview_item(self, _id, display):
        log.log_var(self, currentframe(), ("_id", _id), ("display", display))
        se_lb = tk.Label(self, text=display, borderwidth=2, relief="groove")
        se_lb.bind('<Double-Button-1>', func=lambda x: self.on_item_select(_id))
        se_lb.grid(row=len(self.se_lables) + 2, 
                column=0, 
                columnspan=1,
                sticky=tk.NSEW,
                padx=10,
                pady=5)
        se_lb['font'] = tkFont.Font(family='Helvetica', size=15, weight=tkFont.BOLD)
        self.se_lables[_id] = se_lb

    def on_item_select(self, _id):
        log.log_var(self, currentframe(), ("_id", _id))
        for observer in self.observers:
            observer.on_open(_id, self.ph_type)
            
        for navigator in self.navigators:
            navigator.on_open(self.ph_type)

    def remove_all_overview_items(self):
        log.log(self, currentframe())
        for se_lb_key in self.se_lables.keys():
            self.se_lables.get(se_lb_key).destroy()            
        self.se_lables.clear()
    
    def configure_actions(self, conf):
        log.log_var(self, currentframe(), ("conf", conf))
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=1, column=0, sticky="NSEW", padx=(5,5), pady=(5,5))
        
        self.configure_button(conf, __SEControls__.BTN_CHARACTER, self.on_character, btn_frame)
        self.configure_button(conf, __SEControls__.BTN_CLOSE, self.on_close, btn_frame)
        self.configure_button(conf, __SEControls__.BTN_NEW, self.on_new, btn_frame)
        self.configure_button(conf, __SEControls__.BTN_PLOTHOLE, self.on_plothole, btn_frame)
        self.configure_button(conf, __SEControls__.BTN_TOP, self.on_top, btn_frame)

    def on_character(self):
       log.log(self, currentframe())
       for observer in self.observers:
           observer.on_character()
           
       for navigator in self.navigators:
           navigator.on_character()        
        
    def on_close(self):
        log.log(self, currentframe())
        for observer in self.observers:
            observer.on_close()
            
        for navigator in self.navigators:
            navigator.on_close()

    def on_new(self):
        log.log(self, currentframe())
        for observer in self.observers:
            observer.on_new()
            
        for navigator in self.navigators:
            navigator.on_new()

    def on_plothole(self):
        log.log(self, currentframe())
        for observer in self.observers:
            observer.on_plothole()
            
        for navigator in self.navigators:
            navigator.on_plothole()

    def on_top(self):
        log.log(self, currentframe())
        for observer in self.observers:
            observer.on_top()
            
        for navigator in self.navigators:
            navigator.on_top()
            
    def configure_button(self, conf, secontrol, action, parent):
        log.log_var(self, currentframe(), ("conf", conf), ("secontrol", secontrol))
        if not conf.is_hidden(secontrol):
            btn = tk.Button(
                parent, 
                text=conf.get_label(secontrol), 
                command=action)
            btn.config(width=conf.get_button_width(secontrol))
            pos = conf.get_control_position(secontrol)
            btn.grid(
                row=pos[1], 
                column=pos[0], 
                sticky=conf.get_control_sticky(secontrol), 
                padx=conf.get_control_padx(secontrol), 
                pady=conf.get_control_pady(secontrol))
            self.controls[secontrol.value] = btn

    def configure_header(self, conf):
        log.log_var(self, currentframe(), ("conf", conf))
        self.configure_label(conf, __SEControls__.HEADER)
        
    def configure_label(self, conf, secontrol):
        log.log_var(self, currentframe(), ("conf", conf), ("secontrol", secontrol))
        if not conf.is_hidden(secontrol):
            lb = tk.Label(self, text=conf.get_label(secontrol), 
                               anchor=conf.get_label_anchor(secontrol))
            pos = conf.get_label_position(secontrol)
            lb.grid(row=pos[1], column=pos[0], 
                         columnspan=conf.get_label_colspan(secontrol), 
                         sticky=conf.get_label_sticky(secontrol),
                         padx=conf.get_label_padx(secontrol), 
                         pady=conf.get_label_pady(secontrol))
            lb['font'] = conf.get_label_font(secontrol)
            self.labels[secontrol.value] = lb
            
    def register(self, uiobserver):
        log.log_var(self, currentframe(), ("uiobserver", uiobserver))
        self.observers.append(uiobserver)
        
    def unregister(self, uiobserver):
        log.log_var(self, currentframe(), ("uiobserver", uiobserver))
        self.observers.pop(self.observers.index(uiobserver))
        
    def add_navigator(self, navigator):
        log.log_var(self, currentframe(), ("navigator", navigator))
        self.navigators.append(navigator)

    def remove_mavigator(self, navigator):
        log.log_var(self, currentframe(), ("navigator", navigator))
        self.navigators.pop(self.navigators.index(navigator))        

def create_book_conf():
    
    conf = __SEConfiguration__()
    conf.set_column_weigth(3, 1)
    conf.set_column_weigth(5, 1)
    conf.set_row_weigth(3, 1)
    conf.set_grid_column_ctn(6)
    conf.set_grid_row_ctn(5)
    
    conf.set_label_colspan(__SEControls__.HEADER, 7)
    conf.set_label(__SEControls__.HEADER,'Bücher Übersicht')
    conf.set_label_position(__SEControls__.HEADER, (0,0))
    conf.set_label_sticky(__SEControls__.HEADER, tk.W)
    conf.set_label_font(__SEControls__.HEADER, tkFont.Font(family='Helvetica', size=15, weight=tkFont.BOLD))
    conf.set_label_anchor(__SEControls__.HEADER, tk.W)
    
    btn_width = 15
    
    secontrol = __SEControls__.BTN_CHARACTER 
    conf.set_control_position(secontrol, (3,0))
    conf.set_label(secontrol,'Charakter')
    conf.set_control_padx(secontrol, (1,1))
    conf.set_button_width(secontrol, btn_width)

    secontrol = __SEControls__.BTN_CLOSE
    conf.set_control_position(secontrol, (0,0))
    conf.set_label(secontrol,'Neu')
    conf.set_control_padx(secontrol, (20,1))
    conf.set_button_width(secontrol, btn_width)
    
    secontrol = __SEControls__.BTN_NEW
    conf.set_control_position(secontrol, (1,0))
    conf.set_label(secontrol,'Schließen')
    conf.set_control_padx(secontrol, (1,1))
    conf.set_button_width(secontrol, btn_width)
    
    secontrol = __SEControls__.BTN_PLOTHOLE
    conf.set_control_position(secontrol, (2,0))
    conf.set_label(secontrol,'Plothole')
    conf.set_control_padx(secontrol, (1,1))
    conf.set_button_width(secontrol, btn_width)
    
    secontrol = __SEControls__.BTN_TOP
    conf.set_control_position(secontrol, (4,0))
    conf.set_label(secontrol,'^')
    conf.set_control_padx(secontrol, (1,1))
    conf.set_button_width(secontrol, 5)
    
    return conf

def create_story_conf():
    
    conf = __SEConfiguration__()
    conf.set_column_weigth(3, 1)
    conf.set_column_weigth(5, 1)
    conf.set_row_weigth(3, 1)
    conf.set_grid_column_ctn(6)
    conf.set_grid_row_ctn(5)
    
    conf.set_label_colspan(__SEControls__.HEADER, 7)
    conf.set_label(__SEControls__.HEADER,'Geschichten Übersicht')
    conf.set_label_position(__SEControls__.HEADER, (0,0))
    conf.set_label_sticky(__SEControls__.HEADER, tk.W)
    conf.set_label_font(__SEControls__.HEADER, tkFont.Font(family='Helvetica', size=15, weight=tkFont.BOLD))
    conf.set_label_anchor(__SEControls__.HEADER, tk.W)
    
    btn_width = 15
    
    secontrol = __SEControls__.BTN_CHARACTER 
    conf.set_control_position(secontrol, (2,0))
    conf.set_label(secontrol,'Charakter')
    conf.set_control_padx(secontrol, (1,1))
    conf.set_button_width(secontrol, btn_width)
    
    secontrol = __SEControls__.BTN_NEW
    conf.set_control_position(secontrol, (0,0))
    conf.set_label(secontrol,'Neu')
    conf.set_control_padx(secontrol, (20,1))
    conf.set_button_width(secontrol, btn_width)
    
    secontrol = __SEControls__.BTN_PLOTHOLE
    conf.set_control_position(secontrol, (1,0))
    conf.set_label(secontrol,'Plothole')
    conf.set_control_padx(secontrol, (1,1))
    conf.set_button_width(secontrol, btn_width)
    
    conf.hide_control(__SEControls__.BTN_CLOSE)
    conf.hide_control(__SEControls__.BTN_TOP)
    
    return conf
        
if __name__ == '__main__':
    
    log.ENABLE_LOGGING = True
    log.TRACE_ONLY = False
    
    w = tk.Tk()
    w.title("Story Element Overview")
    w.geometry("1250x750+300+100")
    w.grid_columnconfigure(0, weight=1)
    w.grid_rowconfigure(0, weight=1)
    
    conf = create_book_conf()
    
    frame = StoryElementOverview(w, conf, PlotHoleType.STORY)
    frame.grid(row=0, column=0, sticky="NSEW")
    
    frame.add_overview_item("test_id", 'Test Eintrag')
    frame.add_overview_item("cooleStory", 'Alaska')
    
    frame.remove_all_overview_items()

    
    w.mainloop()