# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 20:45:21 2025

@author: mthoma
"""
from pathlib import Path
import shutil
import logger as log
from inspect import currentframe

__POSSIBLE_MODES__ = ['r', 'w', 'a', 'r+', 'w+', 'a+', 'b']

from glob import glob

def move(old, new):
    log.log_var(None, currentframe(), ('old',old), ('new',new))
    Path(old).rename(new)
    log.log_var(None, currentframe(), ('return',"void"))

def find_files(_filter, recursive):
    log.log_var(None, currentframe(), ('_filter',_filter), ('recursive',recursive))
    files = []
    for filename in glob(_filter, recursive=recursive):
        files.append(filename)
    log.log_var(None, currentframe(), ('return',files))    
    return files

def delete_folder(path):
    log.log_var(None, currentframe(), ('path',path))
    dirpath = Path(path)    
    if dirpath.exists() and dirpath.is_dir():
        shutil.rmtree(dirpath)
    log.log_var(None, currentframe(), ('return',"void"))  
 

def exists(path):    
    log.log_var(None, currentframe(), ('path',path))
    file = Path(path)
    log.log_var(None, currentframe(), ('return',file))      
    return file.is_file()

def create_dir(path):
    log.log_var(None, currentframe(), ('path',path))    
    Path(path).mkdir(parents=True, exist_ok=True)
    log.log_var(None, currentframe(), ('return',"void"))  

def open_file(path, mode='r'):
    log.log_var(None, currentframe(), ('path',path), ('mode',mode))    
    if path is None or len(path) == 0:
        raise Exception(f"path not set: '{path}'")
        
    if mode not in __POSSIBLE_MODES__:        
        raise Exception(f"invalid mode: '{mode}'")    
    
    f = open(path, mode)
    log.log_var(None, currentframe(), ('return',f))        
    return f

def read_from_file(path, as_list=True):
    log.log_var(None, currentframe(), ('path',path), ('as_list',as_list))     
    file = open_file(path, mode='r')    
    try:
        if as_list:
            return file.readlines()
        else:
            return file.read()
    finally:
        file.close()
    log.log_var(None, currentframe(), ('return',"void")) 
        
def write(path, content=""):
    log.log_var(None, currentframe(), ('path',path), ('content',content))    
    if not isinstance(content, str):
        content = f"{content}"    
    file = None    
    try:         
        file = open(path, mode="w")
        file.write(content)
    finally:
        if file is not None:
            file.close()    
    log.log_var(None, currentframe(), ('return',"void"))         

def append_to_file(file, lines=[]):
    log.log_var(None, currentframe(), ('file',file), ('lines',lines))       
    for line in lines:
        file.write("\n")
        file.write(line)
    log.log_var(None, currentframe(), ('return',"void"))    
        
def read_line_number(file, line_number=0):
    log.log_var(None, currentframe(), ('file',file), ('line_number',line_number))    
    lines = file.readlines()
    if line_number < 0 or line_number > len(lines) - 1:
        raise Exception(f"invalid line number '{line_number}'")
    else:
        return lines[line_number]
    log.log_var(None, currentframe(), ('return',"void")) 
    
def insert_to_file(file, text, pos, close_file=True):
    log.log_var(None, currentframe(), ('file',file), ('text',text),('pos',pos),('close_file',close_file)) 
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
    log.log_var(None, currentframe(), ('return',"void")) 