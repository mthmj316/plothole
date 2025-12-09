# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 20:45:21 2025

@author: mthoma
"""

__POSSIBLE_MODES__ = ['r', 'w', 'a', 'r+', 'w+', 'a+', 'b']

def open_file(path, mode='r'):
    
    if path is None or len(path) == 0:
        raise Exception(f"path not set: '{path}'")
        
    if mode not in __POSSIBLE_MODES__:        
        raise Exception(f"invalid mode: '{mode}'")    
    
    f = open(path, mode)
    
    return f

def read_from_file(path, as_list=True):
    
    file = open_file(path, mode='r')
    
    try:
        if as_list:
            return file.readlines()
        else:
            return file.read()
    
    finally:
        file.close()
        
def write(path, content=""):
    if not isinstance(content, str):
        content = f"{content}"
    
    file = None
    
    try:         
        file = open(path, mode="w")
        file.write(content)
    finally:
        if file is not None:
            file.close()
            

def append_to_file(file, lines=[]):
    
    for line in lines:
        file.write("\n")
        file.write(line)
        
def read_line_number(file, line_number=0):
    
    lines = file.readlines()
    #print(lines)
    
    if line_number < 0 or line_number > len(lines) - 1:
        raise Exception(f"invalid line number '{line_number}'")
    else:
        return lines[line_number]
    
def insert_to_file(file, text, pos, close_file=True):
    
    if not isinstance(text, str):
        text = f"{text}"
    
    try:        
        # Cursor to insert position 
        file.seek(pos)
        # write to file
        file.write(text)
    finally:
        if close_file:
            file.close()