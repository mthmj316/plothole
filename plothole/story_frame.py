# -*- coding: utf-8 -*-
"""
Created on Tue Dec  9 14:36:56 2025

@author: mthoma
"""

import tkinter as tk

class StoryFrame(tk.Frame):
    
    def __init__(self, root, *args, **kwargs):
        
       super().__init__(root, *args, **kwargs)
       
       label = tk.Label(self, text="Alias")
       label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
       
       label = tk.Label(self, text="Title")
       label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
       
       label = tk.Label(self, text="Description")
       label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
       
       ... #do other initialisation
       self.grid() #or pack()
       
    def raise_frame(self):
        self.tkraise()