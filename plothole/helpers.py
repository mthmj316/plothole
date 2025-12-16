# -*- coding: utf-8 -*-
"""
Created on Mon Dec  8 20:26:25 2025

@author: mthoma
"""
import file_access as fs
import json

ALL_STORIES_FILE_FILTER = "{0}/**/*.{1}"

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
    aliases = []
    for story in get_all(base_dir, as_dict=True, extension=extension):
        aliases.append(story.get('alias'))
    return aliases

def get_book_path_by_alias(base_dir, alias):    
    return get_path_for_alias(base_dir, alias, extension='book')

def get_book_by_alias(base_dir, alias):
    
    for book in get_all(base_dir, as_dict=True, extension='book'):
        if book.get('alias') == alias:
            return book
        
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
    e = fs.read_from_file(fq_path, as_list=False)        
    if as_dict:
        e = json.loads(e)      
    return e

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
    return get(fq_path, as_dict)

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
    _filter = ALL_STORIES_FILE_FILTER.format(base_dir, extension)   
    pathes = fs.find_files(_filter, True)
    return pathes

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
    return get_all_pathes(base_dir, 'story')

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
    elements = []    
    for path in get_all_pathes(base_dir, extension=extension):
        elements.append(get_story(path, as_dict))
    return elements

def get_all_books(base_dir, as_dict=False):
    return get_all(base_dir, 'book', as_dict)
   
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
    return get_all(base_dir, 'story', as_dict)

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
    elements = get_all(base_dir, as_dict=True, extension=extension)
    for story in elements:
        if alias.casefold() == story.get('alias').casefold():
            return True  
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
    for path in get_all_pathes(base_dir, extension=extension):
        story = get_story(path, as_dict=True)
        if story.get('alias') == alias:
            return path
    return None
    