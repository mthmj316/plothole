# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 15:09:28 2025

@author: mthoma
"""
import plothole_main_window as win
import models
import sys

TEST_PLOTHOLE_REPOS = "C:/Users/mthoma/Documents/PlotHole-Test_Repos"
PROD_PLOTHOLE_REPOS = "C:/Users/mthoma/Documents/PlotHole_Repos"

if __name__ == '__main__':
    
    path_repros = TEST_PLOTHOLE_REPOS
    
    for o in sys.argv:        
        if o.startswith("path=prod"):
            path_repros = PROD_PLOTHOLE_REPOS        
        
    w = win.PlotholeMainWindow()
    
    story_overview_ui = w.get_story_overview_ui()
    story_overview_model = models.StoryOverviewModel(w, path_repros)
    
    
    story_ui = w.get_story_ui()
    story_model = models.StoryModel(story_ui, path_repros) 
    
    
    w.run()