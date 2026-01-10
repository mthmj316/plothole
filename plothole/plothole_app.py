# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 15:09:28 2025

@author: mthoma
"""
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

    part_ui = seui.StoryElement(w, seui.create_part_conf(), PlotHoleType.PART)
    part_ui.grid(row=0, column=0, sticky="NSEW")
    part_overview_ui = seoui.StoryElementOverview(w, seoui.create_part_conf(), PlotHoleType.PART)
    part_overview_ui.grid(row=0, column=0, sticky="NSEW")   

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
    ui_frames_dict[PlotHoleType.PART.value] = part_ui
    
    ui_overview_frames_dict = {}
    ui_overview_frames_dict[PlotHoleType.STORY.value] = story_overview_ui
    ui_overview_frames_dict[PlotHoleType.BOOK.value] = book_overview_ui
    ui_overview_frames_dict[PlotHoleType.PART.value] = part_overview_ui
    
    navi = navi.NavigatorInstance(story_overview_ui, ui_frames_dict, ui_overview_frames_dict)
    story_ui.add_navigator(navi)
    story_overview_ui.add_navigator(navi)
    book_ui.add_navigator(navi)
    book_overview_ui.add_navigator(navi)
    part_ui.add_navigator(navi)
    part_overview_ui.add_navigator(navi)
    
    story_model = sem.StoryModel(story_ui, story_overview_ui, path_repros)    
    book_model = sem.BookModel(book_ui, book_overview_ui, path_repros)
    part_model = sem.PartModel(part_ui, part_overview_ui, path_repros)
    
    story_model.on_raised()
    
    menu_bar = tk.Menu(w)  
    file_menu = file_menu(menu_bar, w)
    menu_bar.add_cascade(label="File", menu=file_menu)
    w.config(menu=menu_bar)
    w.mainloop()
        
    log.log(None, currentframe(), "... plothole terminated!")