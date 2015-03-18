'''
Created on Jun 29, 2014

@author: dave

Instructions for adding new:
- homunculus windows in h_launch.py
- scanned languages (for "pita") in scanner.py
'''


try:
    from apps import *
    from asynch import *
    from lib import control, utilities, ccr, settings, context, recording
    from asynch import auto_com
    
    ccr.initialize_ccr()
    utilities.clean_temporary_files()
    recording.load_alias_rules()
    recording.load_recorded_rules()
    
    from asynch.hmc import h_launch
    h_launch.clean_homunculi()
    
except:
    import sys
    print sys.exc_info(), "\nAttempting to load CCR anyway..."
    from lib import ccr
    ccr.initialize_ccr()