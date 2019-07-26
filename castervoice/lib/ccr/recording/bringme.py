from castervoice.lib.imports import *
from castervoice.apps.gitbash import terminal_context
from castervoice.apps.file_dialogue import dialogue_context


class BringRule(SelfModifyingRule):
    pronunciation = "bring me"

    def refresh(self):
        self.mapping = {
            "bring me <program>": R(Function(self.bring_program)),
            "bring me <website>": R(Function(self.bring_website)),
            "bring me <folder> [in <app>]": R(Function(self.bring_folder)),
            "bring me <file>": R(Function(self.bring_file)),
            "refresh bring me": R(Function(self.load_and_refresh)),
            "<launch> to bring me as <key>": R(Function(self.bring_add)),
            "to bring me as <key>": R(Function(self.bring_add_auto)),
            "remove <key> from bring me": R(Function(self.bring_remove)),
            "restore bring me defaults": R(Function(self.bring_restore)),
        }
        self.extras = [
            Choice(
                "launch", {
                    "[current] program": "program",
                    "website": "website",
                    "folder": "folder",
                    "file": "file",
                }),
            Choice("app", {
                "terminal": "terminal",
                "explorer": "explorer",
            }),
            Dictation("key"),
        ]
        self.extras.extend(self._rebuild_items())
        self.defaults = {"app": None}
        self.reset(self.mapping)

    def __init__(self):
        # Contexts
        self.browser_context = AppContext(["chrome", "firefox"])
        self.explorer_context = AppContext("explorer.exe") | dialogue_context
        self.terminal_context = terminal_context
        # Paths
        self.config_path = settings.SETTINGS["paths"]["BRINGME_PATH"]
        self.defaults_path = settings.SETTINGS["paths"]["BRINGME_DEFAULTS_PATH"]
        self.terminal_path = settings.SETTINGS["paths"]["TERMINAL_PATH"]
        self.explorer_path = "C:\\Windows\\explorer.exe"
        # Get things set up
        self.config = {}
        self.load_config()
        SelfModifyingRule.__init__(self)

    def bring_website(self, website):
        browser = utilities.default_browser_command()
        Popen(shlex.split(browser.replace('%1', website)))

    def bring_folder(self, folder, app):
        if not app:
            ContextAction(Function(lambda: Popen([self.explorer_path, folder])), [
                (self.terminal_context, Text("cd \"%s\"\n" % folder)),
                (self.explorer_context, Key("c-l/5") + Text("%s\n" % folder))
            ]).execute()
        elif app == "terminal":
            Popen([self.terminal_path, "--cd=" + folder.replace("\\", "/")])
        elif app == "explorer":
            Popen([self.explorer_path, folder])

    def bring_program(self, program):
        Popen(program)

    def bring_file(self, file):
        threading.Thread(target=os.startfile, args=(file, )).start()

    def bring_add(self, launch, key):
        # Add current program or highlighted text to bring me
        key = str(key)
        if launch == "program":
            path = utilities.get_active_window_path()
            if not path:
                # dragonfly.get_engine().speak("program not detected")
                print("Program path for bring me not found ")
        elif launch == 'file':
            files = utilities.get_selected_files(folders=False)
            path = files[0] if files else None # or allow adding multiple files
        elif launch == 'folder':
            files = utilities.get_selected_files(folders=True)
            path = files[0] if files else None # or allow adding multiple folders
        else:
            Key("a-d/5").execute()
            fail, path = context.read_selected_without_altering_clipboard()
            if fail == 2:
                # FIXME
                time.sleep(0.1)
                _, path = context.read_selected_without_altering_clipboard()
                if not path:
                    # dragonfly.get_engine().speak("nothing selected")
                    print("Selection for bring me not found ")
            Key("escape").execute()
        if not path:
            # logger.warn('Cannot add %s as %s to bringme: cannot get path', launch, key)
            return
        self.config[launch][key] = path
        self.save_config()
        self.refresh()

    def bring_add_auto(self, key):
        def add(launch):
            return Function(lambda: self.bring_add(launch, key))

        ContextAction(add("program"), [
            (self.browser_context, add("website")),
            (self.explorer_context, add("folder")),
        ]).execute()

    def bring_remove(self, key):
        # Remove item from bring me
        key = str(key)
        for section in self.config.keys():
            if key in self.config[section]:
                del self.config[section][key]
                self.save_config()
                self.refresh()
                return

    def _rebuild_items(self):
        # E.g. [Choice("folder", {"my pictures": ...}), ...]
        return [
            Choice(header,
                   {key: os.path.expandvars(value)
                    for key, value in section.iteritems()})
            for header, section in self.config.iteritems()
        ]

    def load_and_refresh(self):
        self.load_config()
        self.refresh()

    def load_config(self):
        if os.path.isfile(self.config_path) is False:
            self.bring_restore(startup=True)
        else:
            self.config = utilities.load_toml_file(self.config_path)
        if not self.config:
            print("Could not load bringme defaults")

    def save_config(self):
        utilities.save_toml_file(self.config, self.config_path)

    def bring_restore(self, startup=False):
        # Restore bring me list to defaults
        self.config = self.bm_defaults
        self.save_config()
        if not startup:
            self.refresh()

    bm_defaults = {
        "website": {
            "caster documentation": "https://caster.readthedocs.io/en/latest/",
            "dragonfly documentation": "https://dragonfly2.readthedocs.io/en/latest/",
            "dragonfly gitter": "https://gitter.im/dictation-toolbox/dragonfly",
            "caster gitter": "https://gitter.im/dictation-toolbox/Caster",
            "caster discord": "https://discord.gg/9eAAsCJr",
            "google": "https://www.google.com",
        },
        "folder": {
            "libraries": "%USERPROFILE%",
            "my pictures": "%USERPROFILE%\\Pictures",
            "my documents": "%USERPROFILE%\\Documents",
            "caster user": "%USERPROFILE%\\.caster",
            "caster filters": "%USERPROFILE%\\.caster\\filters",
            "caster rules": "%USERPROFILE%\\.caster\\rules",
            "caster data": "%USERPROFILE%\\.caster\\data",
            "sick you lee": "%USERPROFILE%\\.caster\\sikuli",
        },
        "program": {
            "notepad": "C:\\Windows\\notepad.exe",
        },
        "file": {
            "caster settings": "%USERPROFILE%\\.caster\\data\\settings.toml",
            "caster alias": "%USERPROFILE%\\.caster\\data\\aliases.toml",
            "caster bring me": "%USERPROFILE%\\.caster\\data\\bringme.toml",
            "caster ccr": "%USERPROFILE%\\.caster\\data\\ccr.toml",
            "caster config debug": "%USERPROFILE%\\.caster\\data\\configdebug.txt",
            "caster words": "%USERPROFILE%\\.caster\\filter\\words.txt",
            "caster log": "%USERPROFILE%\\.caster\\data\\log.txt",
        }
    }


control.non_ccr_app_rule(BringRule(), context=None, rdp=False, filter=True)
