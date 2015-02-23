import os

from lib import utilities, settings
from lib.element import regex
from lib.element.regex import LanguageRegexSet


DATA = {}

def scan_directory(directory):
    '''
    Adds a scan of the directory to DATA
    '''
    
    global DATA
    languageRegexSets={}
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
                        languageRegexSets[extension]=LanguageRegexSet(extension)
                    
                    # search out imports, function names, variable names
                    scanned_file = {}
                    scanned_file["names"] = []
                    for line in lines:
                        filter_results = _filter_words(line, languageRegexSets[extension])
                        for result in filter_results:
                            if _passes_tests(result, scanned_file):
                                scanned_file["names"].append(result)
                    
                    scanned_file["names"].sort()
                    scanned_directory[base + "/" + fname] = scanned_file
    except Exception:
        utilities.simple_log(True)
    
    meta_information = {}
    meta_information["files"] = scanned_directory
    DATA["directories"][directory] = meta_information

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
    if len(lrs.import_match_object) > 0:
        results = _process_match(lrs.import_match_object, lrs.import_indices, results)
    if len(lrs.function_match_object) > 0:
        results = _process_match(lrs.function_match_object, lrs.function_indices, results)
    if len(lrs.variable_match_object) > 0:
        results = _process_match(lrs.variable_match_object, lrs.variable_indices, results)
    return results

def _process_match(self, match_object, indices, results):
    for m in match_object:
        if isinstance(m, tuple):
            for index in indices:
                match = m[index]
                if not (match == "" or match.isdigit() or match in results):
                    results.append(match)
        elif isinstance(m, str):
            results.append(m)
    return results

def _passes_tests(self, word, scanned_file):
    # short words can be gotten faster by just spelling them
    too_short = len(word) < 4
    already_in_names = word in scanned_file["names"]
    return already_in_names or too_short