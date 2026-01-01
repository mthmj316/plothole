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

class __SEControls__(enum.StrEnum):
    ACCENT = 'accent'
    ALIAS = 'alias'
    CLOSE_BTN = 'close_btn'
    CONTENT = 'content'
    DELETE_BTN = 'delete_btn'
    DIALOG = 'dialog'
    GENRE = 'genre'
    HEADER = 'header'
    MESSAGE = 'msg'
    NEW_BTN = 'new_btn'
    OPEN_BTN = 'open_btn'
    PLOTHOLE_PTN = 'plothole_btn'
    REVERT_BTN = 'revert_btn'
    SAVE_BTN = 'save_btn'
    SEQUENTIAL_NO = 'sequential_no'
    SUB_BTN = 'sub_btn'
    TITLE = 'title'
    TOP_BTN = 'top_btn'
    UPDATE_BTN = 'update_btn'

class StoryElement(tk.Frame, UIObservable):
    def __init__(self, root, conf, *args, **kwargs):
        super().__init__(root, *args, **kwargs)       
        log.log_var(self, currentframe(), ("args", args), ("kwargs", kwargs))
        self.root = root
        self.observers = []
        
        self.labels = {}
        self.controls = {}
        self.controls_vars = {}
        
        self.configure_grid(conf)
        self.configure_header(conf)
        self.configure_alias(conf)
        self.configure_sequential_no(conf)
        
    def configure_sequential_no(self, conf):
        log.log_var(self, currentframe(), ("conf", conf))
        self.configure_label(conf, __SEControls__.SEQUENTIAL_NO)
        self.configure_option_menu(conf, __SEControls__.SEQUENTIAL_NO)
        
    def set_sequential_no(self, no):
        log.log_var(self, currentframe(), ("no", no))
        self.controls_vars.get(__SEControls__.SEQUENTIAL_NO).set(no)
        
    def get_sequential_no(self):
        log.log(self, currentframe())
        no =  self.controls_vars.get(__SEControls__.SEQUENTIAL_NO).get()
        log.log_var(self, currentframe(), ("no", no))
        return no
        
    def configure_alias(self, conf):
        log.log_var(self, currentframe(), ("conf", conf)) 
        self.configure_label(conf, __SEControls__.ALIAS)
        self.configure_entry(conf, __SEControls__.ALIAS)

    def disable_alias(self):
        log.log(self, currentframe())
        self.controls.get(__SEControls__.ALIAS).config(state='disabled')
        
    def enable_alias(self):
        log.log(self, currentframe())
        self.controls.get(__SEControls__.ALIAS).config(state='normal')
        
    def get_alias(self):
        log.log(self, currentframe())
        alias = self.controls_vars.get(__SEControls__.ALIAS).get()
        log.log_var(self, currentframe(), ("alias", alias))
        return alias
    
    def set_alias(self, alias):
        log.log_var(self, currentframe(), ("alias", alias))
        self.controls_vars.get(__SEControls__.ALIAS).set(alias)
    
    def configure_header(self, conf):
        log.log_var(self, currentframe(), ("conf", conf))
        self.configure_label(conf, __SEControls__.HEADER)

    def set_header(self, header):
        log.log_var(self, currentframe(), ("header", header))
        self.labels.get(__SEControls__.HEADER).config(text=header)

    def configure_option_menu(self, conf, secontrol):
        log.log_var(self, currentframe(), ("conf", conf), ("secontrol", secontrol))
        if not conf.is_hidden(secontrol):
            values = conf.get_option_menu_values(secontrol)
            menu_value = StringVar(self)
            self.controls_vars[secontrol.value] = menu_value
            menu_value.set(values[0])
            menu = tk.OptionMenu(self, menu_value, *values)            
            pos = conf.get_control_position(secontrol)
            menu.grid(row=pos[1], column=pos[0], columnspan=1, 
                       sticky=conf.get_control_sticky(secontrol), 
                       padx=conf.get_control_padx(secontrol), 
                       pady=conf.get_control_pady(secontrol))
            self.controls[secontrol.value] = menu   

    def configure_entry(self, conf, secontrol):
        log.log_var(self, currentframe(), ("conf", conf), ("secontrol", secontrol))
        if not conf.is_hidden(secontrol):
            entry_value = StringVar(self)
            self.controls_vars[secontrol.value] = entry_value
            entry = tk.Entry(self, textvariable=entry_value)
            pos = conf.get_control_position(secontrol)
            entry.grid(row=pos[1], column=pos[0], columnspan=1, 
                       sticky=conf.get_control_sticky(secontrol), 
                       padx=conf.get_control_padx(secontrol), 
                       pady=conf.get_control_pady(secontrol))
            self.controls[secontrol.value] = entry

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
        
    def configure_grid(self, conf):
        log.log_var(self, currentframe(), ("conf", conf))        
        for i in range(conf.get_grid_column_ctn()):
            self.grid_columnconfigure(i, weight=conf.get_col_weight(i))
        for i in range(conf.get_grid_row_ctn()):
            self.grid_rowconfigure(i, weight=conf.get_row_weight(i))
        
    def raise_frame(self, abovethis):
        log.log_var(self, currentframe(), ("abovethis", abovethis)) 

    def register(self, uiobserver):
        log.log_var(self, currentframe(), ("uiobserver", uiobserver))
        self.observers.append(uiobserver)
        
    def unregister(self, uiobserver):
        log.log_var(self, currentframe(), ("uiobserver", uiobserver))
        self.observers.pop(self.observers.index(uiobserver))

