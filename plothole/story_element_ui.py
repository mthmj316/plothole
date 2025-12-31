# -*- coding: utf-8 -*-
"""
Created on Wed Dec 31 10:45:35 2025

@author: mthoma
"""
import tkinter as tk
from observers import UIObservable
from tkinter import font as tkFont
from plothole_types import PlotHoleType 
from tkinter import scrolledtext as stxt
from tkinter.filedialog import askopenfilename
from tkinter import StringVar
from tkinter import messagebox as mb
from inspect import currentframe
import logger as log
import enum

class __SEControlls__(enum.StrEnum):
    ACCENT = 'accent'
    ALIAS = 'alias'
    CLOSE = 'close'
    CONTENT = 'content'
    DELETE = 'delete'
    DIALOG = 'dialog'
    GENRE = 'genre'
    HEADER = 'header'
    MESSAGE = 'msg'
    NEW = 'new'
    OPEN = 'open'
    PLOTHOLE = 'plothole'
    REVERT = 'revert'
    SAVE = 'save'
    SUB = 'sub'
    TITLE = 'title'
    UPDATE = 'update'

class StoryElement(tk.Frame, UIObservable):
    def __init__(self, root, conf, *args, **kwargs):
        super().__init__(root, *args, **kwargs)       
        log.log_var(self, currentframe(), ("args", args), ("kwargs", kwargs))
        self.root = root
        self.observers = []
        self.default_font = tkFont.Font(family='Helvetica', size=20, weight='bold')    
        
        self.configure_grid(conf)
        self.configure_header(conf)
        self.configure_alias_ui(conf)
    
    def configure_header(self, conf):
        log.log_var(self, currentframe(), ("conf", conf))
        if not conf.is_hidden(__SEControlls__.HEADER):
            self.lb_header = tk.Label(self, text=conf.get_label(__SEControlls__.HEADER), anchor=tk.W,)
            pos = conf.get_label_position(__SEControlls__.HEADER)
            self.lb_header.grid(row=pos[1], column=pos[0], columnspan=conf.get_header_colspan(), sticky=tk.W, padx=5, pady=5)
            self.lb_header['font'] = self.default_font  
    
    def configure_grid(self, conf):
        log.log_var(self, currentframe(), ("conf", conf))        
        for i in range(conf.grid_column_ctn()):
            self.grid_columnconfigure(i, weight=conf.get_col_weight(i))
        for i in range(conf.grid_row_ctn()):
            self.grid_rowconfigure(i, weight=conf.get_row_weight(i))
    
    def configure_alias_ui(self, conf):
        log.log_var(self, currentframe(), ("conf", conf)) 
        if not conf.is_hidden(__SEControlls__.ALIAS):
            self.lb_alias = tk.Label(self, text=conf.get_label(__SEControlls__.ALIAS))
            pos = conf.get_label_position(__SEControlls__.ALIAS)
            self.lb_alias.grid(row=pos[1], column=pos[0], sticky=tk.E, padx=5, pady=5)  
            self.tb_alias_value = StringVar()
            self.tb_alias = tk.Entry(self, textvariable=self.tb_alias_value)
            pos = conf.get_control_position(__SEControlls__.ALIAS)
            self.tb_alias.grid(row=pos[1], column=pos[0], columnspan=conf.get_input_colspan(), sticky=tk.NSEW, padx=5, pady=5)
    
    def raise_frame(self, abovethis):
        log.log_var(self, currentframe(), ("abovethis", abovethis)) 

    def register(self, uiobserver):
        log.log_var(self, currentframe(), ("uiobserver", uiobserver))
        self.observers.append(uiobserver)
        
    def unregister(self, uiobserver):
        log.log_var(self, currentframe(), ("uiobserver", uiobserver))
        self.observers.pop(self.observers.index(uiobserver))

    def set_header(self, header):
        log.log_var(self, currentframe(), ("header", header))
        self.lb_header.config(text=header)

