'''
Created on Jun 29, 2014

@author: dave
'''
try:
    from apps import *
    from asynch import _element, _dispel, _hmc
    from asynch.hmc import h_launch
    from lib import utilities
    from lib import ccr
    from lib import control
    from lib import settings, context, recording
    
    control.print_startup_message()
    ccr.initialize_ccr()
    utilities.clean_temporary_files()
    h_launch.clean_homunculi()
    recording.load_recorded_rules()
except:
    import sys
    print sys.exc_info(), "\nAttempting to load CCR anyway..."
    from lib import ccr
    ccr.initialize_ccr()