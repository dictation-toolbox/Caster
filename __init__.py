'''
Created on Jun 29, 2014

@author: dave
'''
from lib import settings
from apps import *
from asynch import _element, _dispel
from asynch.hmc import h_launch
from lib import control
from lib import  ccr, utilities

control.print_startup_message()
ccr.refresh()
utilities.clean_temporary_files()
h_launch.clean_homunculi()
