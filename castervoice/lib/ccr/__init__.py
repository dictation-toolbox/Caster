# new modules should be added in the dictionary --- this is now outdated


# command_sets = {
#     "bash.bash": ("Bash", ),
#     "core.alphabet": ("Alphabet", ),
#     "core.nav": ("Navigation", ),
#     "core.numeric": ("Numbers", ),
#     "core.punctuation": ("Punctuation", ),
#     "core.text_manipulation": ("TextManipulation", ),
#     "cpp.cpp": ("CPP", ),
#     "csharp.csharp": ("CSharp", ),
#     "dart.dart": ("Dart", ),
#     "voice_dev_commands.voice_dev_commands": ("VoiceDevCommands"),
#     "go.go": ("Go", ),
#     "haxe.haxe": ("Haxe", ),
#     "html.html_": ("HTML", ),
#     "java.java": ("Java", ),
#     "javascript.javascript": ("Javascript", ),
#     "latex.latex": ("LaTeX", ),
#     "markdown.markdown": ("Markdown", ),
#     "matlab.matlab": ("Matlab", ),
#     "python.python": ("Python", ),
#     "r.r": ("Rlang", ),
#     "rust.rust": ("Rust", ),
#     "sql.sql": ("SQL", ),
#     "prolog.prolog": ("Prolog", ),
#     "vhdl.vhdl": ("VHDL", ),
# }

# for module_name, class_name_tup in command_sets.iteritems():
#     for class_name in class_name_tup:
#         try:
#             module = __import__(module_name, globals(), locals(),
#                                 [class_name])  # attempts to import the class
#             globals()[class_name] = module  # make the name available globally
#
#         except Exception as e:
#             print("Ignoring ccr rule '{}'. Failed to load with: ".format(class_name))
#             utilities.simple_log()
