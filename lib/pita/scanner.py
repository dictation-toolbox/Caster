import os
import re

from asynch.hmc import h_launch
from lib import utilities, settings
from lib.pita import filters
from lib.pita.filters import LanguageFilter


NATLINK_AVAILABLE = True
try:
    import natlink
except Exception:
    NATLINK_AVAILABLE = False

_d = utilities.load_json_file(settings.SETTINGS["paths"]["PITA_JSON_PATH"])
DATA = _d if _d != {} else {"directories":{}}

# filename_pattern was used to determine when to update the list in the element window, checked to see when a new file name had appeared
FILENAME_PATTERN = re.compile(r"[/\\]([\w_]+\.[\w]+)")

def scan_directory():
    h_launch.launch(settings.QTYPE_DIRECTORY, _scan_directory, None)
    

def _scan_directory(data):
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
                if extension in settings.SETTINGS["element"]["extensions"]:
                    f = open(base + "/" + fname, "r")
                    lines = f.readlines()
                    f.close()
                    
                    # may as well reuse these
                    if not (extension in languageFilters):
                        languageFilters[extension] = LanguageFilter(extension)
                    
                    # search out imports, function names, variable names
                    scanned_file = {}
                    scanned_file["names"] = []
                    for line in lines:
                        ''' to do: handle long comments '''
                        if line.strip().startswith(languageFilters[extension].short_comment):
                            continue
                        filter_results = filters.SYMBOL_PATTERN.findall(line)  # _filter_words(line, languageFilters[extension])
                        for symbol in filter_results:
                            if _passes_tests(symbol, scanned_file, languageFilters[extension]):
                                scanned_file["names"].append(symbol)
                    
                    scanned_file["names"].sort()
                    scanned_directory[base.replace("\\", "/") + "/" + fname] = scanned_file
    except Exception:
        utilities.simple_log(True)
    
    meta_information = {}
    meta_information["files"] = scanned_directory
    DATA["directories"][directory] = meta_information
    
    utilities.save_json_file(DATA, settings.SETTINGS["paths"]["PITA_JSON_PATH"])

def _passes_tests(symbol, scanned_file, language_filter):
    global NATLINK_AVAILABLE
    # short words can be gotten faster by just spelling them
    too_short = len(symbol) < 4
    already_in_names = symbol in scanned_file["names"]
    is_digit = symbol.isdigit()
    is_keyword = symbol in language_filter.keywords
    typeable = (settings.SETTINGS["element"]["filter_strict"] and NATLINK_AVAILABLE and not _difficult_to_type(symbol))
    return not (is_keyword or already_in_names or too_short or is_digit or typeable)






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

