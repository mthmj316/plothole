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
from tkinter import scrolledtext as stxt

GENRES = ['', 'Abenteuer','Action','Alltag','Alternative','Comedy', 'Erotic', 
          'Excotic', 'Fantasy','Graphic Novel','Historie','Horror','Krimi',
          'Manga','Mystery','Romantik','Science Fiction','Superhelden',
          'Underground ','Western']

class __SEControls__(enum.StrEnum):
    ALIAS = 'alias'
    BTN_CLOSE = 'btn_close'
    BTN_DELETE = 'btn_delete'
    BTN_NEW = 'btn_new'
    BTN_NEXT = 'btn_next'
    BTN_OPEN = 'btn_open'
    BTN_PLOTHOLE = 'btn_plothole'
    BTN_PREVIOUS = 'btn_previous'
    BTN_REVERT = 'btn_revert'
    BTN_SAVE = 'btn_save'
    BTN_SUB = 'btn_sub'
    BTN_TOP = 'btn_top'
    BTN_UPDATE = 'btn_update'
    CONTENT = 'content'
    DIALOG = 'dialog'
    GENRE = 'genre'
    HEADER = 'header'
    MESSAGE = 'msg'
    SEQUENTIAL_NO = 'sequential_no'
    TITLE = 'title'
    TONE = 'tone'

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
        self.configure_title(conf)
        self.configure_tone(conf)
        self.configure_genre(conf)
        self.configure_message(conf)
        self.configure_content(conf)
        self.configure_actions(conf)    
    
    def configure_actions(self, conf):
        log.log_var(self, currentframe(), ("conf", conf))
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=conf.get_grid_row_ctn() - 1, column=1, 
                       columnspan=conf.get_grid_column_ctn() - 1,
                       sticky="NSEW", padx=(5,5), pady=(5,5))
        
        self.configure_button(conf, __SEControls__.BTN_CLOSE, self.on_close, btn_frame)
        self.configure_button(conf, __SEControls__.BTN_DELETE, self.on_delete, btn_frame)
        self.configure_button(conf, __SEControls__.BTN_NEW, self.on_new, btn_frame)
        self.configure_button(conf, __SEControls__.BTN_NEXT, self.on_next, btn_frame)
        self.configure_button(conf, __SEControls__.BTN_OPEN, self.on_open, btn_frame)
        self.configure_button(conf, __SEControls__.BTN_PLOTHOLE, self.on_plothole, btn_frame)
        self.configure_button(conf, __SEControls__.BTN_PREVIOUS, self.on_previous, btn_frame)
        self.configure_button(conf, __SEControls__.BTN_REVERT, self.on_revert, btn_frame)
        self.configure_button(conf, __SEControls__.BTN_SAVE, self.on_save, btn_frame)
        self.configure_button(conf, __SEControls__.BTN_SUB, self.on_sub, btn_frame)
        self.configure_button(conf, __SEControls__.BTN_TOP, self.on_top, btn_frame)
        self.configure_button(conf, __SEControls__.BTN_UPDATE, self.on_update, btn_frame)  
        
        
    def on_close(self):
        log.log(self, currentframe())
        
    def on_delete(self):
        log.log(self, currentframe())

    def on_new(self):
        log.log(self, currentframe())

    def on_next(self):
        log.log(self, currentframe())

    def on_open(self):
        log.log(self, currentframe())

    def on_plothole(self):
        log.log(self, currentframe())

    def on_previous(self):
        log.log(self, currentframe())

    def on_revert(self):
        log.log(self, currentframe())

    def on_save(self):
        log.log(self, currentframe())

    def on_sub(self):
        log.log(self, currentframe())

    def on_top(self):
        log.log(self, currentframe())
        
    def on_update(self):
        log.log(self, currentframe())
    
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

    def configure_content(self, content):
        log.log_var(self, currentframe(), ("content", content))
        self.configure_label(conf, __SEControls__.CONTENT)
        self.configure_scrolled_text(conf, __SEControls__.CONTENT)

    def set_content(self, content):
        log.log_var(self, currentframe(), ("content", content))
        content_stxt = self.controls.get(__SEControls__.CONTENT)
        content_stxt.delete('1.0', tk.END)
        content_stxt.insert(tk.INSERT, content)
        
    def get_content(self):
        log.log(self, currentframe())
        content_stxt = self.controls.get(__SEControls__.CONTENT)
        content =  content_stxt.get("1.0", tk.END)
        log.log_var(self, currentframe(), ("content", content))
        return content
        
    def configure_message(self, message):
        log.log_var(self, currentframe(), ("message", message))
        self.configure_label(conf, __SEControls__.MESSAGE)
        self.configure_entry(conf, __SEControls__.MESSAGE)

    def set_message(self, message):
        log.log_var(self, currentframe(), ("message", message))
        self.controls_vars.get(__SEControls__.MESSAGE).set(message)
        
    def get_message(self):
        log.log(self, currentframe())
        message =  self.controls_vars.get(__SEControls__.MESSAGE).get()
        log.log_var(self, currentframe(), ("message", message))
        return message
        
    def configure_genre(self, genre):
        log.log_var(self, currentframe(), ("genre", genre))
        self.configure_label(conf, __SEControls__.GENRE)
        self.configure_option_menu(conf, __SEControls__.GENRE)

    def set_genre(self, genre):
        log.log_var(self, currentframe(), ("genre", genre))
        self.controls_vars.get(__SEControls__.GENRE).set(genre)
        
    def get_genre(self):
        log.log(self, currentframe())
        genre =  self.controls_vars.get(__SEControls__.GENRE).get()
        log.log_var(self, currentframe(), ("genre", genre))
        return genre
        
    def configure_tone(self, tone):
        log.log_var(self, currentframe(), ("tone", tone))
        self.configure_label(conf, __SEControls__.TONE)
        self.configure_entry(conf, __SEControls__.TONE)

    def set_tone(self, tone):
        log.log_var(self, currentframe(), ("tone", tone))
        self.controls_vars.get(__SEControls__.TONE).set(tone)
        
    def get_tone(self):
        log.log(self, currentframe())
        tone =  self.controls_vars.get(__SEControls__.TONE).get()
        log.log_var(self, currentframe(), ("tone", tone))
        return tone
        
    def configure_title(self, conf):
        log.log_var(self, currentframe(), ("conf", conf))
        self.configure_label(conf, __SEControls__.TITLE)
        self.configure_entry(conf, __SEControls__.TITLE)

    def set_title(self, title):
        log.log_var(self, currentframe(), ("title", title))
        self.controls_vars.get(__SEControls__.TITLE).set(title)
        
    def get_title(self):
        log.log(self, currentframe())
        title =  self.controls_vars.get(__SEControls__.TITLE).get()
        log.log_var(self, currentframe(), ("title", title))
        return title
    
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

    def configure_scrolled_text(self, conf, secontrol):
        log.log_var(self, currentframe(), ("conf", conf), ("secontrol", secontrol))
        if not conf.is_hidden(secontrol):
            scrolled_text = stxt.ScrolledText(self)
            self.controls[secontrol.value] = scrolled_text           
            pos = conf.get_control_position(secontrol)
            scrolled_text.grid(
                row=pos[1], 
                column=pos[0], 
                columnspan=conf.get_control_colspan(secontrol), 
                sticky=conf.get_control_sticky(secontrol), 
                padx=conf.get_control_padx(secontrol), 
                pady=conf.get_control_pady(secontrol))

    def configure_option_menu(self, conf, secontrol):
        log.log_var(self, currentframe(), ("conf", conf), ("secontrol", secontrol))
        if not conf.is_hidden(secontrol):
            values = conf.get_option_menu_values(secontrol)
            menu_value = StringVar(self)
            self.controls_vars[secontrol.value] = menu_value
            menu_value.set(values[0])
            menu = tk.OptionMenu(self, menu_value, *values)            
            pos = conf.get_control_position(secontrol)
            menu.grid(row=pos[1], column=pos[0], 
                      columnspan=conf.get_control_colspan(secontrol), 
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
            entry.grid(row=pos[1], column=pos[0], 
                       columnspan=conf.get_control_colspan(secontrol), 
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
        # self.button_width = 20
        self.button_width = {}
        
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
                f"control_font={self.control_font};"
                f"button_width={self.button_width};")
        return _str
 
    def set_button_width(self, secontrol, width):
        log.log_var(self, currentframe(),("secontrol", secontrol), ("width", width))
        self.button_width[secontrol.value] = width

    def get_button_width(self, secontrol):
        log.log_var(self, currentframe(), ("secontrol", secontrol))
        width = 20 if secontrol not in self.button_width.keys() else self.button_width.get(secontrol)
        log.log_var(self, currentframe(), ("width", width))
        return width
        
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
    conf.set_column_weigth(3, 1)
    conf.set_column_weigth(5, 1)
    conf.set_row_weigth(3, 1)
    conf.set_grid_column_ctn(6)
    conf.set_grid_row_ctn(5)
    
    conf.set_label_colspan(__SEControls__.HEADER, 7)
    conf.set_label(__SEControls__.HEADER,'Neues Buch')
    conf.set_label_position(__SEControls__.HEADER, (0,0))
    conf.set_label_sticky(__SEControls__.HEADER, tk.W)
    conf.set_label_font(__SEControls__.HEADER, tkFont.Font(family='Helvetica', size=15, weight=tkFont.BOLD))
    conf.set_label_anchor(__SEControls__.HEADER, tk.W)
    
    conf.set_label(__SEControls__.SEQUENTIAL_NO,'Nr.')
    conf.set_label_position(__SEControls__.SEQUENTIAL_NO, (0,1))
    conf.set_control_position(__SEControls__.SEQUENTIAL_NO, (1,1))
    conf.set_control_sticky(__SEControls__.SEQUENTIAL_NO, tk.EW)
    
    secontrol = __SEControls__.ALIAS
    
    conf.set_label(secontrol,'Alias')
    conf.set_label_position(secontrol, (2,1))
    conf.set_control_position(secontrol, (3,1))
    conf.set_control_sticky(secontrol, tk.EW)

    secontrol = __SEControls__.TITLE

    conf.set_label(secontrol,'Titel')
    conf.set_label_position(secontrol, (4,1))
    conf.set_control_position(secontrol, (5,1))
    conf.set_control_sticky(secontrol, tk.EW)
    
    secontrol = __SEControls__.TONE

    conf.set_label(secontrol,'Tonfall')
    conf.set_label_position(secontrol, (2,2))
    conf.set_control_position(secontrol, (3,2))
    conf.set_control_sticky(secontrol, tk.EW)
    
    secontrol = __SEControls__.GENRE

    conf.set_label(secontrol,'Genre')
    conf.set_label_position(secontrol, (0,2))
    conf.set_control_position(secontrol, (1,2))
    conf.set_control_sticky(secontrol, tk.EW)
    conf.set_option_menu_values(secontrol, GENRES)
    
    secontrol = __SEControls__.MESSAGE

    conf.set_label(secontrol,'Botschaft')
    conf.set_label_position(secontrol, (4,2))
    conf.set_control_position(secontrol, (5,2))
    conf.set_control_sticky(secontrol, tk.EW)
    
    secontrol = __SEControls__.CONTENT

    conf.set_label(secontrol,'Inhalt')
    conf.set_label_position(secontrol, (0,3))
    conf.set_label_sticky(secontrol, tk.N)
    conf.set_control_position(secontrol, (1,3))
    conf.set_control_sticky(secontrol, tk.NSEW)
    conf.set_control_colspan(secontrol, 5)
    conf.set_control_pady(secontrol, (5,5))
    
    secontrol = __SEControls__.BTN_CLOSE    
    conf.set_control_position(secontrol, (3,0))
    conf.set_label(secontrol,'Schließen')
    conf.set_control_padx(secontrol, (1,1))
    
    secontrol = __SEControls__.BTN_DELETE   
    conf.set_control_position(secontrol, (2,0))
    conf.set_label(secontrol,'Löschen')
    conf.set_control_padx(secontrol, (1,1))
    
    secontrol = __SEControls__.BTN_PLOTHOLE   
    conf.set_control_position(secontrol, (5,0))
    conf.set_label(secontrol,'Plothole')
    conf.set_control_padx(secontrol, (1,1))
    
    secontrol = __SEControls__.BTN_REVERT   
    conf.set_control_position(secontrol, (1,0))
    conf.set_label(secontrol,'Zurücksetzen')
    conf.set_control_padx(secontrol, (1,1))
    
    secontrol = __SEControls__.BTN_SAVE
    conf.set_control_position(secontrol, (0,0))
    conf.set_label(secontrol,'Speichern')
    conf.set_control_padx(secontrol, (0,1))
    
    secontrol = __SEControls__.BTN_SUB
    conf.set_control_position(secontrol, (4,0))
    conf.set_label(secontrol,'Teile')
    conf.set_control_padx(secontrol, (1,1))
    
    secontrol = __SEControls__.BTN_NEXT
    conf.set_control_position(secontrol, (8,0))
    conf.set_label(secontrol,'>')
    conf.set_control_padx(secontrol, (1,1))
    conf.set_button_width(secontrol, 5)
    
    secontrol = __SEControls__.BTN_TOP
    conf.set_control_position(secontrol, (7,0))
    conf.set_label(secontrol,'^')
    conf.set_control_padx(secontrol, (1,1))
    conf.set_button_width(secontrol, 5)
    
    secontrol = __SEControls__.BTN_PREVIOUS
    conf.set_control_position(secontrol, (6,0))
    conf.set_label(secontrol,'<')
    conf.set_control_padx(secontrol, (1,1))
    conf.set_button_width(secontrol, 5)
    
    conf.hide_control(__SEControls__.BTN_NEW)
    conf.hide_control(__SEControls__.BTN_OPEN)
    conf.hide_control(__SEControls__.BTN_UPDATE)
    
    return conf

def create_story_conf():
    conf = __SEConfiguration__()
    conf.set_column_weigth(3, 1)
    conf.set_column_weigth(5, 1)
    conf.set_row_weigth(3, 1)
    conf.set_grid_column_ctn(6)
    conf.set_grid_row_ctn(5)
    
    conf.set_label_colspan(__SEControls__.HEADER, 7)
    conf.set_label(__SEControls__.HEADER,'Neue Geschicht')
    conf.set_label_position(__SEControls__.HEADER, (0,0))
    conf.set_label_sticky(__SEControls__.HEADER, tk.W)
    conf.set_label_font(__SEControls__.HEADER, tkFont.Font(family='Helvetica', size=15, weight=tkFont.BOLD))
    conf.set_label_anchor(__SEControls__.HEADER, tk.W)
    
    conf.hide_control(__SEControls__.SEQUENTIAL_NO)
    
    secontrol = __SEControls__.ALIAS
    
    conf.set_label(secontrol,'Alias')
    conf.set_label_position(secontrol, (2,1))
    conf.set_control_position(secontrol, (3,1))
    conf.set_control_sticky(secontrol, tk.EW)

    secontrol = __SEControls__.TITLE

    conf.set_label(secontrol,'Titel')
    conf.set_label_position(secontrol, (4,1))
    conf.set_control_position(secontrol, (5,1))
    conf.set_control_sticky(secontrol, tk.EW)
    
    secontrol = __SEControls__.TONE

    conf.set_label(secontrol,'Tonfall')
    conf.set_label_position(secontrol, (2,2))
    conf.set_control_position(secontrol, (3,2))
    conf.set_control_sticky(secontrol, tk.EW)
    
    secontrol = __SEControls__.GENRE

    conf.set_label(secontrol,'Genre')
    conf.set_label_position(secontrol, (0,2))
    conf.set_control_position(secontrol, (1,2))
    conf.set_control_sticky(secontrol, tk.EW)
    conf.set_option_menu_values(secontrol, GENRES)
    
    secontrol = __SEControls__.MESSAGE

    conf.set_label(secontrol,'Botschaft')
    conf.set_label_position(secontrol, (4,2))
    conf.set_control_position(secontrol, (5,2))
    conf.set_control_sticky(secontrol, tk.EW)
    
    secontrol = __SEControls__.CONTENT

    conf.set_label(secontrol,'Inhalt')
    conf.set_label_position(secontrol, (0,3))
    conf.set_label_sticky(secontrol, tk.N)
    conf.set_control_position(secontrol, (1,3))
    conf.set_control_sticky(secontrol, tk.NSEW)
    conf.set_control_colspan(secontrol, 5)
    conf.set_control_pady(secontrol, (5,5))
    
    secontrol = __SEControls__.BTN_CLOSE    
    conf.set_control_position(secontrol, (3,0))
    conf.set_label(secontrol,'Schließen')
    conf.set_control_padx(secontrol, (1,1))
    
    secontrol = __SEControls__.BTN_DELETE   
    conf.set_control_position(secontrol, (2,0))
    conf.set_label(secontrol,'Löschen')
    conf.set_control_padx(secontrol, (1,1))
    
    secontrol = __SEControls__.BTN_PLOTHOLE   
    conf.set_control_position(secontrol, (5,0))
    conf.set_label(secontrol,'Plothole')
    conf.set_control_padx(secontrol, (1,1))
    
    secontrol = __SEControls__.BTN_REVERT   
    conf.set_control_position(secontrol, (1,0))
    conf.set_label(secontrol,'Zurücksetzen')
    conf.set_control_padx(secontrol, (1,1))
    
    secontrol = __SEControls__.BTN_SAVE
    conf.set_control_position(secontrol, (0,0))
    conf.set_label(secontrol,'Speichern')
    conf.set_control_padx(secontrol, (0,1))
    
    secontrol = __SEControls__.BTN_SUB
    conf.set_control_position(secontrol, (4,0))
    conf.set_label(secontrol,'Bücher')
    conf.set_control_padx(secontrol, (1,1))
    
    conf.hide_control(__SEControls__.BTN_NEW)
    conf.hide_control(__SEControls__.BTN_NEXT)
    conf.hide_control(__SEControls__.BTN_OPEN)
    conf.hide_control(__SEControls__.BTN_PREVIOUS)
    conf.hide_control(__SEControls__.BTN_TOP)
    conf.hide_control(__SEControls__.BTN_UPDATE)
    
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

    
    w.mainloop()