class __SEConfiguration__():
    def __init__(self):
        log.log(self, currentframe())
        self.column_ctn = 0
        self.row_ctn = 0
        self.column_weigths = {}
        self.row_weigths = {}
        self.lables = {}
        self.hidden_controls = []
        self.label_positions = {}
        self.control_positions = {}
        self.label_padx = {}
        self.label_pady = {}
        self.control_padx = {}
        self.control_pady = {}
        self.label_anchor = {}
        self.control_anchor = {}   
        self.label_sticky = {}
        self.control_sticky = {}   
        self.label_colspan = {}
        self.control_colspan = {}        
        self.label_font = {}
        self.control_font = {}
        self.option_menu_values = {}
        
    def __str__(self):        
        _str = (f"lables={self.lables};"
                f"column_ctn={self.column_ctn};"
                f"row_ctn={self.row_ctn};"
                f"hidden_controls={self.hidden_controls};"
                f"label_positions={self.label_positions};"
                f"control_positions={self.control_positions};"
                f"label_padx={self.label_padx};"
                f"label_pady={self.label_pady};"
                f"label_padx={self.control_padx};"
                f"label_anchor={self.label_anchor};"
                f"control_anchor={self.control_anchor};"
                f"label_sticky={self.label_sticky};"
                f"control_sticky={self.control_sticky};"
                f"label_colspan={self.label_colspan};"
                f"control_colspan={self.control_colspan};"
                f"label_font={self.label_font};"
                f"control_font={self.control_font};"
                f"control_font={self.control_font};")
        return _str

    def get_option_menu_values(self, secontrol):
        log.log_var(self, currentframe(), ("secontrol", secontrol))
        values = range(1,11) if secontrol not in self.option_menu_values.keys() else self.option_menu_values.get(secontrol)
        log.log_var(self, currentframe(), ("values", values))
        return values

    def set_option_menu_values(self, secontrol, values):
        log.log_var(self, currentframe(), ("secontrol", secontrol), ("values", values))
        self.option_menu_values[secontrol.value] = values  

    def set_label_font(self, secontrol, font):
        log.log_var(self, currentframe(), ("secontrol", secontrol), ("font", font))
        self.label_font[secontrol.value] = font

    def get_label_font(self, secontrol):
        log.log_var(self, currentframe(), ("secontrol", secontrol))
        font = tkFont.nametofont('TkDefaultFont') if secontrol not in self.label_font.keys() else self.label_font.get(secontrol)
        log.log_var(self, currentframe(), ("font", font))
        return font
    
    def set_control_font(self, secontrol, font):
        log.log_var(self, currentframe(), ("secontrol", secontrol), ("font", font))
        self.control_font[secontrol.value] = font

    def get_control_font(self, secontrol):
        log.log_var(self, currentframe(), ("secontrol", secontrol))
        font = tkFont.Font(family='Helvetica', size=12, weight=tkFont.NORMAL) if secontrol not in self.control_font.keys() else self.control_font.get(secontrol)
        log.log_var(self, currentframe(), ("colspan", font))
        return font

    def set_control_colspan(self, secontrol, colspan):
        log.log_var(self, currentframe(), ("secontrol", secontrol), ("colspan", colspan))
        self.control_colspan[secontrol.value] = colspan

    def get_control_colspan(self, secontrol):
        log.log_var(self, currentframe(), ("secontrol", secontrol))
        colspan = 1 if secontrol not in self.control_colspan.keys() else self.control_colspan.get(secontrol)
        log.log_var(self, currentframe(), ("colspan", colspan))
        return colspan

    def set_label_colspan(self, secontrol, colspan):
        log.log_var(self, currentframe(), ("secontrol", secontrol), ("colspan", colspan))
        self.label_colspan[secontrol.value] = colspan

    def get_label_colspan(self, secontrol):
        log.log_var(self, currentframe(), ("secontrol", secontrol))
        colspan = 1 if secontrol not in self.label_colspan.keys() else self.label_colspan.get(secontrol)
        log.log_var(self, currentframe(), ("colspan", colspan))
        return colspan

    def set_control_anchor(self, secontrol, anchor):
        log.log_var(self, currentframe(), ("secontrol", secontrol), ("anchor", anchor))
        self.control_anchor[secontrol.value] = anchor

    def get_control_anchor(self, secontrol):
        log.log_var(self, currentframe(), ("secontrol", secontrol))
        anchor = tk.NSEW if secontrol not in self.control_anchor.keys() else self.control_anchor.get(secontrol)
        log.log_var(self, currentframe(), ("anchor", anchor))
        return anchor

    def set_control_sticky(self, secontrol, sticky):
        log.log_var(self, currentframe(), ("secontrol", secontrol), ("sticky", sticky))
        self.control_sticky[secontrol.value] = sticky

    def get_control_sticky(self, secontrol):
        # is currently anchor values
        log.log_var(self, currentframe(), ("secontrol", secontrol))
        sticky = tk.NSEW if secontrol not in self.control_sticky.keys() else self.control_sticky.get(secontrol)
        log.log_var(self, currentframe(), ("sticky", sticky))
        return sticky

    def set_label_anchor(self, secontrol, anchor):
        log.log_var(self, currentframe(), ("secontrol", secontrol), ("anchor", anchor))
        self.label_anchor[secontrol.value] = anchor

    def get_label_anchor(self, secontrol):
        log.log_var(self, currentframe(), ("secontrol", secontrol))
        anchor = tk.E if secontrol not in self.label_anchor.keys() else self.label_anchor.get(secontrol)
        log.log_var(self, currentframe(), ("anchor", anchor))
        return anchor
 
    def set_label_sticky(self, secontrol, sticky):
        log.log_var(self, currentframe(), ("secontrol", secontrol), ("sticky", sticky))
        self.label_sticky[secontrol.value] = sticky
    
    def get_label_sticky(self, secontrol):
        # is currently anchor values
        log.log_var(self, currentframe(), ("secontrol", secontrol))
        sticky = tk.E if secontrol not in self.label_sticky.keys() else self.label_sticky.get(secontrol)
        log.log_var(self, currentframe(), ("sticky", sticky))
        return sticky

    def set_control_pady(self, secontrol, pady):
        log.log_var(self, currentframe(), ("secontrol", secontrol), ("pady", pady))
        self.control_pady[secontrol.value] = pady

    def get_control_pady(self, secontrol):
        log.log_var(self, currentframe(), ("secontrol", secontrol))
        pady = (5, 5) if secontrol not in self.control_pady.keys() else self.control_pady.get(secontrol)
        log.log_var(self, currentframe(), ("pady", pady))
        return pady

    def set_control_padx(self, secontrol, padx):
        log.log_var(self, currentframe(), ("secontrol", secontrol), ("padx", padx))
        self.control_padx[secontrol.value] = padx

    def get_control_padx(self, secontrol):
        log.log_var(self, currentframe(), ("secontrol", secontrol))
        padx = (5, 20) if secontrol not in self.control_padx.keys() else self.control_padx.get(secontrol)
        log.log_var(self, currentframe(), ("padx", padx))
        return padx 

    def set_label_pady(self, secontrol, pady):
        log.log_var(self, currentframe(), ("secontrol", secontrol), ("pady", pady))
        self.label_pady[secontrol.value] = pady

    def get_label_pady(self, secontrol):
        log.log_var(self, currentframe(), ("secontrol", secontrol))
        pady = (5, 5) if secontrol not in self.label_pady.keys() else self.label_pady.get(secontrol)
        log.log_var(self, currentframe(), ("pady", pady))
        return pady

    def set_label_padx(self, secontrol, padx):
        log.log_var(self, currentframe(), ("secontrol", secontrol), ("padx", padx))
        self.label_padx[secontrol.value] = padx

    def get_label_padx(self, secontrol):
        log.log_var(self, currentframe(), ("secontrol", secontrol))
        padx = (20, 5) if secontrol not in self.label_padx.keys() else self.label_padx.get(secontrol)
        log.log_var(self, currentframe(), ("padx", padx))
        return padx 

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

    def get_grid_column_ctn(self):
        log.log(self, currentframe())
        col_count = self.column_ctn
        log.log_var(self, currentframe(), ("col_count", col_count)) 
        return col_count
    
    def set_grid_column_ctn(self, ctn):
        log.log_var(self, currentframe(), ("ctn", ctn)) 
        self.column_ctn = ctn
    
    def get_grid_row_ctn(self):
        log.log(self, currentframe())
        row_count = self.row_ctn
        log.log_var(self, currentframe(), ("row_count", row_count)) 
        return row_count
    
    def set_grid_row_ctn(self, ctn):
        log.log_var(self, currentframe(), ("ctn", ctn))   
        self.row_ctn = ctn
    
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

