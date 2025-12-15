# -*- coding: utf-8 -*-

import tkinter as tk
from observers import UIObservable

class StoryOverview(tk.Frame, UIObservable):
    
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.grid_columnconfigure(0, weight=1)
    
    def raise_frame(self, abovethis):
        self.tkraise(aboveThis=abovethis)

    def register(self, uiobserver):
        """
        register an observer of type Observer

        Returns
        -------
        None.

        """
        
    def unregister(self, uiobserver):
        """
        register an observer of type Observer

        Returns
        -------
        None.
        """
