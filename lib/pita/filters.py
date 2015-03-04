'''
Created on Feb 21, 2015

@author: dave
'''
import re


GENERIC_PATTERN = re.compile("([A-Za-z0-9._]+\s*=)|(import [A-Za-z0-9._]+)")
SYMBOL_PATTERN = re.compile("([A-Za-z0-9_]+)")

# python language
PYTHON_KEYWORDS = ["and", "del", "from", "not", "while", "as", "elif",
                 "global", "or", "with", "assert", "else", "if", "pass",
                 "yield", "break", "except", "import", "print", "class",
                 "exec", "in", "raise", "continue", "finally", "is",
                 "return", "def", "for", "lambda", "try"]
PYTHON_LONG_COMMENT = ["'''", '"""']
PYTHON_SHORT_COMMENT = "#"

# java language
JAVA_KEYWORDS = ["abstract", "continue", "for", "new", "switch", "assert",
                 "default", "goto", "package", "synchronized", "boolean",
                 "do", "if", "private", "this", "break", "double",
                 "implements", "protected", "throw", "byte", "else",
                 "import", "public", "throws", "case", "enum",
                 "instanceof", "return", "transient", "catch", "extends",
                 "int", "short", "try", "char", "final", "interface",
                 "static", "void", "class", "finally", "long", "strictfp",
                 "volatile", "const", "float", "native", "super", "while"]
JAVA_LONG_COMMENT = ["/*", "*/"]
JAVA_SHORT_COMMENT = "//"

class LanguageFilter:
    def __init__(self, extension):
        
        self.extension = extension.lower()
        
        if self.extension == ".java":
            global JAVA_KEYWORDS, JAVA_SHORT_COMMENT, JAVA_LONG_COMMENT
            self.keywords, self.short_comment, self.long_comment = JAVA_KEYWORDS, JAVA_SHORT_COMMENT, JAVA_LONG_COMMENT
        elif self.extension == ".py":
            global PYTHON_KEYWORDS, PYTHON_SHORT_COMMENT, PYTHON_LONG_COMMENT
            self.keywords, self.short_comment, self.long_comment = PYTHON_KEYWORDS, PYTHON_SHORT_COMMENT, PYTHON_LONG_COMMENT
        else:
            self.keywords, self.short_comment, self.long_comment = [], "\n", []





