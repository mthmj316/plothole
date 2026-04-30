# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 09:04:43 2026

@author: mthoma
"""

from inspect import currentframe
import logger as log
import helpers as hlp

import pathlib
import plothole_types as pt
from story_element_ui import __SEControls__ as sec


def desolve_by_path(path, return_path_only=False):
    
    log.log_var(None, currentframe(), ('path',path), ('return_path_only',return_path_only))
    
    relations = {}
    
    relations['this'] = hlp.get(path, as_dict=True)
    relations['this_ptype'] = __get_ptype_by_path(path)
    relations['this_path'] = path
    
    while True:
        
        parent_ptype = __get_parent_ptype_by_path(path)
        
        if parent_ptype is None:
            break
        
        parent_obj = desolve_parent_by_path(path)
        log.log_var(None, currentframe(), ('parent_obj',parent_obj))
        
        parent_alias = parent_obj.get(sec.ALIAS)
        log.log_var(None, currentframe(), ('parent_alias',parent_alias))
        
        parent_path = hlp.get_path_for_alias(__get_parent_path(path), parent_alias, extension=parent_ptype)
        log.log_var(None, currentframe(), ('parent_path',parent_path))
        
        parent_obj['path'] = parent_path
        parent_obj['pytpe'] = parent_ptype
        relations[parent_ptype] = parent_obj        
        
        path = parent_path
        
    log.log_var(None, currentframe(), ("relations", relations))

    return relations    


def __get_ptype_by_path(path):

    log.log_var(None, currentframe(), ("path", path))
    
    ptype = pathlib.Path(path).suffix.split(".")[-1]

    log.log_var(None, currentframe(), ("ptype", ptype))

    return ptype    

def __get_parent_path(child_path):

    log.log_var(None, currentframe(), ("child_path", child_path))
    
    parent_path = pathlib.Path(pathlib.Path(child_path).parent).parent
   
    log.log_var(None, currentframe(), ("parent_path", parent_path)) 
    
    return parent_path
    
    

def desolve_parent_by_path(path, return_path_only=False):
    
    log.log_var(None, currentframe(), ('path',path), ('return_path_only',return_path_only))
    
    # folder of the story element parent: part -> book
    parent_folder = __get_parent_path(path)
    log.log_var(None, currentframe(), ("parent_folder", parent_folder))
    
    parent_ptype = __get_parent_ptype_by_path(path)
    log.log_var(None, currentframe(), ("parent_ptype", parent_ptype))
    
    parent_se = None
    
    if parent_ptype is not None:
        parent_se = hlp.get_all(parent_folder, parent_ptype, as_dict=True)[0]
    
    log.log_var(None, currentframe(), ("parent_se", parent_se))
    
    return parent_se    
    

def desolve_children_by_path(path, return_path_only=False):
    
    log.log_var(None, currentframe(), ('path',path), ('return_path_only',return_path_only))
    
    folder = pathlib.Path(path).parent
    log.log_var(None, currentframe(), ("folder", folder))

    child_ptype = __get_child_ptype_by_path(path)
    log.log_var(None, currentframe(), ("child_ptype", child_ptype))
    
    children_se = None
    
    if child_ptype is not None:
        children_se = hlp.get_all(folder, child_ptype, as_dict=True)
    
    log.log_var(None, currentframe(), ("children_se", children_se))
    
    return children_se

def __get_parent_ptype_by_path(path):

    log.log_var(None, currentframe(), ("path", path))
    
    ptype = pt.PARENT_PLOTHOLE_TYPE.get(__get_ptype_by_path(path))

    log.log_var(None, currentframe(), ("ptype", ptype))

    return ptype   

def __get_child_ptype_by_path(path):

    log.log_var(None, currentframe(), ("path", path))
    
    ptype = pt.CHILD_PLOTHOLE_TYPE.get(__get_ptype_by_path(path))

    log.log_var(None, currentframe(), ("ptype", ptype))

    return ptype   

if __name__ == '__main__':
    
    log.ENABLE_LOGGING = True
    log.TRACE_ONLY = False
    
    test_path = "C:\\Users\\mthoma\\Documents\\PlotHole-Test_Repos\\LearningMotionComic\\TheSnakeAndTheMouse\\TheSnakeAndTheMouse\\TheSnakeAndTheMouse\\TheSnakeAndTheMouse.chapter"
    
    result_desolve_parent_by_path = desolve_parent_by_path(test_path)   
    log.log_var(None, currentframe(), ("result_desolve_parent_by_path", result_desolve_parent_by_path))
    
    result_desolve_children_by_path = desolve_children_by_path(test_path)   
    log.log_var(None, currentframe(), ("result_desolve_children_by_path", result_desolve_children_by_path))   
    
    result_relations = desolve_by_path(test_path)   
    log.log_var(None, currentframe(), ("result_relations", result_relations))    
    