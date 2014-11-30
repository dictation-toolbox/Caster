'''
Created on Jun 29, 2014

@author: dave
'''
from apps import *
from lib import common, settings, ccr, utilities
from asynch import _element, _dispel

common.print_startup_message()
settings.load_settings()
ccr.refresh()
utilities.clean_temporary_files()
