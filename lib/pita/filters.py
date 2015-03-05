'''
Created on Feb 21, 2015

@author: dave
'''
import re

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

#javascript language
JAVASCRIPT_KEYWORDS = ["abstract", "arguments", "boolean", "break", "byte", 
                 "case", "catch", "char", "class", "const", "continue", 
                 "debugger", "default", "delete", "do", "double", "else", 
                 "enum", "eval", "export", "extends", "false", "final", 
                 "finally", "float", "for", "function", "goto", "if", 
                 "implements", "import", "in", "instanceof", "int", 
                 "interface", "let", "long", "native", "new", "null", 
                 "package", "private", "protected", "public", "return", 
                 "short", "static", "super", "switch", "synchronized", 
                 "this", "throw", "throws", "transient", "true", "try", 
                 "typeof", "var", "void", "volatile", "while", "with", 
                 "yield"]
JAVASCRIPT_LONG_COMMENT = ["/*", "*/"]
JAVASCRIPT_SHORT_COMMENT = "//"

# C++ language
CPP_KEYWORDS = ["alignas", "alignof", "and", "and_eq", "asm", "auto", 
                "bitand", "bitor", "bool", "break", "case", "catch", 
                "char", "char16_t", "char32_t", "class", "compl", 
                "concept", "const", "constexpr", "const_cast", "continue", 
                "decltype", "default", "delete", "do", "double", 
                "dynamic_cast", "else", "enum", "explicit", "export", 
                "extern", "false", "float", "for", "friend", "goto", "if", 
                "inline", "int", "long", "mutable", "namespace", "new", 
                "noexcept", "not", "not_eq", "nullptr", "operator", "or", 
                "or_eq", "private", "protected", "public", "register", 
                "reinterpret_cast", "requires", "return", "short", "signed", 
                "sizeof", "static", "static_assert", "static_cast", "struct", 
                "switch", "template", "this", "thread_local", "throw", "true", 
                "try", "typedef", "typeid", "typename", "union", "unsigned", 
                "using", "virtual", "void", "volatile", "wchar_t", "while", 
                "xor", "xor_eq"   ]
CPP_LONG_COMMENT = ["/*", "*/"]
CPP_SHORT_COMMENT = "//"

class LanguageFilter:
    def __init__(self, extension):
        
        self.extension = extension.lower()
        
        if self.extension == ".java":
            global JAVA_KEYWORDS, JAVA_SHORT_COMMENT, JAVA_LONG_COMMENT
            self.keywords, self.short_comment, self.long_comment = JAVA_KEYWORDS, JAVA_SHORT_COMMENT, JAVA_LONG_COMMENT
        elif self.extension == ".js":
            global JAVASCRIPT_KEYWORDS, JAVASCRIPT_SHORT_COMMENT, JAVASCRIPT_LONG_COMMENT
            self.keywords, self.short_comment, self.long_comment = JAVASCRIPT_KEYWORDS, JAVASCRIPT_SHORT_COMMENT, JAVASCRIPT_LONG_COMMENT
        elif self.extension == ".py":
            global PYTHON_KEYWORDS, PYTHON_SHORT_COMMENT, PYTHON_LONG_COMMENT
            self.keywords, self.short_comment, self.long_comment = PYTHON_KEYWORDS, PYTHON_SHORT_COMMENT, PYTHON_LONG_COMMENT
        elif self.extension in [".cpp", ".h"]:
            global CPP_KEYWORDS, CPP_SHORT_COMMENT, CPP_LONG_COMMENT
            self.keywords, self.short_comment, self.long_comment = CPP_KEYWORDS, CPP_SHORT_COMMENT, CPP_LONG_COMMENT
        else:
            self.keywords, self.short_comment, self.long_comment = [], "\n", []





