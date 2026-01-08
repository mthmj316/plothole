# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 15:09:28 2025

@author: mthoma
"""
import book_models
import story_models
import sys
import tkinter as tk

from inspect import currentframe
import logger as log

import story_element_ui as seui
import story_element_model as sem

import story_element_overview_ui as seoui

import navigator as navi

from plothole_types import PlotHoleType

TEST_PLOTHOLE_REPOS = "C:\\Users\\mthoma\\Documents\\PlotHole-Test_Repos"
PROD_PLOTHOLE_REPOS = "C:\\Users\\mthoma\\Documents\\PlotHole_Repos"

VERSION = 0.3

def _exit(win):
    log.log_var(None, currentframe(), ('win',win))
    win.destroy()

def file_menu(menu_bar, win):
    log.log(None, currentframe())
    file_menu = tk.Menu(menu_bar, tearoff=False)
    file_menu.add_command(label="Exit", command=lambda: _exit(win))
    return file_menu

if __name__ == '__main__':
    
    path_repros = TEST_PLOTHOLE_REPOS
    for o in sys.argv:        
        if o == "path=prod":
            path_repros = PROD_PLOTHOLE_REPOS  
        elif o == "logging=on":
            log.ENABLE_LOGGING=True
        elif o == "trace_only=off":
            log.TRACE_ONLY = False
    
    log.log(None, currentframe(), "plothole started ...")
    
    if path_repros == TEST_PLOTHOLE_REPOS:
        log.ENABLE_LOGGING=True
        log.TRACE_ONLY = False
    
    log.log_var(None, currentframe(), ('path_repros',path_repros))
    
    w = tk.Tk()
    w.title(f"Plothole v{VERSION}")
    w.geometry("1250x750+300+100")
    w.grid_columnconfigure(0, weight=1)
    w.grid_rowconfigure(0, weight=1) 

    book_ui = seui.StoryElement(w, seui.create_book_conf(), PlotHoleType.BOOK)
    book_ui.grid(row=0, column=0, sticky="NSEW")
    book_overview_ui = seoui.StoryElementOverview(w, seoui.create_book_conf(), PlotHoleType.BOOK)
    book_overview_ui.grid(row=0, column=0, sticky="NSEW")    
    
    story_ui = seui.StoryElement(w, seui.create_story_conf(), PlotHoleType.STORY)
    story_ui.grid(row=0, column=0, sticky="NSEW")
    story_overview_ui = seoui.StoryElementOverview(w, seoui.create_story_conf(), PlotHoleType.STORY)
    story_overview_ui.grid(row=0, column=0, sticky="NSEW")
    
    ui_frames_dict = {}
    ui_frames_dict[PlotHoleType.STORY.value] = story_ui
    ui_frames_dict[PlotHoleType.BOOK.value] = book_ui
    
    ui_overview_frames_dict = {}
    ui_overview_frames_dict[PlotHoleType.STORY.value] = story_overview_ui
    ui_overview_frames_dict[PlotHoleType.BOOK.value] = book_overview_ui
    
    navi = navi.NavigatorInstance(story_overview_ui, ui_frames_dict, ui_overview_frames_dict)
    story_ui.add_navigator(navi)
    story_overview_ui.add_navigator(navi)
    book_ui.add_navigator(navi)
    book_overview_ui.add_navigator(navi)
    
    story_model = sem.StoryModel(story_ui, story_overview_ui, path_repros)    
    book_model = sem.BookModel(book_ui, book_overview_ui, path_repros)
    story_overview_ui.register(book_model)
    
    story_model.on_open(None)
    
    menu_bar = tk.Menu(w)  
    file_menu = file_menu(menu_bar, w)
    menu_bar.add_cascade(label="File", menu=file_menu)
    w.config(menu=menu_bar)
    w.mainloop()
        
    # w = win.PlotholeMainWindow()
    
    # story_overview_ui = w.get_story_overview_ui()
    # story_ui = w.get_story_ui()
    # book_overview_ui = w.get_book_overview_ui()
    # book_ui = w.get_book_ui()
    
    # story_overview_model = story_models.StoryOverviewModel(story_overview_ui, path_repros)
    # story_model = story_models.StoryModel(story_ui, path_repros)
    # book_overview_model = book_models.BookOverviewModel(book_overview_ui, path_repros)
    # book_ui_model = book_models.BookModel(book_ui, path_repros)
    
    # story_overview_ui.register(book_overview_model)
    # story_overview_ui.register(book_ui_model)
    # story_overview_ui.register(story_model)
    # book_overview_ui.register(book_ui_model)
    
    # w.run()
    
    log.log(None, currentframe(), "... plothole terminated!")