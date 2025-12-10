# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 15:09:28 2025

@author: mthoma
"""
import plothole_main_window as win
import story_frame as sf
import models

if __name__ == '__main__':
    
    w = win.PlotholeMainWindow()
    
    story_ui = w.get_story_ui()
    story_model = models.StoryModel(story_ui, "C:/Users/mthoma/Documents/PlotHole-Test_Repos") 
    
    
    w.run()