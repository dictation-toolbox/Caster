'''
Created on Jun 29, 2014

@author: dave
'''


try:
    from apps import *
    from asynch import *
    from lib import utilities, ccr, control, settings, context, recording
    
    control.print_startup_message()
    ccr.initialize_ccr()
    utilities.clean_temporary_files()
    recording.load_recorded_rules()
    
    from asynch.hmc import h_launch
    h_launch.clean_homunculi()
    
except:
    import sys
    print sys.exc_info(), "\nAttempting to load CCR anyway..."
    from lib import ccr
    ccr.initialize_ccr()