def create_book_conf():
    
    conf = __SEConfiguration__()
    conf.set_column_weigth(1, 1)
    conf.set_row_weigth(4, 1)
    conf.set_grid_column_ctn(2)
    conf.set_grid_row_ctn(8)
    
    conf.set_label_colspan(__SEControls__.HEADER, 7)
    conf.set_label(__SEControls__.HEADER,'Neues Buch')
    conf.set_label_position(__SEControls__.HEADER, (0,0))
    conf.set_label_sticky(__SEControls__.HEADER, tk.W)
    
    conf.set_label(__SEControls__.SEQUENTIAL_NO,'Nr.')
    conf.set_label_position(__SEControls__.SEQUENTIAL_NO, (0,1))
    conf.set_control_position(__SEControls__.SEQUENTIAL_NO, (1,1))
    conf.set_control_sticky(__SEControls__.SEQUENTIAL_NO, tk.W)
    
    conf.set_label(__SEControls__.ALIAS,'Alias')
    conf.set_label_position(__SEControls__.ALIAS, (0,2))
    conf.set_control_position(__SEControls__.ALIAS, (1,2))
    
    conf.set_label_font(__SEControls__.HEADER, tkFont.Font(family='Helvetica', size=15, weight=tkFont.BOLD))
    conf.set_label_anchor(__SEControls__.HEADER, tk.W)
    
    return conf

