# -*- coding: utf-8 -*-
"""
Created on Mon Dec  8 20:38:34 2025

@author: mthoma
"""

import tkinter as tk
import story_frame as sframe

#from tkinter import font

VERSION = "v0.1"



class PlotholeMainWindow(object):
    
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.grid_columnconfigure(0, weight=1)
        self.main_window.grid_rowconfigure(0, weight=1)
        self.main_window.title(f"Plothole {VERSION}")
        self.main_window.geometry("1250x750+300+100")
        
        # self.main_window.option_add("*Font", "TimesNewRoman 10"
        #print(font.families())
        
        self.menu_bar = tk.Menu(self.main_window)        
        self.__file_menu__()            
        self.story_frame = sframe.StoryFrame(self.main_window)
        
    
    def create_story_button(self, alias):
        
        btn = tk.Button(self.main_window, text=alias, command=lambda: self.onStorySelect(alias))
        btn.config(width=20, height=20)
        btn.pack(side=tk.LEFT, anchor=tk.NW, padx=(5,5), pady=(5,5))
        
    def onStorySelect(self, alias):
        print(alias)
    
    def get_story_ui(self):
        return self.story_frame
        
        
    def __file_menu__(self):
        self.file_menu = tk.Menu(self.menu_bar, tearoff=False)
        
        self.new_menu = tk.Menu(self.file_menu, tearoff=False)       
        self.file_menu.add_command(label="Story", command=self.open_story)
        
        # self.file_menu.add_command(label="Save", command=lambda:self.save(False))        
        # self.file_menu.add_command(label="Save + Exit", command=lambda:self.save(True))
        
        self.file_menu.add_separator()        
        self.file_menu.add_command(label="Exit", command=self.exit)
    
    def save(self, _exit):
        print("save story")
        
        if _exit:
            self.exit()
    
    def open_story(self):
        self.story_frame.pack()
        #.grid(row=0, column=0, sticky="NSEW")
        self.story_frame.raise_frame()

    
    def exit(self):
        self.main_window.destroy()
        
    def run(self):
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.main_window.config(menu=self.menu_bar)
        self.main_window.mainloop()

    
    