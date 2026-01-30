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

VERSION = 0.4

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
    
    scene_ui = seui.SceneFrame(w)
    scene_ui.grid(row=0, column=0, sticky="NSEW")
    scene_overview_ui = seoui.SceneOverviewFrame(w)
    scene_overview_ui.grid(row=0, column=0, sticky="NSEW") 
    
    plothole_ui = seui.PlotholeFrame(w)
    plothole_ui.grid(row=0, column=0, sticky="NSEW")
    plothole_overview_ui = seoui.PlotholeOverviewFrame(w)
    plothole_overview_ui.grid(row=0, column=0, sticky="NSEW")   

    chapter_ui = seui.ChapterFrame(w)
    chapter_ui.grid(row=0, column=0, sticky="NSEW")
    chapter_overview_ui = seoui.ChapterOverviewFrame(w)
    chapter_overview_ui.grid(row=0, column=0, sticky="NSEW") 

    part_ui = seui.PartFrame(w)
    part_ui.grid(row=0, column=0, sticky="NSEW")
    part_overview_ui = seoui.PartOverviewFrame(w)
    part_overview_ui.grid(row=0, column=0, sticky="NSEW")   

    book_ui = seui.BookFrame(w)
    book_ui.grid(row=0, column=0, sticky="NSEW")
    book_overview_ui = seoui.BookOverviewFrame(w)
    book_overview_ui.grid(row=0, column=0, sticky="NSEW")    
    
    story_ui = seui.StoryFrame(w)
    story_ui.grid(row=0, column=0, sticky="NSEW")
    story_overview_ui = seoui.StoryOverviewFrame(w)
    story_overview_ui.grid(row=0, column=0, sticky="NSEW")
    
    ui_frames_dict = {}
    ui_frames_dict[PlotHoleType.STORY.value] = story_ui
    ui_frames_dict[PlotHoleType.BOOK.value] = book_ui
    ui_frames_dict[PlotHoleType.PART.value] = part_ui
    ui_frames_dict[PlotHoleType.CHAPTER.value] = chapter_ui
    ui_frames_dict[PlotHoleType.PLOTHOLE.value] = plothole_ui
    ui_frames_dict[PlotHoleType.SCENE.value] = scene_ui
    
    ui_overview_frames_dict = {}
    ui_overview_frames_dict[PlotHoleType.STORY.value] = story_overview_ui
    ui_overview_frames_dict[PlotHoleType.BOOK.value] = book_overview_ui
    ui_overview_frames_dict[PlotHoleType.PART.value] = part_overview_ui
    ui_overview_frames_dict[PlotHoleType.CHAPTER.value] = chapter_overview_ui
    ui_overview_frames_dict[PlotHoleType.PLOTHOLE.value] = plothole_overview_ui
    ui_overview_frames_dict[PlotHoleType.SCENE.value] = scene_overview_ui
    
    navi = navi.NavigatorInstance(story_overview_ui, ui_frames_dict, ui_overview_frames_dict)
    story_ui.add_navigator(navi)
    story_overview_ui.add_navigator(navi)
    book_ui.add_navigator(navi)
    book_overview_ui.add_navigator(navi)
    part_ui.add_navigator(navi)
    part_overview_ui.add_navigator(navi)    
    chapter_ui.add_navigator(navi)
    chapter_overview_ui.add_navigator(navi)
    plothole_ui.add_navigator(navi)
    plothole_overview_ui.add_navigator(navi)
    scene_ui.add_navigator(navi)
    scene_overview_ui.add_navigator(navi)
    
    story_model = sem.StoryModel(story_ui, story_overview_ui, path_repros)    
    book_model = sem.BookModel(book_ui, book_overview_ui, path_repros)
    part_model = sem.PartModel(part_ui, part_overview_ui, path_repros)
    chapter_model = sem.ChapterModel(chapter_ui, chapter_overview_ui, path_repros)
    plothole_model = sem.PlotholeModel(plothole_ui, plothole_overview_ui, path_repros)
    scene_model = sem.SceneModel(scene_ui, scene_overview_ui, path_repros)
    
    story_model.on_raised()
    
    menu_bar = tk.Menu(w)  
    file_menu = file_menu(menu_bar, w)
    menu_bar.add_cascade(label="File", menu=file_menu)
    w.config(menu=menu_bar)
    w.mainloop()
        
    log.log(None, currentframe(), "... plothole terminated!")