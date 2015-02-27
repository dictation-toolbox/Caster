import os
import re

from asynch.hmc import h_launch
from lib import utilities, settings
from lib.element import regex
from lib.element.regex import LanguageRegexSet


NATLINK_AVAILABLE = True
try:
    import natlink
except Exception:
    NATLINK_AVAILABLE = False

_d = settings.load_json_file(settings.SETTINGS["paths"]["ELEMENT_JSON_PATH"])
DATA = _d if _d != {} else {"directories":{}}

# filename_pattern was used to determine when to update the list in the element window, checked to see when a new file name had appeared
FILENAME_PATTERN = re.compile(r"[/\\]([\w]+\.[\w]+)")

def scan_directory():
    h_launch.launch(settings.QTYPE_DIRECTORY, _scan_directory, None)
    

def _scan_directory(data):
    '''
    Adds a scan of the directory to DATA
    '''
    
    global DATA
    directory=data["path"]
    languageRegexSets = {}
    scanned_directory = {}
    
    try:
        for base, dirs, files in os.walk(directory):  # traverse base directory, and list directories as dirs and files as files
            for fname in files:
                extension = "." + fname.split(".")[-1]
                if extension in settings.SETTINGS["element"]["extensions"]:
                    f = open(base + "/" + fname, "r")
                    lines = f.readlines()
                    f.close()
                    
                    # may as well reuse these
                    if not (extension in languageRegexSets):
                        languageRegexSets[extension] = LanguageRegexSet(extension)
                    
                    # search out imports, function names, variable names
                    scanned_file = {}
                    scanned_file["names"] = []
                    for line in lines:
                        filter_results = _filter_words(line, languageRegexSets[extension])
                        for result in filter_results:
                            if _passes_tests(result, scanned_file):
                                scanned_file["names"].append(result)
                    
                    scanned_file["names"].sort()
                    scanned_directory[base.replace("\\", "/") + "/" + fname] = scanned_file
    except Exception:
        utilities.simple_log(True)
    
    meta_information = {}
    meta_information["files"] = scanned_directory
    DATA["directories"][directory] = meta_information
    
    settings.save_json_file(DATA, settings.SETTINGS["paths"]["ELEMENT_JSON_PATH"])

def _filter_words(line, lrs):
    '''
    Scans a single line fed to it by another function
    
    '''
    #  handle the case that a regular expression hasn't been made  for this language yet
    if lrs.unmatched:
        results = []
        generic_match_object = regex.GENERIC_PATTERN.findall(line)  # for languages without specific regular expressions made yet
        if len(generic_match_object) > 0:
            results = _process_match(generic_match_object, [0], results)
        return results
    
    results = []
    for match_object, indices in [(lrs.import_regex.findall(line), lrs.import_indices),
                                  (lrs.function_regex.findall(line), lrs.function_indices),
                                  (lrs.variable_regex.findall(line), lrs.variable_indices), ]:
        results = _process_match(match_object, indices, results)
    return results

def _process_match(match_object, indices, results):
    for m in match_object:
        if isinstance(m, tuple):
            for index in indices:
                match = m[index]
                if not (match == "" or match.isdigit() or match in results):
                    results.append(match)
        elif isinstance(m, str):
            results.append(m)
    return results

def _passes_tests(word, scanned_file):
    global NATLINK_AVAILABLE
    # short words can be gotten faster by just spelling them
    too_short = len(word) < 4
    already_in_names = word in scanned_file["names"]
    typeable = (settings.SETTINGS["element"]["filter_strict"] and NATLINK_AVAILABLE and not _difficult_to_type(word))
    return not (already_in_names or too_short or typeable)






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
            if dragon_check == None:  # only add letter combinations that Dragon doesn't recognize as words
                found_something_difficult_to_type = True
                break
    return found_something_difficult_to_type

