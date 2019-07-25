from castervoice.lib.dfplus.selfmod.selfmodrule import BaseSelfModifyingRule
from castervoice.lib.imports import *
from castervoice.apps.gitbash import terminal_context
from castervoice.apps.file_dialogue import dialogue_context


class BringRule(BaseSelfModifyingRule):
    pronunciation = "bring me"

    def __init__(self):
        # Contexts
        self._browser_context = AppContext(["chrome", "firefox"])
        self._explorer_context = AppContext("explorer.exe") | dialogue_context
        self._terminal_context = terminal_context
        # Paths
        self._config_path = settings.SETTINGS["paths"]["BRINGME_PATH"]
        self._terminal_path = settings.SETTINGS["paths"]["TERMINAL_PATH"]
        self._explorer_path = "C:\\Windows\\explorer.exe"
        # Get things set up
        self._config = {}
        self._load_config()
        SelfModifyingRule.__init__(self)

    def _refresh(self):
        self._smr_mapping = {
            "bring me <program>": R(Function(self._bring_program)),
            "bring me <website>": R(Function(self._bring_website)),
            "bring me <folder> [in <app>]": R(Function(self._bring_folder)),
            "bring me <file>": R(Function(self._bring_file)),
            "refresh bring me": R(Function(self._load_and_refresh)),
            "<launch> to bring me as <key>": R(Function(self._bring_add)),
            "to bring me as <key>": R(Function(self._bring_add_auto)),
            "remove <key> from bring me": R(Function(self._bring_remove)),
            "restore bring me defaults": R(Function(self._bring_reset_defaults)),
        }
        self._smr_extras = [
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
        self._smr_extras.extend(self._rebuild_items())
        self._smr_defaults = {"app": None}
        self.reset()

    def _bring_website(self, website):
        browser = utilities.default_browser_command()
        Popen(shlex.split(browser.replace('%1', website)))

    def _bring_folder(self, folder, app):
        if not app:
            ContextAction(Function(lambda: Popen([self._explorer_path, folder])), [
                (self._terminal_context, Text("cd \"%s\"\n" % folder)),
                (self._explorer_context, Key("c-l/5") + Text("%s\n" % folder))
            ]).execute()
        elif app == "terminal":
            Popen([self._terminal_path, "--cd=" + folder.replace("\\", "/")])
        elif app == "explorer":
            Popen([self._explorer_path, folder])

    def _bring_program(self, program):
        Popen(program)

    def _bring_file(self, file):
        threading.Thread(target=os.startfile, args=(file, )).start()

    def _bring_add(self, launch, key):
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
        self._config[launch][key] = path
        self._save_config()
        self._refresh()

    def _bring_add_auto(self, key):
        def add(launch):
            return Function(lambda: self._bring_add(launch, key))

        ContextAction(add("program"), [
            (self._browser_context, add("website")),
            (self._explorer_context, add("folder")),
        ]).execute()

    def _bring_remove(self, key):
        # Remove item from bring me
        key = str(key)
        for section in self._config.keys():
            if key in self._config[section]:
                del self._config[section][key]
                self._save_config()
                self._refresh()
                return

    def _rebuild_items(self):
        # E.g. [Choice("folder", {"my pictures": ...}), ...]
        return [
            Choice(header,
                   {key: os.path.expandvars(value)
                    for key, value in section.iteritems()})
            for header, section in self._config.iteritems()
        ]

    def _load_and_refresh(self):
        self._load_config()
        self._refresh()

    def _load_config(self):
        """
        Guarantees that the config file exists.
        If it doesn't, it saves it as BringRule._bm_defaults.
        """
        if os.path.isfile(self._config_path) is False:
            self._bring_reset_defaults(startup=True)
        else:
            self._config = utilities.load_toml_file(self._config_path)
        if not self._config:
            print("Could not load bringme defaults")

    def _bring_reset_defaults(self, startup=False):
        # Restore bring me list to defaults
        self._config = self._bm_defaults
        self._save_config()
        if not startup:
            self._refresh()

    _bm_defaults = {
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
            "caster transformers": "%USERPROFILE%\\.caster\\transformers",
            "caster rules": "%USERPROFILE%\\.caster\\rules",
            "caster data": "%USERPROFILE%\\.caster\\data",
            "sick you lee": "%USERPROFILE%\\.caster\\sikuli",
        },
        "program": {
            "notepad": "C:\\Windows\\notepad.exe",
        },
        "file": {
            "caster settings": "%USERPROFILE%\\.caster\\data\\settings.toml",
            "caster alias": "%USERPROFILE%\\.caster\\data\\sm_aliases.toml",
            "caster bring me": "%USERPROFILE%\\.caster\\data\\bringme.toml",
            "caster ccr": "%USERPROFILE%\\.caster\\data\\ccr.toml",
            "caster config debug": "%USERPROFILE%\\.caster\\data\\configdebug.txt",
            "caster words": "%USERPROFILE%\\.caster\\filter\\words.txt",
            "caster log": "%USERPROFILE%\\.caster\\data\\log.txt",
        }
    }


control.non_ccr_app_rule(BringRule(), context=None, rdp=False, filter=True)

def get_rule():
    '''
    TODO: make a 'Paths' object which auto-finds modules --
    it should be first-find, and only need a module name and whether this file is in the .caster dir (default False)
    this saves the user from having to use os.realpath--- that ugly mess everywhere
    -- also, get rid of location in MergeRule so the behavior can be consistent
    '''