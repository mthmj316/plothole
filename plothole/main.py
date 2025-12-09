# -*- coding: utf-8 -*-
"""
Created on Mon Dec  8 20:38:34 2025

@author: mthoma
"""

import tkinter as tk
import story_frame as sframe

VERSION = "v0.1"


class Plothole(object):
    
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title(f"Plothole {VERSION}")
        
        self.menu_bar = tk.Menu(self.main_window)
        
        self.__file_menu__()
        
    def __file_menu__(self):
        self.file_menu = tk.Menu(self.menu_bar, tearoff=False)
        
        self.new_menu = tk.Menu(self.file_menu, tearoff=False)       
        self.file_menu.add_cascade(label="Story", menu=self.new_menu) 
        self.new_menu.add_command(label="New", command=self.new_story)        
        self.new_menu.add_command(label="Open", command=self.open_story)                  
        self.new_menu.add_command(label="Close", command=self.close_story) 
        self.new_menu.add_command(label="Delete", command=self.delete_story)
        
        self.file_menu.add_command(label="Save", command=lambda:self.save(False))        
        self.file_menu.add_command(label="Save + Exit", command=lambda:self.save(True))
        
        self.file_menu.add_separator()        
        self.file_menu.add_command(label="Exit", command=self.exit)
    
    def save(self, _exit):
        print("save story")
        
        if _exit:
            self.exit()
    
    def new_story(self):
        
        self.story_frame = sframe.StoryFrame(self.main_window) 
        self.story_frame.raise_frame()
        
        print("new story")
        
    def open_story(self):
        print("open story")
        
    def close_story(self):
        print("close story")
        
    def delete_story(self):
        print("delete story")
    
    def exit(self):
        self.main_window.destroy()
        
    def run(self):
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.main_window.config(menu=self.menu_bar)
        self.main_window.mainloop()


if __name__ == '__main__':
    w = Plothole()
    w.run()