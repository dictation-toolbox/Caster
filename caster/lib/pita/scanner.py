'''
To add a new scanned language:
    (1) add its filetype extension to SETTINGS["pita"]["extensions"] in lib/settings.py
    (2) add its keywords, long comment and short comment syntax in lib/pita/filters.py
'''

import os
import re

from caster.asynch.hmc import h_launch
from caster.lib import utilities, settings
from caster.lib.dfplus.state.actions import AsynchronousAction
from caster.lib.dfplus.state.short import L, S
from caster.lib.pita import filters
from caster.lib.pita.filters import LanguageFilter


if not settings.WSR:
    import natlink

_d = utilities.load_json_file(settings.SETTINGS["paths"]["PITA_JSON_PATH"])
DATA = _d if _d != {} else {"directories":{}}

def scan_directory(nexus):
    on_complete = AsynchronousAction.hmc_complete(lambda data: _scan_directory(data, nexus), nexus)
    h_launch.launch(settings.QTYPE_DIRECTORY)
    AsynchronousAction([L(S(["cancel"], on_complete, None))], 
                           time_in_seconds=0.5, 
                           repetitions=300, 
                           blocking=False).execute()

def rescan_current_file():
    global DATA
    try:
        filename, folders, title = utilities.get_window_title_info()
        current_file_path = guess_file_based_on_window_title(filename, folders)[1]
        scanned_file = _scan_single_file(current_file_path, LanguageFilter("." + filename.split(".")[-1]))
        # find out exact match in DATA
        file_was_found=False
        
        for d in DATA["directories"]:
            if current_file_path in DATA["directories"][d]:
                DATA["directories"][d][current_file_path] = scanned_file
                utilities.save_json_file(DATA, settings.SETTINGS["paths"]["PITA_JSON_PATH"])
                file_was_found=True
                break
        if not file_was_found:
            if not "uncategorized" in DATA["directories"]:
                DATA["directories"]["uncategorized"]={}
            DATA["directories"]["uncategorized"][current_file_path]=scanned_file
            utilities.save_json_file(DATA, settings.SETTINGS["paths"]["PITA_JSON_PATH"])
    except Exception:
        utilities.simple_log()
    
                

def _scan_directory(data, nexus):
    '''
    Adds a scan of the directory to DATA
    '''
    
    global DATA
    directory = data["path"]
    languageFilters = {}
    scanned_directory = {}
    try:
        for base, dirs, files in os.walk(directory):  # traverse base directory, and list directories as dirs and files as files
            for fname in files:
                extension = "." + fname.split(".")[-1]
                if not extension in languageFilters:
                    languageFilters[extension] = LanguageFilter(extension)
                
                if extension in settings.SETTINGS["pita"]["extensions"]:
                    # scanned_file is a list
                    scanned_file = _scan_single_file(base + "/" + fname, languageFilters[extension], nexus)
                    # scanned_directory["absolute path to file"] = that list
                    scanned_directory[base.replace("\\", "/") + "/" + fname] = scanned_file
                    
    except Exception:
        utilities.simple_log(True)
    
    if "directories" not in DATA:
        DATA["directories"] = {}
    DATA["directories"][directory] = scanned_directory
    
    utilities.save_json_file(DATA, settings.SETTINGS["paths"]["PITA_JSON_PATH"])

def _scan_single_file(path, languageFilter, nexus):
    f = open(path, "r")
    lines = f.readlines()
    f.close()
    
    # search out imports, function names, variable names
    scanned_file = {}
    scanned_file["names"] = []
    for line in lines:
        ''' to do: handle long comments '''
        if line.strip().startswith(languageFilter.short_comment):
            continue
        filter_results = filters.SYMBOL_PATTERN.findall(line)  # @UndefinedVariable
        for symbol in filter_results:
            if _passes_tests(symbol, scanned_file, languageFilter, nexus):
                scanned_file["names"].append(symbol)
    
    scanned_file["names"].sort()
    return scanned_file

def _passes_tests(symbol, scanned_file, language_filter, nexus):
    # short words can be gotten faster by just spelling them
    too_short = len(symbol) < 4
    already_in_names = symbol in scanned_file["names"]
    is_digit = symbol.isdigit()
    is_keyword = symbol in language_filter.keywords
    typeable = settings.SETTINGS["pita"]["filter_strict"] and nexus.dep.NATLINK and not _difficult_to_type(symbol)
    fails = is_keyword or already_in_names or too_short or is_digit or typeable
    return not fails


def guess_file_based_on_window_title(title_file, title_path_folders):
    global DATA
    
    d_candidate_best = ["", 0]
    for d in DATA["directories"]:
        d_candidate = [d, 0]
        for folder in title_path_folders:
            d_candidate[1] += 1 * (folder in d_candidate[0])
                
        if d_candidate[1] > d_candidate_best[1]:
            d_candidate_best = d_candidate
    
    
    f_candidate_best = ["", 0]
    for f in DATA["directories"][d_candidate_best[0]]:
        f_candidate = [f, 0]
        for folder in title_path_folders:
            f_candidate[1] += 1 * (folder in f_candidate[0])
        f_candidate[1] += 1 * (title_file in f_candidate[0])
        if f_candidate[1] > f_candidate_best[1]:
            f_candidate_best = f_candidate
            
    return d_candidate_best[0], f_candidate_best[0]



# ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## 
# Strict filter section
# ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## # ## 


STRICT_PARSER = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')            
def _difficult_to_type(name):
    global STRICT_PARSER
    found_something_difficult_to_type = False
    capitals_changed_to_underscores = STRICT_PARSER.sub(r'_\1', name).lower()
    broken_by_underscores = capitals_changed_to_underscores.split("_")
    for name_piece in broken_by_underscores:
        if not name_piece == "" and len(name_piece) > 1:
            dragon_check = natlink.getWordInfo(name_piece, 7)
            if dragon_check is None:  # only add letter combinations that Dragon doesn't recognize as words
                found_something_difficult_to_type = True
                break
    return found_something_difficult_to_type

