# new modules should be added in the dictionary
# the tuple contains the rules which will be imported
from castervoice.lib import utilities

command_sets = {
    "bash.bash": ("Bash", ),
    "core.alphabet": ("Alphabet", ),
    "core.nav": ("Navigation", ),
    "core.numbers": ("Numbers", ),
    "core.punctuation": ("Punctuation", ),
    "cpp.cpp": ("CPP", ),
    "csharp.csharp": ("CSharp", ),
    "dart.dart": ("Dart", ),
    "go.go": ("Go", ),
    "haxe.haxe": ("Haxe", ),
    "html.html": ("HTML", ),
    "java.java": ("Java", ),
    "javascript.javascript": ("Javascript", ),
    "latex.latex": ("LaTeX", ),
    "matlab.matlab": ("Matlab", ),
    "python.python": ("Python", ),
    "r.r": ("Rlang", ),
    "rust.rust": ("Rust", ),
    "sql.sql": ("SQL", ),
    "prolog.prolog": ("Prolog", ),
    "vhdl.vhdl": ("VHDL", ),
}

for module_name, class_name_tup in command_sets.iteritems():
    for class_name in class_name_tup:
        try:
            module = __import__(module_name, globals(), locals(),
                                [class_name])  # attempts to import the class
            globals()[class_name] = module  # make the name available globally

        except Exception as e:
            print("Ignoring ccr rule '{}'. Failed to load with: ".format(class_name))
            utilities.simple_log()
