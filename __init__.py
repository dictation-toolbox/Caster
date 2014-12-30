'''
Created on Jun 29, 2014

@author: dave
'''
from apps import *
from asynch import _element, _dispel
from asynch.hmc import h_launch
from lib import utilities
from lib import ccr
from lib import control
from lib import settings, context


control.print_startup_message()
ccr.initialize_ccr()
# ccr.refresh()
utilities.clean_temporary_files()
h_launch.clean_homunculi()
context.load_recorded_rules()