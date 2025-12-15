# -*- coding: utf-8 -*-
"""
Created on Tue Dec  9 14:36:56 2025

@author: mthoma
"""

import tkinter as tk
from observers import UIObservable

from tkinter import scrolledtext as stxt
from tkinter.filedialog import askopenfilename
from tkinter import StringVar
from tkinter import messagebox as mb

PAD_X_RIGHT_BOLD = (5, 20)
PAD_X_LEFT_BOLD = (20, 5)

PAD_X_TOP_BOLD = (20, 5)
PAD_X_BOTTON_BOLD = (5,20)

COLSPAN_RIGHT = 5

BUTTON_WIDTH = 20

class StoryFrame(tk.Frame, UIObservable):
    
    def __init__(self, root, *args, **kwargs):
        
       super().__init__(root, *args, **kwargs)
       # super().__init__(root, background="red", *args, **kwargs)
       self.root = root
       self.observers = []
       
       self.grid_columnconfigure(1, weight=1)
       self.grid_rowconfigure(4, weight=1)
       
       lb_alias = tk.Label(self, text="Alias")
       lb_title = tk.Label(self, text="Titel")
       lb_accent = tk.Label(self, text="Tonfall")       
       lb_genre = tk.Label(self, text="Genre")
       lb_msg = tk.Label(self, text="Botschaft")
       lb_basic_idea = tk.Label(self, text="Grundidee")
       
       self.tb_alias_value = StringVar()
       self.tb_alias = tk.Entry(self, textvariable=self.tb_alias_value)
       
       self.tb_title_value = StringVar()
       tb_title = tk.Entry(self, textvariable=self.tb_title_value)
       
       self.tb_accent_value = StringVar()
       tb_accent = tk.Entry(self, textvariable=self.tb_accent_value)
       
       self.tb_genre_value = StringVar()
       tb_genre = tk.Entry(self, textvariable=self.tb_genre_value)
       
       self.sta_msg = stxt.ScrolledText(self, width=200, height=5)
       
       self.sta_basic_idea = stxt.ScrolledText(self, width=200, height=30)    
       
       lb_alias.grid(row=0, column=0, sticky="E", padx=PAD_X_LEFT_BOLD, pady=5)       
       self.tb_alias.grid(row=0, column=1, columnspan=COLSPAN_RIGHT, sticky="NSEW", padx=PAD_X_RIGHT_BOLD, pady=5)
       
       lb_title.grid(row=1, column=0, sticky="E", padx=PAD_X_LEFT_BOLD, pady=5)
       tb_title.grid(row=1, column=1, columnspan=COLSPAN_RIGHT, sticky="NSEW", padx=PAD_X_RIGHT_BOLD, pady=5)
       
       lb_accent.grid(row=2, column=0, sticky="NE", padx=PAD_X_LEFT_BOLD, pady=5)
       tb_accent.grid(row=2, column=1, columnspan=COLSPAN_RIGHT, sticky="NSEW", padx=PAD_X_RIGHT_BOLD, pady=5)
       
       lb_genre.grid(row=3, column=0, sticky="NE", padx=PAD_X_LEFT_BOLD, pady=5)
       tb_genre.grid(row=3, column=1, columnspan=COLSPAN_RIGHT, sticky="NSEW", padx=PAD_X_RIGHT_BOLD, pady=5)
       
       lb_msg.grid(row=4, column=0, sticky="NE", padx=PAD_X_LEFT_BOLD, pady=5)
       self.sta_msg.grid(row=4, column=1, columnspan=COLSPAN_RIGHT, sticky="NSEW", padx=PAD_X_RIGHT_BOLD, pady=5)
       
       lb_basic_idea.grid(row=5, column=0, sticky="NE", padx=PAD_X_LEFT_BOLD, pady=PAD_X_BOTTON_BOLD)
       self.sta_basic_idea.grid(row=5, column=1, columnspan=COLSPAN_RIGHT, sticky="NSEW", padx=PAD_X_RIGHT_BOLD, pady=5)
       
       btn_frame = tk.Frame(self)
       btn_frame.grid(row=6, column=1, sticky="NSEW", padx=PAD_X_RIGHT_BOLD, pady=5)
       
       btn_open = tk.Button(btn_frame, text="Öffnen", command=self._open)
       btn_open.config(width=BUTTON_WIDTH)
       btn_open.grid(row=0, column=1, sticky="NSEW", padx=(0,1), pady=5)
      
       btn_save = tk.Button(btn_frame, text="Speichern", command=self.save)
       btn_save.config(width=BUTTON_WIDTH)
       btn_save.grid(row=0, column=2, sticky="NSEW", padx=(1,1), pady=5)
       
       btn_revert = tk.Button(btn_frame, text="Zurücksetzen", command=self.revert)
       btn_revert.config(width=BUTTON_WIDTH)
       btn_revert.grid(row=0, column=3, sticky="NSEW", padx=(1,1), pady=5)
       
       btn_delete = tk.Button(btn_frame, text="Löschen", command=self.delete)
       btn_delete.config(width=BUTTON_WIDTH)
       btn_delete.grid(row=0, column=4, sticky="NSEW", padx=(1,0), pady=5)
       
       btn_close = tk.Button(btn_frame, text="Schließen", command=self.close)
       btn_close.config(width=BUTTON_WIDTH)
       btn_close.grid(row=0, column=5, sticky="NSEW", padx=(1,0), pady=5)
    
    def close(self):
        for observer in self.observers:
            observer.onClose()
        
        self.root.close_me(self)
    
    def set_base_dir(self, base_dir):
        self.base_dir = base_dir
     
    def register(self, uiobserver):
        self.observers.append(uiobserver)
    
    def unregister(self, uiobserver):
        self.observers.pop(self.observers.index(uiobserver))

    def _open(self):
       # Tk().withdraw()
       self.story_file = askopenfilename(initialdir=self.base_dir)
       for observer in self.observers:
           observer.onLoad(self.story_file)
        
    def save(self):
        for observer in self.observers:
            observer.onSave()

    def update(self):
        for observer in self.observers:
            observer.onUpdate()
    
    def delete(self):
        for observer in self.observers:
            observer.onDelete()

    def revert(self):
        for observer in self.observers:
            observer.onRevert()
    
    def raise_frame(self, abovethis):
        self.tkraise(aboveThis=abovethis)
        
    def get_alias(self):
        return self.tb_alias_value.get()
    
    def set_alias(self, alias):
        self.tb_alias_value.set(alias)
    
    def get_title(self):
        return self.tb_title_value.get()
    
    def set_title(self, title):
        self.tb_title_value.set(title)
    
    def get_accent(self):
        return self.tb_accent_value.get()
    
    def set_accent(self, accent):
        self.tb_accent_value.set(accent)
  
    def get_genre(self):
        return self.tb_genre_value.get()
    
    def set_genre(self, genre):
            self.tb_genre_value.set(genre)
    
    def get_message(self):
        return self.sta_msg.get("1.0", tk.END)
    
    def set_message(self, msg):
        self.sta_msg.delete('1.0', tk.END)
        self.sta_msg.insert(tk.INSERT, msg)
    
    def get_basic_idea(self):
        return self.sta_basic_idea.get("1.0", tk.END)
    
    def set_basic_idea(self, basic_idea):
        self.sta_basic_idea.delete('1.0', tk.END)
        self.sta_basic_idea.insert(tk.INSERT, basic_idea)
    
    def raise_error(self, error):
        mb.showerror("Fehler", error)
        
    def disable_alias(self):
        self.tb_alias.config(state='disabled')
        
    def enable_alias(self):
        self.tb_alias.config(state='normal')