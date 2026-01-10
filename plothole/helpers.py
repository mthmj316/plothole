# -*- coding: utf-8 -*-
"""
Created on Mon Dec  8 20:26:25 2025

@author: mthoma
"""
import file_access as fs
import json
import time
from datetime import datetime
from inspect import currentframe
import logger as log

ALL_STORIES_FILE_FILTER = "{0}/**/*.{1}"

def exists_alias(base_dir, alias, extension='story'):
    """
    Returns True if the passed alias already exists.
    The search for the alias is case-insensitive

    Parameters
    ----------
    base_dir : string
        The directory which is search for the given alias
    alias : string
        The alias which searched for.

    Returns
    -------
    bool
        True in case the alias exists otherwise false.

    """
    log.log_var(None, currentframe(), ('base_dir',base_dir), ('alias',alias), ('extension',extension))
    
    elements = get_all(base_dir, as_dict=True, extension=extension)
    for story in elements:
        if alias.casefold() == story.get('alias').casefold():
            log.log_var(None, currentframe(), ('return',True))
            return True
    log.log_var(None, currentframe(), ('return',False))
    return False
    
def get_path_for_alias(base_dir, alias, extension='story'):
    """
    Returns for the given alias the fully qulified path of the story with given path.

    Parameters
    ----------
    base_dir : string
        Path for directory which searched for the story
    alias : string
        Aieas of the story.

    Returns
    -------
    string
        Fully qulified name of the story with the given alias.

    """
    log.log_var(None, currentframe(), ('base_dir',base_dir), ('alias',alias), ('extension',extension))
    for path in get_all_pathes(base_dir, extension=extension):
        story = get_story(path, as_dict=True)
        if story.get('alias') == alias:
            log.log_var(None, currentframe(), ('return',True))
            return path
    log.log_var(None, currentframe(), ('return',False))
    return None

def get_current_time_stamp(millis=False): 
    
    log.log_var(None, currentframe(), ('millis',millis))
    if millis:
        timestamp = datetime.utcnow().strftime('%F %T.%f')[:-3]
        log.log_var(None, currentframe(), ('return',timestamp))
        return timestamp
    
    _format='%Y%m%d-%H%M%S'
    timestr = time.strftime(_format)
    log.log_var(None, currentframe(), ('return',timestr))
    return timestr

def get_all_aliases(base_dir, extension='story'):
    """
    Returns a list of all aliases fond in the base dir.

    Parameters
    ----------
    base_dir : string
        Directory which searched recursively.

    Returns
    -------
    aliases : list
        All found aliaese

    """
    log.log_var(None, currentframe(), ('base_dir',base_dir), ('extension',extension))
    aliases = []
    for story in get_all(base_dir, as_dict=True, extension=extension):
        aliases.append(story.get('alias'))
    log.log_var(None, currentframe(), ('return',aliases))
    return aliases

def get_by_alias(base_dir, alias, extension):
    log.log_var(None, currentframe(), ('base_dir',base_dir), ('alias',alias), ('extension',extension))
    for book in get_all(base_dir, as_dict=True, extension=extension):
        if book.get('alias') == alias:
            log.log_var(None, currentframe(), ('return',book))
            return book
    log.log_var(None, currentframe(), ('return',"None"))
    return None

def get(fq_path, as_dict=False):
    """
    Returns the plothole element for the fully qulified apth

    Parameters
    ----------
    fq_path : string
        Fully qualified path of the plothole element
    as_dict : bool, optional
        If True the element is retured as dictionary, otherwise as string. 
        The default is False.

    Returns
    -------
    None.

    """
    log.log_var(None, currentframe(), ('fq_path',fq_path), ('as_dict',as_dict))
    e = fs.read_from_file(fq_path, as_list=False)        
    if as_dict:
        e = json.loads(e)
    log.log_var(None, currentframe(), ('return',e))     
    return e

def get_all_pathes(base_dir, extension):
    """
    Returns for the given extension all fully qualified names.

    Parameters
    ----------
    base_dir : string
        The directory which is recursively searched.

    Returns
    -------
    pathes : string
        A list of of all pathes.

    """
    log.log_var(None, currentframe(), ('base_dir',base_dir), ('extension',extension))
    _filter = ALL_STORIES_FILE_FILTER.format(base_dir, extension)   
    pathes = fs.find_files(_filter, True)
    log.log_var(None, currentframe(), ('return',pathes)) 
    return pathes

def get_all(base_dir, extension, as_dict=False):
    """
    Returns all existing plothole elements with the given extenesion.
    The search is recursive - subfolder will be searched, too.
    In case as_dict==True the single stories will be returned as dictionaries
    otherwise as string

    Parameters
    ----------
    base_dir : String
        The directory which is searched for the stories.
    as_dict : bool, optional
        If True the story is retured as dictionary, otherwise as string. 
        The default is False.

    Returns
    -------
    stories : list
        ALl found stories. .

    """
    log.log_var(None, currentframe(), ('base_dir',base_dir), ('extension',extension), ('as_dict',as_dict))
    elements = []    
    for path in get_all_pathes(base_dir, extension=extension):
        elements.append(get_story(path, as_dict))
    log.log_var(None, currentframe(), ('return',elements)) 
    return elements

def get_story_path_by_alias(base_dir, alias): 
    log.log_var(None, currentframe(), ('base_dir',base_dir), ('alias',alias))
    extension='story'
    ret_val = get_path_for_alias(base_dir, alias, extension)
    log.log_var(None, currentframe(), ('return',ret_val)) 
    return ret_val

def get_book_path_by_alias(base_dir, alias): 
    log.log_var(None, currentframe(), ('base_dir',base_dir), ('alias',alias))
    extension='book'
    ret_val = get_path_for_alias(base_dir, alias, extension)
    log.log_var(None, currentframe(), ('return',ret_val)) 
    return ret_val

