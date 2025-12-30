# -*- coding: utf-8 -*-
"""
Created on Mon Dec  8 20:38:34 2025

@author: mthoma
"""

import tkinter as tk
import story_ui
import book_ui
from abc import ABC
from abc import abstractclassmethod
from observers import UIObservable
from inspect import currentframe
import logger as log

VERSION = "v0.1"

class MainWindow(ABC):
    @abstractclassmethod
    def close_me(self, frame, back=True):
        """
        If called the passed frame is moved down the statck

        Parameters
        ----------
        frame : tk.Frame
            The frame which is currently displayed and shall be moved down the stack..
        back : bool, optional
            If there are two possible navigation, than back
            decides which frame is to be displayed next.
            back==True back to the former frame back==False to the next frame.
            The default is True.

        Returns
        -------
        None.

        """      
        
class PlotholeMainWindow(tk.Tk, MainWindow, UIObservable):
    
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        log.log_var(self, currentframe(), ("args", args), ("kwargs", kwargs))
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.title(f"Plothole {VERSION}")
        self.geometry("1250x750+300+100")       
        self.menu_bar = tk.Menu(self)        
        self.__file_menu__()            
        
        self.story_frame = story_ui.StoryFrame(self)        
        self.story_frame.grid(row=0, column=0, sticky="NSEW")
        
        self.book_frame = book_ui.BookFrame(self)        
        self.book_frame.grid(row=0, column=0, sticky="NSEW")
        
        self.book_overview_frame = book_ui.BookOverviewFrame(self)       
        self.book_overview_frame.grid(row=0, column=0, sticky="NSEW")
        
        self.story_overview_frame = story_ui.StoryOverview(self)       
        self.story_overview_frame.grid(row=0, column=0, sticky="NSEW")
        self.observers = []
        
    def close_me(self, frame, back=True):
        log.log_var(self, currentframe(), ("frame", frame), ("back", back))
        if frame == self.story_frame:
            self.story_overview_frame.raise_frame(frame)
        elif frame == self.story_overview_frame:
            self.book_overview_frame.raise_frame(frame)
        elif frame == self.book_overview_frame:
            if back:
                self.story_overview_frame.raise_frame(frame)
            else:
                self.book_frame.raise_frame(frame)
        elif frame == self.book_frame:
            self.book_overview_frame.raise_frame(frame)

    def get_book_ui(self):
        log.log(self, currentframe())
        return self.book_frame
    
    def get_story_ui(self):
        log.log(self, currentframe())
        return self.story_frame
    
    def get_story_overview_ui(self):
        log.log(self, currentframe())
        return self.story_overview_frame
    
    def get_book_overview_ui(self):
        log.log(self, currentframe())
        return self.book_overview_frame
        
    def __file_menu__(self):
        log.log(self, currentframe())
        self.file_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.new_menu = tk.Menu(self.file_menu, tearoff=False)       
        self.file_menu.add_command(label="Story", command=self.open_story)
        self.file_menu.add_separator()        
        self.file_menu.add_command(label="Exit", command=self.exit)
    
    def save(self, _exit):
        log.log_var(self, currentframe(), ("_exit", _exit))
        if _exit:
            self.exit()
    
    def open_story(self):
        log.log(self, currentframe())
        self.story_frame.raise_frame(self.story_overview_frame)
    
    def exit(self):
        log.log(self, currentframe())
        self.destroy()
        
    def run(self):
        log.log(self, currentframe())
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.config(menu=self.menu_bar)
        self.mainloop()

    def register(self, uiobserver):
        """
        register an observer of type Observer

        Returns
        -------
        None.

        """
        log.log_var(self, currentframe(), ("uiobserver", uiobserver))
        self.observers.append(uiobserver)
        
    def unregister(self, uiobserver):
        """
        register an observer of type Observer

        Returns
        -------
        None.

        """
        log.log_var(self, currentframe(), ("uiobserver", uiobserver))
        self.observers.pop(self.observers.index(uiobserver))
    
    