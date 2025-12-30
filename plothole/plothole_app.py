# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 15:09:28 2025

@author: mthoma
"""
import plothole_main_window as win
import book_models
import story_models
import sys

from inspect import currentframe
import logger as log

TEST_PLOTHOLE_REPOS = "C:\\Users\\mthoma\\Documents\\PlotHole-Test_Repos"
PROD_PLOTHOLE_REPOS = "C:\\Users\\mthoma\\Documents\\PlotHole_Repos"

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
        
    w = win.PlotholeMainWindow()
    
    story_overview_ui = w.get_story_overview_ui()
    story_ui = w.get_story_ui()
    book_overview_ui = w.get_book_overview_ui()
    book_ui = w.get_book_ui()
    
    story_overview_model = story_models.StoryOverviewModel(story_overview_ui, path_repros)
    story_model = story_models.StoryModel(story_ui, path_repros)
    book_overview_model = book_models.BookOverviewModel(book_overview_ui, path_repros)
    book_ui_model = book_models.BookModel(book_ui, path_repros)
    
    # story_overview_ui.register(book_overview_model)
    # story_overview_ui.register(book_ui_model)
    story_overview_ui.register(story_model)
    book_overview_ui.register(book_ui_model)
    
    w.run()
    
    log.log(None, currentframe(), "... plothole terminated!")