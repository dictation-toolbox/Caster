'''
Created on Sep 1, 2015

@author: synkarius
'''
from dragonfly import Dictation, MappingRule, Choice, Pause

from castervoice.lib import control
from castervoice.lib.actions import Key, Text
from castervoice.lib.ccr.standard import SymbolSpecs
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R


class PythonNon(MappingRule):
    mapping = {
        "with":
            R(Text("with "), rdescript="Python: With"),
        "open file":
            R(Text("open('filename','r') as f:"), rdescript="Python: Open File"),
        "read lines":
            R(Text("content = f.readlines()"), rdescript="Python: Read Lines"),
        "try catch":
            R(Text("try:") + Key("enter:2/10, backspace") + Text("except Exception:") +
              Key("enter"),
              rdescript="Python: Try Catch"),
    }


class Python(MergeRule):
    non = PythonNon

    mapping = {
        SymbolSpecs.IF:
            R(Key("i,f,space,colon,left"), rdescript="Python: If"),
        SymbolSpecs.ELSE:
            R(Text("else:") + Key("enter"), rdescript="Python: Else"),
        # (no switch in Python)
        SymbolSpecs.BREAK:
            R(Text("break"), rdescript="Python: Break"),
        SymbolSpecs.FOR_EACH_LOOP:
            R(Text("for  in :") + Key("left:5"), rdescript="Python: For Each Loop"),
        SymbolSpecs.FOR_LOOP:
            R(Text("for i in range(0, ):") + Key("left:2"),
              rdescript="Python: For i Loop"),
        SymbolSpecs.WHILE_LOOP:
            R(Text("while :") + Key("left"), rdescript="Python: While"),
        # (no do-while in Python)
        SymbolSpecs.TO_INTEGER:
            R(Text("int()") + Key("left"), rdescript="Python: Convert To Integer"),
        SymbolSpecs.TO_FLOAT:
            R(Text("float()") + Key("left"),
              rdescript="Python: Convert To Floating-Point"),
        SymbolSpecs.TO_STRING:
            R(Text("str()") + Key("left"), rdescript="Python: Convert To String"),
        SymbolSpecs.AND:
            R(Text(" and "), rdescript="Python: And"),
        SymbolSpecs.OR:
            R(Text(" or "), rdescript="Python: Or"),
        SymbolSpecs.NOT:
            R(Text("!"), rdescript="Python: Not"),
        SymbolSpecs.SYSOUT:
            R(Text("print()") + Key("left"), rdescript="Python: Print"),
        SymbolSpecs.IMPORT:
            R(Text("import "), rdescript="Python: Import"),
        SymbolSpecs.FUNCTION:
            R(Text("def ():") + Key("left:3"), rdescript="Python: Function"),
        SymbolSpecs.CLASS:
            R(Text("class :") + Key("left"), rdescript="Python: Class"),
        SymbolSpecs.COMMENT:
            R(Text("#"), rdescript="Python: Add Comment"),
        SymbolSpecs.LONG_COMMENT:
            R(Text("''''''") + Key("left:3"), rdescript="Python: Long Comment"),
        SymbolSpecs.NULL:
            R(Text("None"), rdescript="Python: Null"),
        SymbolSpecs.RETURN:
            R(Text("return "), rdescript="Python: Return"),
        SymbolSpecs.TRUE:
            R(Text("True"), rdescript="Python: True"),
        SymbolSpecs.FALSE:
            R(Text("False"), rdescript="Python: False"),

        # Python specific
        "sue iffae":
            R(Text("if "), rdescript="Python: Short If"),
        "sue shells":
            R(Text("else "), rdescript="Python: Short Else"),
        "from":
            R(Text("from "), rdescript="Python: From"),
        "self":
            R(Text("self"), rdescript="Python: Self"),
        "long not":
            R(Text(" not "), rdescript="Python: Long Not"),
        "it are in":
            R(Text(" in "), rdescript="Python: In"),  #supposed to sound like "iter in"
        "shell iffae | LFA":
            R(Key("e,l,i,f,space,colon,left"), rdescript="Python: Else If"),
        "convert to character":
            R(Text("chr()") + Key("left"), rdescript="Python: Convert To Character"),
        "length of":
            R(Text("len()") + Key("left"), rdescript="Python: Length"),
        "global":
            R(Text("global "), rdescript="Python: Global"),
        "make assertion":
            R(Text("assert "), rdescript="Python: Assert"),
        "list (comprehension | comp)":
            R(Text("[x for x in TOKEN if TOKEN]"),
              rdescript="Python: List Comprehension"),
        
        "[dot] (pie | pi)":
            R(Text(".py"), rdescript="Python: .py"),
        "toml":
            R(Text("toml"), rdescript="Python: toml"),
        "jason":
            R(Text("toml"), rdescript="Python: json"),
        "identity is":
            R(Text(" is "), rdescript="Python: is"),
        "yield":
            R(Text("yield "), rdescript="Python: Yield"),
        
        # Essentially an improved version of the try catch command above
            # probably a better option than this is to use snippets with tab stops 
            # VS code has the extension Python-snippets. these are activated by 
            # going into the command pallet (cs-p) and typing in "insert snippet"
            # then press enter and then you have choices of snippets show up in the drop-down list.
            # you can also make your own snippets.
        "try [<exception>]": 
            R(Text("try : ") + Pause("10") + Key("enter/2") 
            + Text("except %(exception)s:") + Pause("10") + Key("enter/2"),
                rdescript="create 'try catch' block with given exception"),
        "try [<exception>] as": 
            R(Text("try :") + Pause("10") + Key("enter/2") + Text("except %(exception)s as :")
            + Pause("10") + Key("enter/2"),  rdescript="create 'try catch as' block with given exception"),

        # class and class methods
        "subclass": R(Text("class ():") + Key("left:3"), rdescript="Python: Subclass"),
        "dunder": R(Text("____()") + Key("left:4"),  rdescript="Python: Special Method"),
        "initial": R(Text("__init__()"),  rdescript="Python: Init"),
        "meth [<binary_meth>]": R(Text("def __%(binary_meth)s__(self, other):"), 
            rdescript="Python: Binary Special Method"),     
        "meth [<unary_meth>]": R(Text("def __%(unary_meth)s__(self):"), 
            rdescript="Python: Unary Special Method"),     

        # Python vocabulary
        "word <python_keyword>": 
            R(Text(" %(python_keyword)s "), rdescript="Python: keyword"),
        "builtin <python_builtin>": 
            R(Text(" %(python_builtin)s "), rdescript="Python: builtin"),
        "standard <python_standard_library_module>": 
            R(Text(" %(python_standard_library_module)s "), rdescript="type name of Python standard library module"),
        "lib <python_library>": 
            R(Text(" %(python_library)s "),  rdescript="type name of Python nonstandard library"),
        "import <python_standard_library_module>": 
            R(Text("import %(python_standard_library_module)s "), rdescript="import module from Python standard library"),
        "import <python_library>":
            R(Text("import %(python_library)s "), rdescript="important nonstandard library"),
    }

    extras = [
        Dictation("text"),
        Choice(
            "python_keyword",
            {
                "and": "and",
                "as": "as",
                "assert": "assert",
                "async": "async",
                "await": "await",
                "break": "break",
                "class": "class",
                "continue": "continue",
                "def": "def",
                "del": "del",
                "else if": "elif",
                "else": "else",
                "except": "except",
                "finally": "finally",
                "for": "for",
                "from": "from",
                "global": "global",
                "if": "if",
                "import": "import",
                "in": "in",
                "is": "is",
                "lambda": "lambda",
                "non local": "nonlocal",
                "not": "not",
                "or": "or",
                "pass": "pass",
                "raise": "raise",
                "return": "return",
                "try": "try",
                "while": "while",
                "with": "with",
                "yield": "yield",
            },
        ),
        Choice(
            "unary_meth", {"reper": "repr", "stir": "str", "len": "len", "name": "name",
                "Unicode": "unicode", "size of": "sizeof", "dir": "dir", "int": "int"}
        ),
        Choice("binary_meth", {"add": "add", "subtract": "sub", "equal": "eq",
            "strict less": "lt", "strict greater": "gt",  "less equal": "le", "greater equal": "ge" }),
        Choice(
            "exception",
            {
                "exception": "Exception",
                "stop iteration": "StopIteration",
                "system exit": "SystemExit",
                "standard": "StandardError",
                "arithmetic": "ArithmeticError",
                "overflow": "OverflowError",
                "floating-point": "FloatingPointError",
                "zero division": "ZeroDivisionError",
                "assertion": "AssertionError",
                "EOF": "EOFError",
                "import": "ImportError",
                "keyboard interrupt": "KeyboardInterrupt",
                "lookup": "LookupError",
                "index": "IndexError",
                "key": "KeyError",
                "name": "NameError",
                "unbound local": "UnboundLocalError",
                "environment": "EnvironmentError",
                "IO": "IOError",
                "OS": "OSError",
                "syntax": "SyntaxError",
                "system exit": "SystemExit",
                "type": "TypeError",
                "value": "ValueError",
                "runtime": "RuntimeError",
                "not implemented": "NotImplementedError",
                "tab error": "TabError",
            },
        ),
        Choice(
            "python_builtin",
            {
               
                "I PYTHON": "__IPYTHON__",
                "build class": "__build_class__",
                "debug": "__debug__",
                "doc": "__doc__",
                "import": "__import__",
                "loader": "__loader__",
                "name": "__name__",
                "package": "__package__",
                "spec": "__spec__",
                "abs": "abs",
                "all": "all",
                "any": "any",
                "ascii": "ascii",
                "bin": "bin",
                "bool": "bool",
                "breakpoint": "breakpoint",
                "bytearray": "bytearray",
                "bytes": "bytes",
                # "callable": "callable",
                # "chr": "chr",
                # "classmethod": "classmethod",
                # "compile": "compile",
                # "complex": "complex",
                # "copyright": "copyright",
                # "credits": "credits",
                # "del atter": "delattr",
                # "dict": "dict",
                # "dir": "dir",
                # "display": "display",
                # "divmod": "divmod",
                # "enumerate": "enumerate",
                # "eval": "eval",
                # "exec": "exec",
                # "filter": "filter",
                # "float": "float",
                # "format": "format",
                # "frozen set": "frozenset",
                # "get ipython": "get_ipython",
                # "get atter": "getattr",
                # "globals": "globals",
                # "has atter": "hasattr",
                # "hash": "hash",
                # "help": "help",
                # "hex": "hex",
                # "id": "id",
                # "input": "input",
                # "int": "int",
                # "is instance": "isinstance",
                # "is subclass": "issubclass",
                # "iter": "iter",
                # "len": "len",
                # "license": "license",
                # "list": "list",
                # "locals": "locals",
                # "map": "map",
                # "max": "max",
                # "memory view": "memoryview",
                # "min": "min",
                # "next": "next",
                # "object": "object",
                # "oct": "oct",
                # "open": "open",
                # "ord": "ord",
                # "pow": "pow",
                # "print": "print",
                # "property": "property",
                # "range": "range",
                # "repr": "repr",
                # "reversed": "reversed",
                # "round": "round",
                # "set": "set",
                # "set atter": "setattr",
                # "slice": "slice",
                # "sorted": "sorted",
                # "static method": "staticmethod",
                # "stir": "str",
                # "sum": "sum",
                # "super": "super",
                # "tuple": "tuple",
                # "type": "type",
                # "vars": "vars",
                # "zip": "zip",
            },
        ),
        Choice(
            "python_standard_library_module",
            {
                "string": "string",
                "regex": "re",
                "diff lib": "difflib",
                "text wrap": "textwrap",
                "unicode data": "unicodedata",
                "struct": "struct",
                "codecs": "codecs",
                "date time": "datetime",
                "collections": "collections",
                "heap que": "heapq",
                "bisect": "bisect",
                "weak ref": "weakref",
                "types": "types",
                "copy": "copy",
                "pretty print": "pprint",
                "enum": "enum",
                "numbers": "numbers",
                "math": "math",
                "decimal": "decimal",
                "fractions": "fractions",
                "itertools": "itertools",
                "function tools": "functools",
                # "operator": "operator",
                # "path lib": "pathlib",
                # "temp file": "tempfile",
                # "glob": "glob",
                # "line cache": "linecache",
                # "shutil": "shutil",
                # "pickle": "pickle",
                # "sqlite 3": "sqlite3",
                # "zip file": "zipfile",
                # "tar file": "tarfile",
                # "CSV": "csv",
                # "config parser": "configparser",
                # "hash lib": "hashlib",
                # "secrets": "secrets",
                # "OS": "os",
                # "IO": "io",
                # "time": "time",
                # "arg parse": "argparse",
                # "logging": "logging",
                # "get pass": "getpass",
                # "platform": "platform",
                # "C types": "ctypes",
                # "threading": "threading",
                # "multiprocessing": "multiprocessing",
                # "concurrent": "concurrent",
                # "concurrent futures": "concurrent.futures",
                # "subprocess": "subprocess",
                # "queue": "queue",
                # "context vars": "contextvars",
                # "asyncio": "asyncio",
                # "json": "json",
                # "base64": "base64",
                # "bin ascky": "binascii",
                # "url lib parse": "urllib.parse",
                # "get text": "gettext",
                # "locale": "locale",
                # "shlex": "shlex",
                # "typing": "typing",
                # "unit test": "unittest",
                # "time it": "timeit",
                # "trace": "trace",
                # "dist utils": "distutils",
                # "zip app": "zipapp",
                # "sys": "sys",
                # "builtins": "builtins",
                # "warnings": "warnings",
                # "data classes": "dataclasses",
                # "context lib": "contextlib",
                # "ABC": "abc",
                # "atexit": "atexit",
                # "traceback": "traceback",
                # "future": "__future__",
                # "GC": "gc",
                # "inspect": "inspect",
                # "site": "site",
                # "import lib": "importlib",
                # "ast": "ast",
                # "token": "token",
                # "tokenize": "tokenize",
                # "dis": "dis",
            },
        ),
        Choice("python_library", {
                "Requests": "Requests",
                "skappy": "Scapy",
                "w x Python": "wxPython",
                "Pillow": "Pillow",
                "SQL Alchemy": "SQLAlchemy",
                "beautiful soup": "BeautifulSoup",
                "sim pie": "SymPy",
                # "Twisted": "Twisted",
                # "num pie": "NumPy",
                # "sigh pie": "SciPy",
                # "mat plot lib": "matplotlib",
                # "pie game": "Pygame",
                # "Piglet": "Pyglet",
                # "pie QT": "pyQT",
                # "pandas": "pandas",
                # "kivy": "kivy",
                # "jango": "Django",
                # "click": "click"
        }),
    ]
    defaults = {"unary_meth": "", "binary_meth": "", "exception": ""}


control.nexus().merger.add_global_rule(Python(ID=100))
