# -*- coding: utf-8 -*-
"""
Created on Tue Dec  9 14:36:56 2025

@author: mthoma
"""

import tkinter as tk

from tkinter import scrolledtext as stxt

PAD_X_RIGHT_BOLD = (5, 20)
PAD_X_LEFT_BOLD = (20, 5)

PAD_X_TOP_BOLD = (20, 5)
PAD_X_BOTTON_BOLD = (5,20)

class StoryFrame(tk.Frame):
    
    def __init__(self, root, *args, **kwargs):
       super().__init__(root, *args, **kwargs)
       # super().__init__(root, background="red", *args, **kwargs)
       
       self.grid_columnconfigure(1, weight=1)
       self.grid_rowconfigure(4, weight=1)
       
       lb_alias = tk.Label(self, text="Alias")
       lb_title = tk.Label(self, text="Titel")
       lb_accent = tk.Label(self, text="Tonfall")
       lb_msg = tk.Label(self, text="Botschaft")
       lb_basic_idea = tk.Label(self, text="Grundidee")
       
       tb_alias = tk.Entry(self)
       tb_title = tk.Entry(self)
       tb_accent = tk.Entry(self)
       sta_msg = stxt.ScrolledText(self, width=200, height=5)
       sta_basic_idea = stxt.ScrolledText(self, width=200, height=30)    
       
       lb_alias.grid(row=0, column=0, sticky="E", padx=PAD_X_LEFT_BOLD, pady=PAD_X_TOP_BOLD)       
       tb_alias.grid(row=0, column=1, columnspan=3, sticky="NSEW", padx=PAD_X_RIGHT_BOLD, pady=PAD_X_TOP_BOLD)
       
       lb_title.grid(row=1, column=0, sticky="E", padx=PAD_X_LEFT_BOLD, pady=5)
       tb_title.grid(row=1, column=1, columnspan=3, sticky="NSEW", padx=PAD_X_RIGHT_BOLD, pady=5)
       
       lb_accent.grid(row=2, column=0, sticky="NE", padx=PAD_X_LEFT_BOLD, pady=5)
       tb_accent.grid(row=2, column=1, columnspan=3, sticky="NSEW", padx=PAD_X_RIGHT_BOLD, pady=5)
       
       lb_msg.grid(row=3, column=0, sticky="NE", padx=PAD_X_LEFT_BOLD, pady=5)
       sta_msg.grid(row=3, column=1, columnspan=3, sticky="NSEW", padx=PAD_X_RIGHT_BOLD, pady=5)
       
       lb_basic_idea.grid(row=4, column=0, sticky="NE", padx=PAD_X_LEFT_BOLD, pady=PAD_X_BOTTON_BOLD)
       sta_basic_idea.grid(row=4, column=1, columnspan=3, sticky="NSEW", padx=PAD_X_RIGHT_BOLD, pady=5)
       
       btn_save = tk.Button(self, text="Speichern", command=self.save)
       btn_save.grid(row=5, column=1, sticky="NSEW", padx=PAD_X_RIGHT_BOLD, pady=PAD_X_BOTTON_BOLD)
       
      
    def save(self):
        pass
    
    def raise_frame(self):
        self.tkraise()