# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 10:02:08 2025

@author: mthoma
"""
import tkinter as tk
from observers import UIObservable
from tkinter import font as tkFont
from plothole_types import PlotHoleType 
from tkinter import StringVar
from tkinter import messagebox as mb
from tkinter import scrolledtext as stxt
from tkinter.filedialog import askopenfilename
from inspect import currentframe
import logger as log

PAD_X_RIGHT_BOLD = (5, 20)
PAD_X_LEFT_BOLD = (20, 5)

PAD_X_TOP_BOLD = (20, 5)
PAD_X_BOTTON_BOLD = (5,20)

COLSPAN_RIGHT = 5

BUTTON_WIDTH = 20

class BookFrame(tk.Frame, UIObservable):
    
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
       
        log.log_var(self, currentframe(), ("args", args), ("kwargs", kwargs))
        
        self.root = root
        self.observers = []
        self.default_font = tkFont.Font(family='Helvetica', size=20, weight='bold')    
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(4, weight=1)
        
        self.lb_header = tk.Label(self, text="Neues Buch:", anchor=tk.W,)
        self.lb_header.grid(row=0, columnspan=2, column=0, sticky=tk.W, padx=(5,5), pady=(5,5))
        self.lb_header['font'] = self.default_font        
        
        lb_alias = tk.Label(self, text="Alias")
        lb_title = tk.Label(self, text="Titel")
        lb_accent = tk.Label(self, text="Tonfall")
        lb_msg = tk.Label(self, text="Botschaft")
        lb_basic_idea = tk.Label(self, text="Inhalt")
        
        self.tb_alias_value = StringVar()
        self.tb_alias = tk.Entry(self, textvariable=self.tb_alias_value)
        
        self.tb_title_value = StringVar()
        tb_title = tk.Entry(self, textvariable=self.tb_title_value)
        
        self.tb_accent_value = StringVar()
        tb_accent = tk.Entry(self, textvariable=self.tb_accent_value)
        
        self.sta_msg = stxt.ScrolledText(self, width=200, height=5)
        
        self.sta_basic_idea = stxt.ScrolledText(self, width=200, height=30)    
        
        lb_alias.grid(row=1, column=0, sticky="E", padx=PAD_X_LEFT_BOLD, pady=5)       
        self.tb_alias.grid(row=1, column=1, columnspan=COLSPAN_RIGHT, sticky="NSEW", padx=PAD_X_RIGHT_BOLD, pady=5)
        
        lb_title.grid(row=2, column=0, sticky="E", padx=PAD_X_LEFT_BOLD, pady=5)
        tb_title.grid(row=2, column=1, columnspan=COLSPAN_RIGHT, sticky="NSEW", padx=PAD_X_RIGHT_BOLD, pady=5)
        
        lb_accent.grid(row=3, column=0, sticky="NE", padx=PAD_X_LEFT_BOLD, pady=5)
        tb_accent.grid(row=3, column=1, columnspan=COLSPAN_RIGHT, sticky="NSEW", padx=PAD_X_RIGHT_BOLD, pady=5)
        
        lb_msg.grid(row=4, column=0, sticky="NE", padx=PAD_X_LEFT_BOLD, pady=5)
        self.sta_msg.grid(row=4, column=1, columnspan=COLSPAN_RIGHT, sticky="NSEW", padx=PAD_X_RIGHT_BOLD, pady=5)
        
        lb_basic_idea.grid(row=5, column=0, sticky="NE", padx=PAD_X_LEFT_BOLD, pady=PAD_X_BOTTON_BOLD)
        self.sta_basic_idea.grid(row=5, column=1, columnspan=COLSPAN_RIGHT, sticky="NSEW", padx=PAD_X_RIGHT_BOLD, pady=5)
        
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=6, column=1, sticky="NSEW", padx=PAD_X_RIGHT_BOLD, pady=5)
       
        btn_save = tk.Button(btn_frame, text="Speichern", command=self.save)
        btn_save.config(width=BUTTON_WIDTH)
        btn_save.grid(row=0, column=1, sticky="NSEW", padx=(1,1), pady=5)
        
        btn_revert = tk.Button(btn_frame, text="Zurücksetzen", command=self.revert)
        btn_revert.config(width=BUTTON_WIDTH)
        btn_revert.grid(row=0, column=2, sticky="NSEW", padx=(1,1), pady=5)
        
        btn_delete = tk.Button(btn_frame, text="Löschen", command=self.delete)
        btn_delete.config(width=BUTTON_WIDTH)
        btn_delete.grid(row=0, column=3, sticky="NSEW", padx=(1,0), pady=5)
        
        btn_close = tk.Button(btn_frame, text="Schließen", command=self.close)
        btn_close.config(width=BUTTON_WIDTH)
        btn_close.grid(row=0, column=4, sticky="NSEW", padx=(1,0), pady=5)
    
    def set_header(self, header):
        log.log_var(self, currentframe(), ("header", header))
        self.lb_header.config(text=header)
    
    def close(self):
        log.log(self, currentframe())
        self.root.close_me(self)
        for observer in self.observers:
            observer.onClose()
    
    def set_base_dir(self, base_dir):
        log.log_var(self, currentframe(), ("base_dir", base_dir))
        self.base_dir = base_dir

    def _open(self):
        log.log(self, currentframe())
        self.story_file = askopenfilename(initialdir=self.base_dir)
        for observer in self.observers:
            observer.onLoad(self.story_file)
        
    def save(self):
        log.log(self, currentframe())
        for observer in self.observers:
            observer.onSave()

    def update(self):
        log.log(self, currentframe())
        for observer in self.observers:
            observer.onUpdate()
    
    def delete(self):
        log.log(self, currentframe())
        for observer in self.observers:
            observer.onDelete()
        self.root.close_me(self)

    def revert(self):
        log.log(self, currentframe())
        for observer in self.observers:
            observer.onRevert()
    
    def back(self):
        log.log(self, currentframe())
        self.root.close_me(self)
    
    def raise_frame(self, abovethis):
        log.log_var(self, currentframe(), ("abovethis", abovethis))
        self.tkraise(aboveThis=abovethis)
        for observer in self.observers:
            observer.onDisplay(self)       

    def get_alias(self):
        log.log(self, currentframe())
        return self.tb_alias_value.get()
    
    def set_alias(self, alias):
        log.log_var(self, currentframe(), ("alias", alias))
        self.tb_alias_value.set(alias)
    
    def get_title(self):
        log.log(self, currentframe())
        log.log(self, currentframe())
        return self.tb_title_value.get()
    
    def set_title(self, title):
        log.log_var(self, currentframe(), ("title", title))
        self.tb_title_value.set(title)
    
    def get_accent(self):
        log.log(self, currentframe())
        return self.tb_accent_value.get()
    
    def set_accent(self, accent):
        log.log_var(self, currentframe(), ("accent", accent))
        self.tb_accent_value.set(accent)
  
    def get_genre(self):
        log.log(self, currentframe())
        return self.tb_genre_value.get()
    
    def set_genre(self, genre):
        log.log_var(self, currentframe(), ("genre", genre))
        self.tb_genre_value.set(genre)
    
    def get_message(self):
        log.log(self, currentframe())
        return self.sta_msg.get("1.0", tk.END)
    
    def set_message(self, msg):
        log.log_var(self, currentframe(), ("msg", msg))
        self.sta_msg.delete('1.0', tk.END)
        self.sta_msg.insert(tk.INSERT, msg)
    
    def get_basic_idea(self):
        log.log(self, currentframe())
        return self.sta_basic_idea.get("1.0", tk.END)
    
    def set_basic_idea(self, basic_idea):
        log.log_var(self, currentframe(), ("basic_idea", basic_idea))
        self.sta_basic_idea.delete('1.0', tk.END)
        self.sta_basic_idea.insert(tk.INSERT, basic_idea)
    
    def raise_error(self, error):
        log.log_var(self, currentframe(), ("error", error))
        mb.showerror("Fehler", error)
        
    def disable_alias(self):
        log.log(self, currentframe())
        self.tb_alias.config(state='disabled')
        
    def enable_alias(self):
        log.log(self, currentframe())
        log.log(self, currentframe())
        self.tb_alias.config(state='normal')

    def register(self, uiobserver):
        log.log_var(self, currentframe(), ("uiobserver", uiobserver))
        self.observers.append(uiobserver)
        
    def unregister(self, uiobserver):
        log.log_var(self, currentframe(), ("uiobserver", uiobserver))
        self.observers.pop(self.observers.index(uiobserver))

class BookOverviewFrame(tk.Frame, UIObservable):
    
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
       
        log.log_var(self, currentframe(), ("args", args), ("kwargs", kwargs))
        
        self.grid_columnconfigure(0, weight=1)
        self.next_button_row = 0
        self.root = root
        self.observers = []
        self.default_font = tkFont.Font(family='Helvetica', size=20, weight='bold')        
        self.lb_header = tk.Label(self, text="Bücher:", anchor=tk.W,)
        self.lb_header.grid(row=self.next_button_row, column=0, sticky=tk.W, padx=(5,5), pady=(5,5))
        self.lb_header['font'] = self.default_font
        
        btn_new_book = tk.Button(self, text="Neues Buch", command=self.new_book, bg='#f8f8f8')
        btn_new_book.grid(row=self.next_button_row, column=0, sticky=tk.E, padx=(5,5), pady=(5,5))
        btn_back = tk.Button(self, text="Zurück", command=self.back, bg='#f8f8f8')
        btn_back.grid(row=self.next_button_row, column=1, sticky=tk.E, padx=(5,5), pady=(5,5))
        
        self.book_buttons = []
        
        self.next_button_row += 1
  
    def back(self):
        log.log(self, currentframe())
        self.root.close_me(self)
    
    def new_book(self):
        log.log(self, currentframe())
        self.root.close_me(self, back=False)
    
    def raise_frame(self, abovethis):
        log.log_var(self, currentframe(), ("abovethis", abovethis))
        self.tkraise(aboveThis=abovethis)
        for observer in self.observers:
            observer.onDisplay(self)      

    def register(self, uiobserver):
        log.log_var(self, currentframe(), ("uiobserver", uiobserver))
        self.observers.append(uiobserver)
        
    def unregister(self, uiobserver):
        log.log_var(self, currentframe(), ("uiobserver", uiobserver))
        self.observers.pop(self.observers.index(uiobserver))
    
    def on_book_select(self, alias):
        log.log_var(self, currentframe(), ("alias", alias))
        self.root.close_me(self, back=False)
        for observer in self.observers:
            observer.onSelect(alias, PlotHoleType.BOOK)
    
    def remove_all_book_buttons(self):
        log.log(self, currentframe())        
        for btn in self.book_buttons:
            btn.destroy()            
        self.next_button_row = 1
        self.book_buttons.clear()
        
    def create_book_button(self, alias):   
        log.log_var(self, currentframe(), ("alias", alias))     
        btn = tk.Button(self, text=alias, command=lambda: self.on_book_select(alias))
        btn.grid(row=self.next_button_row, column=0, columnspan=2, sticky="NSEW", padx=(5,5), pady=(5,5))
        btn['font'] = tkFont.Font(family='Helvetica', size=20, weight='bold')
        
        self.next_button_row += 1        
        self.book_buttons.append(btn)
        
    def set_header(self, header):
        log.log_var(self, currentframe(), ("header", header))
        self.lb_header.config(text=header)