def get_part_path_by_alias(base_dir, alias): 
    log.log_var(None, currentframe(), ('base_dir',base_dir), ('alias',alias))
    extension='part'
    ret_val = get_path_for_alias(base_dir, alias, extension)
    log.log_var(None, currentframe(), ('return',ret_val)) 
    return ret_val


def get_story_by_alias(base_dir, alias):
    log.log_var(None, currentframe(), ('base_dir',base_dir), ('alias',alias))
    extension='story' 
    ret_val = get_by_alias(base_dir, alias, extension)
    log.log_var(None, currentframe(), ('return',ret_val)) 
    return ret_val

def get_book_by_alias(base_dir, alias):
    log.log_var(None, currentframe(), ('base_dir',base_dir), ('alias',alias))
    extension='book' 
    ret_val = get_by_alias(base_dir, alias, extension)
    log.log_var(None, currentframe(), ('return',ret_val)) 
    return ret_val

def get_part_by_alias(base_dir, alias):
    log.log_var(None, currentframe(), ('base_dir',base_dir), ('alias',alias))
    extension='part'   
    ret_val = get_by_alias(base_dir, alias, extension)
    log.log_var(None, currentframe(), ('return',ret_val)) 
    return ret_val

def get_story(fq_path, as_dict=False):
    """
    Returns the story for the fully qulified apth

    Parameters
    ----------
    fq_path : string
        Fully qualified path of the story
    as_dict : bool, optional
        If True the story is retured as dictionary, otherwise as string. 
        The default is False.

    Returns
    -------
    None.

    """
    log.log_var(None, currentframe(), ('fq_path',fq_path), ('as_dict',as_dict))
    ret_val = get(fq_path, as_dict)
    log.log_var(None, currentframe(), ('return',ret_val)) 
    return ret_val

def get_book(fq_path, as_dict=False):
    """
    Returns the book for the fully qulified apth

    Parameters
    ----------
    fq_path : string
        Fully qualified path of the story
    as_dict : bool, optional
        If True the story is retured as dictionary, otherwise as string. 
        The default is False.

    Returns
    -------
    None.

    """
    log.log_var(None, currentframe(), ('fq_path',fq_path), ('as_dict',as_dict))
    ret_val = get(fq_path, as_dict)
    log.log_var(None, currentframe(), ('return',ret_val)) 
    return ret_val

def get_part(fq_path, as_dict=False):
    """
    Returns the part for the fully qulified apth

    Parameters
    ----------
    fq_path : string
        Fully qualified path of the story
    as_dict : bool, optional
        If True the story is retured as dictionary, otherwise as string. 
        The default is False.

    Returns
    -------
    None.

    """
    log.log_var(None, currentframe(), ('fq_path',fq_path), ('as_dict',as_dict))
    ret_val = get(fq_path, as_dict)
    log.log_var(None, currentframe(), ('return',ret_val)) 
    return ret_val

def get_all_story_pathes(base_dir):
    """
    Returns for all stories the fully qualified name.

    Parameters
    ----------
    base_dir : string
        The directory which is recursively searched.

    Returns
    -------
    pathes : string
        A list of of all pathes.

    """
    log.log_var(None, currentframe(), ('base_dir',base_dir))
    ret_val = get_all_pathes(base_dir, 'story')
    log.log_var(None, currentframe(), ('return',ret_val)) 
    return ret_val

def get_all_book_pathes(base_dir):
    """
    Returns for all books the fully qualified name.

    Parameters
    ----------
    base_dir : string
        The directory which is recursively searched.

    Returns
    -------
    pathes : string
        A list of of all pathes.

    """
    log.log_var(None, currentframe(), ('base_dir',base_dir))
    ret_val = get_all_pathes(base_dir, 'book')
    log.log_var(None, currentframe(), ('return',ret_val)) 
    return ret_val

def get_all_part_pathes(base_dir):
    """
    Returns for all parts the fully qualified name.

    Parameters
    ----------
    base_dir : string
        The directory which is recursively searched.

    Returns
    -------
    pathes : string
        A list of of all pathes.

    """
    log.log_var(None, currentframe(), ('base_dir',base_dir))
    ret_val =  get_all_pathes(base_dir, 'part')
    log.log_var(None, currentframe(), ('return',ret_val)) 
    return ret_val

def get_all_stories(base_dir, as_dict=False):
    """
    Returns all existing stories.
    The search is recursive - subfolder will be searched, too.
    In case as_dict==True the single stories will be returned as dictionaries
    otherwise as string

    Parameters
    ----------
    base_dir : String
        The directory which is searched for the stories.
    as_dict : bool, optional
        If True the story is retured as dictionary, otherwise as string. 
        The default is False.

    Returns
    -------
    stories : list
        ALl found stories. .

    """
    log.log_var(None, currentframe(), ('base_dir',base_dir), ('as_dict',as_dict))
    ret_val = get_all(base_dir, 'story', as_dict)
    log.log_var(None, currentframe(), ('return',ret_val)) 
    return ret_val

def get_all_books(base_dir, as_dict=False):
    log.log_var(None, currentframe(), ('base_dir',base_dir), ('as_dict',as_dict))
    ret_val = get_all(base_dir, 'book', as_dict)
    log.log_var(None, currentframe(), ('return',ret_val)) 
    return ret_val
   
def get_all_parts(base_dir, as_dict=False):
    log.log_var(None, currentframe(), ('base_dir',base_dir), ('as_dict',as_dict))
    ret_val = get_all(base_dir, 'part', as_dict)
    log.log_var(None, currentframe(), ('return',ret_val)) 
    return ret_val