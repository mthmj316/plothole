# -*- coding: utf-8 -*-
"""
Created on Mon Dec  8 20:38:34 2025

@author: mthoma
"""

import tkinter as tk

VERSION = "v0.1"


class Plothole(object):
    
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title(f"Plothole {VERSION}")
        
        self.menu_bar = tk.Menu(self.main_window)
        
        self.__file_menu__()
        
    def __file_menu__(self):
        self.file_menu = tk.Menu(self.menu_bar)
        self.file_menu.add_command(label="Exit", command=self.exit)
        
    
    def exit(self):
        self.main_window.destroy()
        
    def mainloop(self):
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.main_window.config(menu=self.menu_bar)
        self.main_window.mainloop()


if __name__ == '__main__':
    w = Plothole()
    w.mainloop()