LOGGING_ALL=False
LOGGING_SOURCE = [
    # 'BookModel#*',
    # 'file_access#read_from_file',
    # '*#onLoad'
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