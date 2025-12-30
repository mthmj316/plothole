# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 13:05:09 2025

@author: mthoma
"""
from inspect import currentframe, getframeinfo
from pathlib import Path
import sys
import datetime

# Global parameter
ENABLE_LOGGING = False
TRACE_ONLY = True

def get_current_time_stamp():
    return datetime.datetime.now(datetime.UTC).strftime('%F %T.%f')[:-3]

def log_var(clazz, current_frame, *args):
    if ENABLE_LOGGING:
        logs = []
        for t in args:
            _log = f"{t[0]}={t[1]}" 
            logs.append(_log)
            
        log(clazz, current_frame, '; '.join(logs))

def log(clazz, current_frame, log='void'):
    if ENABLE_LOGGING:
        
        file_info = getframeinfo(current_frame)
        
        source = ""
        if clazz is not None:
            source = type(clazz).__name__
        else:
            source = Path(file_info.filename).stem
        
        lineno = file_info.lineno
        function = file_info.function
        
        log_entry = ""
        if TRACE_ONLY:
            log_entry = f"{get_current_time_stamp()} ### {source}#{function}[{lineno}]"
        else:
            log_entry = f"{get_current_time_stamp()} ### {source}#{function}[{lineno}]: {log}"
        
        print(log_entry)
       
    
class Test():    
    def test(self):
        log_var(self, currentframe(), ("username", "Hans Gans"))
        
if __name__ == "__main__":
    
    
    print(sys.getrecursionlimit())
    
    ENABLE_LOGGING = True
    TRACE_ONLY = False
    t = Test()
    t.test()
    log_var(None, currentframe(), ("fileName","c:/Main/Program/Helper"))
    log_var(None, currentframe(), ('fileName',"c:/Main/Program/Helper"), ('upperCas',True),('range',200))
    
    TRACE_ONLY = True
    log_var(None, currentframe(), ('fileName',"c:/Main/Program/Helper"), ('upperCas',True),('range',200))
    
    ENABLE_LOGGING = False
    log_var(None, currentframe(), ('fileName',"c:/Main/Program/Helper"), ('upperCas',True),('range',200))