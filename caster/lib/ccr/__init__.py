# new modules should be added in the dictionary
# the tupple contains the rules which will be imported

command_sets = {
    "bash.bash": ("Bash", ),
    "core.alphabet": ("Alphabet", ),
    "core.nav": ("Navigation", ),
    "core.numbers": ("Numbers", ),
    "core.punctuation": ("Punctuation", ),
    "cpp.cpp": ("CPP", ),
    "csharp.csharp": ("CSharp", ),
    "haxe.haxe": ("Haxe", ),
    "html.html": ("HTML", ),
    "java.java": ("Java", ),
    "javascript.javascript": ("Javascript", ),
    "matlab.matlab": ("Matlab", ),
    "python.python": ("Python", ),
    "r.r": ("Rlang", ),
    "rust.rust": ("Rust", ),
    "sql.sql": ("SQL", ),
    "prolog.prolog": ("Prolog", ),
    "vhdl.vhdl": ("VHDL", ),
    "hearthstone.hearthstone": ("Hearthstone", ),
}


for module_name,class_name_tup in command_sets.iteritems():
    for class_name in class_name_tup:
        try:
            module = __import__(module_name, globals(), locals(),[class_name])    #attempts to import the class
            globals()[class_name]= module    #make the name available globally

        except Exception as e:
            print("Ignoring ccr rule '{}'. Failed to load with: ".format(class_name))
            print(e)
