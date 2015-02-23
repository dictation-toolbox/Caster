'''
Created on Feb 21, 2015

@author: dave
'''
import re


GENERIC_PATTERN = re.compile("([A-Za-z0-9._]+\s*=)|(import [A-Za-z0-9._]+)")

# python language
PYTHON_IMPORTS = re.compile("((\bimport\b|\bfrom\b|\bas\b)(\(|,| )*[A-Za-z0-9._]+)")  # capture group index 3
PYTHON_FUNCTIONS = re.compile("(\bdef \b([A-Za-z0-9_]+)\()|(\.([A-Za-z0-9_]+)\()")  # cgi 1 or 3
PYTHON_VARIABLES = re.compile("(([A-Za-z0-9_]+)[ ]*=)|((\(|,| )([A-Za-z0-9_]+)(\)|,| ))")  # 1 or 4
# Indices indicate relevant match groups
PYTHON_IMPORT_INDICES = [3]
PYTHON_FUNCTION_INDICES = [1, 3]
PYTHON_VARIABLE_INDICES = [1, 4]

# java language
JAVA_IMPORTS = re.compile("import [A-Za-z0-9_\\.]+\.([A-Za-z0-9_]+);|throws ([A-Za-z0-9_]+)|new ([A-Za-z0-9_<>]+)|([A-Za-z0-9_]+)\.")
JAVA_METHODS = re.compile("[ \.]([A-Za-z0-9_]+)\(")
JAVA_VARIABLES = re.compile("([ \.]*([A-Za-z0-9_]+)[ ]*=)|((\bpublic\b|\bprivate\b|\binternal\b|\bfinal\b|\bstatic\b)[ ]+[A-Za-z0-9_]+[ ]+([A-Za-z0-9_]+)[ ]*[;=])|(([A-Za-z0-9_]+)[ ]*[,\)])")  # 1,4,6
JAVA_IMPORT_INDICES = [0, 1, 2, 3]
JAVA_FUNCTION_INDICES = [0]
JAVA_VARIABLE_INDICES = [1, 4, 6]

class LanguageRegexSet:
    def __init__(self, extension):
        self.extension = extension.lower()
        self.unmatched = False
        
        if self.extension == ".java":
            global JAVA_IMPORTS, JAVA_METHODS, JAVA_VARIABLES, JAVA_IMPORT_INDICES, \
            JAVA_FUNCTION_INDICES, JAVA_VARIABLE_INDICES 
            self.import_match_object, self.function_match_object, self.variable_match_object, \
            self.import_indices, self.function_indices, self.variable_indices = \
            JAVA_IMPORTS, JAVA_METHODS, JAVA_VARIABLES, JAVA_IMPORT_INDICES, \
            JAVA_FUNCTION_INDICES, JAVA_VARIABLE_INDICES
        elif self.extension == ".py":
            global PYTHON_IMPORTS, PYTHON_METHODS, PYTHON_VARIABLES, PYTHON_IMPORT_INDICES, \
            PYTHON_FUNCTION_INDICES, PYTHON_VARIABLE_INDICES 
            self.import_match_object, self.function_match_object, self.variable_match_object, \
            self.import_indices, self.function_indices, self.variable_indices = \
            PYTHON_IMPORTS, PYTHON_METHODS, PYTHON_VARIABLES, PYTHON_IMPORT_INDICES, \
            PYTHON_FUNCTION_INDICES, PYTHON_VARIABLE_INDICES
        else:
            self.unmatched = True