def create_story_conf():
    conf = __SEConfiguration__()
    conf.set_column_weigth(1, 1)
    conf.set_row_weigth(4, 1)
    conf.set_grid_column_ctn(2)
    conf.set_grid_row_ctn(7)
    
    conf.set_label_colspan(__SEControls__.HEADER, 7)
    conf.set_label(__SEControls__.HEADER,'Neue Geschicht')
    conf.set_label_position(__SEControls__.HEADER, (0,0))
    conf.set_label_sticky(__SEControls__.HEADER, tk.W)
    
    conf.set_label(__SEControls__.ALIAS,'Alias')
    conf.set_label_position(__SEControls__.ALIAS, (0,1))
    conf.set_control_position(__SEControls__.ALIAS, (1,1))
    
    conf.set_label_font(__SEControls__.HEADER, tkFont.Font(family='Helvetica', size=15, weight=tkFont.BOLD))
    conf.set_label_anchor(__SEControls__.HEADER, tk.W)
    conf.hide_control(__SEControls__.SEQUENTIAL_NO)
    return conf
        
if __name__ == '__main__':
    
    log.ENABLE_LOGGING = True
    log.TRACE_ONLY = False
    
    w = tk.Tk()
    w.title("Story Element")
    w.geometry("1250x750+300+100")
    w.grid_columnconfigure(0, weight=1)
    w.grid_rowconfigure(0, weight=1)
    
    # conf = create_story_conf()    
    conf = create_book_conf()
    
    frame = StoryElement(w, conf)
    frame.grid(row=0, column=0, sticky="NSEW")
    frame.set_alias("Alles nur geklaut")
    frame.disable_alias()
    frame.enable_alias()
    print(frame.get_alias())
    
    frame.set_sequential_no(5)
    print(frame.get_sequential_no())
    
    w.mainloop()