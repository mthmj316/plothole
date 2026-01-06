# -*- coding: utf-8 -*-
"""
Created on Mon Dec  8 20:26:05 2025

@author: mthoma
"""
import file_access as fa
import helpers as hlp
import pathlib
import logger as log
from inspect import currentframe

from plothole_types import FILE_EXTENSIONS_DUMP as fed
from plothole_types import PlotHoleType

def delete(base_dir, alias, plothole_type):
    log.log_var(None, currentframe(), ('base_dir',base_dir), ('alias',alias), ('plothole_type',plothole_type))    
    if plothole_type == PlotHoleType.STORY:
        delete_story(base_dir, alias)
        log.log_var(None, currentframe(), ('return',"void"))
    else:
        path = hlp.get_path_by_alias(base_dir, alias)
        dump_path = dump_file_extension(path, plothole_type.value)
        fa.move(path, dump_path)
    log.log_var(None, currentframe(), ('return',"void"))

def delete_part(base_dir, alias):
    log.log_var(None, currentframe(), ('base_dir',base_dir), ('alias',alias))
    part_path = hlp.get_part_path_by_alias(base_dir, alias)
    part_dump_path = dump_file_extension(part_path, 'part')
    fa.move(part_path, part_dump_path)
    log.log_var(None, currentframe(), ('return',"void"))

def delete_book(base_dir, alias):
    log.log_var(None, currentframe(), ('base_dir',base_dir), ('alias',alias))
    book_path = hlp.get_book_path_by_alias(base_dir, alias)
    book_dump_path = dump_file_extension(book_path, 'book')
    fa.move(book_path, book_dump_path)
    log.log_var(None, currentframe(), ('return',"void"))

def delete_story(base_dir, alias):
    log.log_var(None, currentframe(), ('base_dir',base_dir), ('alias',alias))
    dump_path = init_dump(base_dir)
    story_path = hlp.get_story_path_by_alias(base_dir, alias)
    story_parent_path = str(pathlib.Path(story_path).parent)
    story_dump_parent_path = f"{story_parent_path.replace(base_dir, dump_path)}_{hlp.get_current_time_stamp()}"    
    fa.move(story_parent_path, story_dump_parent_path)
    dump_story_content(story_dump_parent_path)
    log.log_var(None, currentframe(), ('return',"void"))

def dump_story_content(story_path):
    log.log_var(None, currentframe(), ('story_path',story_path))
    for key in fed:
        for path in hlp.get_all_pathes(story_path, key):
            new_path = dump_file_extension(path,key)
            fa.move(path, new_path)
    
    log.log_var(None, currentframe(), ('return',"void"))

def dump_file_extension(filename, extension):  
    log.log_var(None, currentframe(), ('filename',filename), ('extension',extension))  
    p = pathlib.Path(filename)    
    ret_val = f"{p.parent.as_posix()}/{pathlib.Path(filename).stem}.{fed.get(extension)}"
    log.log_var(None, currentframe(), ('return',ret_val))
    return ret_val
    
def init_dump(base_dir):
    log.log_var(None, currentframe(), ('base_dir',base_dir))
    dump_path = f"{base_dir}\story_dump"    
    fa.create_dir(dump_path)
    log.log_var(None, currentframe(), ('return',dump_path))
    return dump_path
    
if __name__ == '__main__':
    alias = 'Mein Geschichte'
    base_dir = 'C:\\Users\\mthoma\\Documents\\PlotHole-Test_Repos'
    delete_story(base_dir, alias)
    