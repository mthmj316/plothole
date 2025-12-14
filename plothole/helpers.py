# -*- coding: utf-8 -*-
"""
Created on Mon Dec  8 20:26:25 2025

@author: mthoma
"""
import file_access as fs
import json

ALL_STORIES_FILE_FILTER = "{0}/**/*.story"

def get_all_aliases(base_dir):
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
    for story in get_all_stories(base_dir, as_dict=True):
        aliases.append(story.get('alias'))
    return aliases
    

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
    story = fs.read_from_file(fq_path, as_list=False)        
    if as_dict:
        story = json.loads(story)      
    return story

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
    _filter = ALL_STORIES_FILE_FILTER.format(base_dir)   
    pathes = fs.find_files(_filter, True)
    return pathes
 
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
    stories = []    
    for path in get_all_story_pathes(base_dir):
        stories.append(get_story(path, as_dict))
    return stories

def exists_alias(base_dir, alias):
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
    stories = get_all_stories(base_dir, as_dict=True)
    for story in stories:
        if alias.casefold() == story.get('alias').casefold():
            return True  
    return False
    