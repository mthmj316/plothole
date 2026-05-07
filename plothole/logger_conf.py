LOGGING_ALL=False
LOGGING_SOURCE = [
    #'StoryElementTreeview#*'
    # 'BookModel#*',
    #'NavigatorInstance#*',
    #'relation_desolver#desolve_children'
    #'file_access#*'
    # 'PlotholeModel#*'
    # 'SelectedStoryElements#*',
    #'PartModel#*',
    'StoryModel#*'
    #'plothole_core#*',
    #'helpers#get_path_for_alias'
    # '*#get_all'
    ]


def is_log_on(source,function=None):
    
    if LOGGING_ALL == True:
        return True
    
    if f"{source}#*" in LOGGING_SOURCE:
        return True

    if f"*#{function}" in LOGGING_SOURCE:
        return True
    
    if function is not None:
        source = f"{source}#{function}"
        
    if source in LOGGING_SOURCE:
        return True
    
    return False