# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 13:05:09 2025

@author: mthoma
"""
import helpers as hlp
# Global parameter
ENABLE_PRINT = True
OPENING_ASTERIS_CTN = 100
CLOSSING_ASTERIS_CTN = OPENING_ASTERIS_CTN

def log_var(source, function, **kwargs):
    if ENABLE_PRINT:
        logs = []
        for v_name, v_value in kwargs.items():
            _log = f"{v_name}={v_value}" 
            logs.append(_log)
            
        log(source, function, '; '.join(logs))

def log(source, function, log):
    if ENABLE_PRINT:
       log_entry = f"{hlp.get_current_time_stamp(millis=True)}->{source}#{function}: {log}"
       print(log_entry)
       
       
if __name__ == "__main__":
    log_var("SomeModel", "onLoad", fileName="c:/Main/Program/Helper")
    log_var("SomeModel", "onLoad", fileName="c:/Main/Program/Helper", upperCase=True,_range=200)