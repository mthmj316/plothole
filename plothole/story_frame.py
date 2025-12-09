# -*- coding: utf-8 -*-
"""
Created on Tue Dec  9 14:36:56 2025

@author: mthoma
"""

import tkinter as tk

from tkinter import scrolledtext as stxt

class StoryFrame(tk.Frame):
    
    def __init__(self, root, *args, **kwargs):
       super().__init__(root, *args, **kwargs)
       # super().__init__(root, background="red", *args, **kwargs)
       
       self.grid_columnconfigure(1, weight=1)
       self.grid_rowconfigure(2, weight=1)
       
       label = tk.Label(self, text="Alias")
       label.grid(row=0, column=0, sticky="E", padx=5, pady=5)
       label = tk.Label(self, text="Title")
       label.grid(row=1, column=0, sticky="E", padx=5, pady=5)
       label = tk.Label(self, text="Description")
       label.grid(row=2, column=0, sticky="NE", padx=5, pady=5)
       
       entry = tk.Entry(self)
       entry.grid(row=0, column=1, columnspan=3, sticky="NSEW", padx=5, pady=5)
       
       entry = tk.Entry(self)
       entry.grid(row=1, column=1, columnspan=3, sticky="NSEW", padx=5, pady=5)
       
       scrolledtext = stxt.ScrolledText(self, width=200, height=30)
       scrolledtext.grid(row=2, column=1, columnspan=3, sticky="NSEW", padx=5, pady=5)
       
    def raise_frame(self):
        self.tkraise()