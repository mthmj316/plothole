# -*- coding: utf-8 -*-
"""
Created on Mon Dec  8 20:38:34 2025

@author: mthoma
"""

import tkinter as tk
import story_frame as sframe
import story_overview_frame as soFrame
from abc import ABC
from abc import abstractclassmethod
from tkinter import font as tkFont


VERSION = "v0.1"

class MainWindow(ABC):
    @abstractclassmethod
    def close_me(self, frame):
        """
        If called the passed frame is moved down the statck

        Parameters
        ----------
        frame : tk.Frame
            The frame which is currently displayed and shall be moved down the stack.

        Returns
        -------
        None.

        """
        
    

class PlotholeMainWindow(tk.Tk, MainWindow):
    
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        
        # self.main_window = tk.Tk()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.title(f"Plothole {VERSION}")
        self.geometry("1250x750+300+100")
        
        # self.main_window.option_add("*Font", "TimesNewRoman 10"
        #print(font.families())
        
        self.menu_bar = tk.Menu(self)        
        self.__file_menu__()            
        self.story_frame = sframe.StoryFrame(self)        
        self.story_frame.grid(row=0, column=0, sticky="NSEW")
        
        self.story_overview_frame = soFrame.StoryOverview(self)       
        self.story_overview_frame.grid(row=0, column=0, sticky="NSEW")
        
        self.next_button_row = 0
        
    
    def close_me(self, frame):
        self.story_overview_frame.raise_frame(frame)
    
    def create_story_button(self, alias):
        
        btn = tk.Button(self.story_overview_frame, text=alias, command=lambda: self.onStorySelect(alias))
        # btn.config(height=5)
        btn.grid(row=self.next_button_row, column=0, sticky="NSEW", padx=(5,5), pady=(5,5))
        btn['font'] = tkFont.Font(family='Helvetica', size=20, weight='bold')
        
        self.next_button_row += 1
        
    def onStorySelect(self, alias):
        print(alias)
    
    def get_story_ui(self):
        return self.story_frame
    
    def get_story_overview_ui(self):
        return self.story_overview_frame
        
        
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
        self.story_frame.raise_frame(self.story_overview_frame)

    
    def exit(self):
        self.destroy()
        
    def run(self):
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.config(menu=self.menu_bar)
        self.mainloop()

    
    