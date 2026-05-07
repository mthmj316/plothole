# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 09:04:43 2026

@author: mthoma
"""

from inspect import currentframe
import logger as log
import helpers as hlp

import json
import file_access as fa

import pathlib
import plothole_types as pt
from story_element_ui import __SEControls__ as sec


def desolve(base):
    log.log_var(None, currentframe(), ('base',base))
    for story in hlp.get_all_stories(base, as_dict=True):
        story['ptype'] = pt.PlotHoleType.STORY.value
        story['path'] = hlp.get_path_for_alias(base, story.get(sec.ALIAS))
        
        log.log_var(None, currentframe(), ('story',story))
        
        desolve_children(story)
        
        data = json.dumps(story, sort_keys=False, indent=2)
        fa.write(story.get('path'), data)

def desolve_children(story_element):
   
    child_ptype = pt.CHILD_PLOTHOLE_TYPE.get(story_element.get('ptype'))
    log.log_var(None, currentframe(), ('child_ptype',child_ptype))
    
    if child_ptype is not None:
        log.log_var(None, currentframe(), ('story_element',story_element))
        parent_path = get_folder_from_fqpath(story_element.get('path'))
        log.log_var(None, currentframe(), ('parent_path',parent_path))
        
        parent_ptype = story_element.get('ptype')
        
        for child in hlp.get_all(parent_path, extension=child_ptype, as_dict=True):
            child['ptype'] = child_ptype
            child['path'] = hlp.get_path_for_alias(parent_path, child.get(sec.ALIAS), child.get('ptype'))
            
            child['pptype'] = parent_ptype
            child[parent_ptype] = story_element.get('path')
            
            for ptype in pt.PlotHoleType:
                
                ptype_value = ptype.value
                
                if ptype_value in story_element:
                    child[ptype.value] = story_element.get(ptype.value)
            
            log.log_var(None, currentframe(), ('child',child))
            
            desolve_children(child)
            
            data = json.dumps(child, sort_keys=False, indent=2)
            fa.write(child.get('path'), data)

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
        
        parent_path = hlp.get_path_for_alias(get_parent_element_path(path), parent_alias, extension=parent_ptype)
        log.log_var(None, currentframe(), ('parent_path',parent_path))
        
        parent_obj['path'] = parent_path
        parent_obj['ptype'] = parent_ptype
        relations[parent_ptype] = parent_obj        
        
        path = parent_path
        
    log.log_var(None, currentframe(), ("relations", relations))

    return relations    


def __get_ptype_by_path(path):

    log.log_var(None, currentframe(), ("path", path))
    
    ptype = pathlib.Path(path).suffix.split(".")[-1]

    log.log_var(None, currentframe(), ("ptype", ptype))

    return ptype    

def get_parent_element_path(child_path):

    log.log_var(None, currentframe(), ("child_path", child_path))
    
    parent_path = pathlib.Path(pathlib.Path(child_path).parent).parent
   
    log.log_var(None, currentframe(), ("parent_path", parent_path)) 
    
    return parent_path

def get_folder_from_fqpath(fqpath):

    log.log_var(None, currentframe(), ("fqpath", fqpath))
    
    parent_path = pathlib.Path(fqpath).parent
   
    log.log_var(None, currentframe(), ("parent_path", parent_path)) 
    
    return parent_path    
    

def desolve_parent_by_path(path, return_path_only=False):
    
    log.log_var(None, currentframe(), ('path',path), ('return_path_only',return_path_only))
    
    # folder of the story element parent: part -> book
    parent_folder = get_parent_element_path(path)
    log.log_var(None, currentframe(), ("parent_folder", parent_folder))
    
    parent_ptype = __get_parent_ptype_by_path(path)
    log.log_var(None, currentframe(), ("parent_ptype", parent_ptype))
    
    parent_se = None
    
    if parent_ptype is not None:
        parent_se = hlp.get_all(parent_folder, parent_ptype, as_dict=True)[0]
        
    if return_path_only:
        parent_se = hlp.get_path_for_alias(parent_folder, parent_se.get(sec.ALIAS), extension=parent_ptype)
    
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
    
    test_path = "C:\\Users\\mthoma\\Documents\\PlotHole-Test_Repos"
    
    desolve(test_path)    