class __SEConfiguration__():
    def __init__(self):
        log.log(self, currentframe())
        self.column_weigths = {}
        self.row_weigths = {}
        self.lables = {}
        self.set_label(__SEControlls__.HEADER, "New Element")
        self.hidden_controls = []
        self.label_positions = {}
        self.control_positions = {}
        
    def __str__(self):        
        _str = (f"lables={self.lables};"
                f"hidden_controls={self.hidden_controls};"
                f"label_positions={self.label_positions};"
                f"control_positions={self.control_positions};")
        return _str

    def set_label_position(self, secontrol, position):
        log.log_var(self, currentframe(), ("secontrol", secontrol), ("position", position))
        self.label_positions[secontrol.value] = position
        
    def get_label_position(self, secontrol):
        log.log_var(self, currentframe(), ("secontrol", secontrol))
        position = (0,0) if secontrol not in self.label_positions.keys() else self.label_positions.get(secontrol)
        log.log_var(self, currentframe(), ("position", position))
        return position 

    def set_control_position(self, secontrol, position):
        log.log_var(self, currentframe(), ("secontrol", secontrol), ("position", position))
        self.control_positions[secontrol.value] = position
        
    def get_control_position(self, secontrol):
        log.log_var(self, currentframe(), ("secontrol", secontrol))
        position = (0,0) if secontrol not in self.control_positions.keys() else self.control_positions.get(secontrol)
        log.log_var(self, currentframe(), ("position", position))
        return position    

    def get_header_colspan(self):
        log.log(self, currentframe())
        colspan = self.grid_column_ctn()
        log.log_var(self, currentframe(), ("colspan", colspan))         
        return colspan
    
    def get_input_colspan(self):
        log.log(self, currentframe())
        colspan = self.grid_column_ctn() - 1
        log.log_var(self, currentframe(), ("colspan", colspan))         
        return colspan
        
    def hide_control(self, secontrol):
        log.log_var(self, currentframe(), ("secontrol", secontrol))   
        self.hidden_controls.append(secontrol.value)

    def is_hidden(self, secontrol):
        log.log_var(self, currentframe(), ("secontrol", secontrol))
        hidden = (secontrol in self.hidden_controls)
        log.log_var(self, currentframe(), ("hidden", hidden))
        return hidden
    
    def set_label(self, secontrol, lable):
        log.log_var(self, currentframe(), ("secontrol", secontrol), ("lable", lable))
        self.lables[secontrol.value] = lable
    
    def get_label(self, secontrol):
        log.log_var(self, currentframe(), ("secontrol", secontrol))
        label = 'NA'
        if secontrol in self.lables.keys():
            label = self.lables.get(secontrol)
        log.log_var(self, currentframe(), ("label", label))
        return label
    
    def set_column_weigth(self, col_num, weight):
        log.log_var(self, currentframe(), ("col_num", col_num), ("weight", weight)) 
        self.column_weigths[col_num] = weight

    def set_row_weigth(self, row_num, weight):
        log.log_var(self, currentframe(), ("row_num", row_num), ("weight", weight)) 
        self.row_weigths[row_num] = weight

    def grid_column_ctn(self):
        log.log(self, currentframe())
        col_count = 2
        log.log_var(self, currentframe(), ("col_count", col_count)) 
        return col_count
    
    def grid_row_ctn(self):
        log.log(self, currentframe())
        row_count = 7
        log.log_var(self, currentframe(), ("row_count", row_count)) 
        return row_count
    
    def get_col_weight(self, col_num):
        log.log_var(self, currentframe(), ("col_num", col_num))        
        weight = 0
        if col_num in self.column_weigths.keys():
            weight = self.column_weigths.get(col_num)
        log.log_var(self, currentframe(), ("weight", weight))        
        return weight

    def get_row_weight(self, row_num):
        log.log_var(self, currentframe(), ("row_num", row_num))        
        weight = 0
        if row_num in self.row_weigths.keys():
            weight = self.row_weigths.get(row_num)
        log.log_var(self, currentframe(), ("weight", weight))        
        return weight

def create_story_conf():
    conf = __SEConfiguration__()
    conf.set_column_weigth(1, 1)
    conf.set_row_weigth(4, 1)
    conf.set_label(__SEControlls__.HEADER,'Guter alter junger Dorian')
    conf.set_label(__SEControlls__.ALIAS,'Alias')
    conf.set_label_position(__SEControlls__.HEADER, (0,0))
    conf.set_label_position(__SEControlls__.ALIAS, (0,1))
    conf.set_control_position(__SEControlls__.ALIAS, (1,1))
    return conf
        
if __name__ == '__main__':
    
    log.ENABLE_LOGGING = True
    log.TRACE_ONLY = False
    
    w = tk.Tk()
    w.title("Story Element")
    w.geometry("1250x750+300+100")
    w.grid_columnconfigure(0, weight=1)
    w.grid_rowconfigure(0, weight=1)
    
    conf = create_story_conf()    
    
    frame = StoryElement(w, conf)
    frame.grid(row=0, column=0, sticky="NSEW")
    
    w.mainloop()