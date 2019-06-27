from castervoice.lib.imports import *
from castervoice.apps.gitbash import terminal_context

class BringRule(SelfModifyingRule):
    pronunciation = "bring me"

    def refresh(self):
        self.mapping = {
            "bring me <desired_item>":
                R(Function(self.bring_it)),
            "<launch> to bring me as <key>":
                R(Function(self.bring_add, extra={"launch", "key"})),
            "remove <key> from bring me":
                R(Function(self.bring_remove, extra="key")),
            "restore bring me defaults":
                R(Function(self.bring_restore)),
        }
        self.extras = [
            Choice("desired_item", self._rebuild_items()),
            Choice(
                "launch", {
                    "[current] program": "program",
                    "website": "website",
                    "folder": "folder",
                    "file": "file",
                }),
            Dictation("key"),
        ]
        self.reset(self.mapping)

    def __init__(self):
        self.config_path = settings.SETTINGS["paths"]["BRINGME_PATH"]
        self.defaults_path = settings.SETTINGS["paths"]["BRINGME_DEFAULTS_PATH"]
        self.config = {}
        self.load_config()
        SelfModifyingRule.__init__(self)


    # module functions
    def bring_it(self, desired_item):
        '''
        Currently simply invoke os.startfile. New thread keeps Dragon from crashing.
        '''
        item, item_type = desired_item
        if item_type == "website":
            browser = utilities.default_browser_command()
            subprocess.Popen(shlex.split(browser.replace('%1', item)))
        elif item_type == 'folder':
            ContextAction(
                Function(lambda: subprocess.Popen([r'C:\Windows\explorer.exe', item])),
                [(terminal_context, Text("cd \"%s\"\n" % item)),
                (AppContext("explorer.exe"), Key("c-l/5") + Text("%s\n" % item))
                ]).execute()

        elif item_type == 'program':
            subprocess.Popen(item)
        else:
            threading.Thread(target=os.startfile, args=(item, )).start()

    def bring_add(self, launch, key):
        # Add current program or highlighted text to bring me
        key = str(key)
        if launch == "program":
            path = utilities.get_active_window_path()
            if not path:
                # dragonfly.get_engine().speak("program not detected")
                print("Program path for bring me not found ")
        # elif launch == 'file':
        # no way to add file via pyperclip
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

    def bring_remove(self, key):
        # Remove item from bring me
        key = str(key)
        for section in self.config.keys():
            if key in self.config[section]:
                del self.config[section][key]
                self.save_config()
                self.refresh()
                return

    def bring_restore(self):
        # Restore bring me list to defaults
        self.config = utilities.load_toml_file(self.defaults_path)
        self.refresh()

    def _rebuild_items(self):
        # logger.debug('Bring me rebuilding extras')
        return {
            key: (os.path.expandvars(value), header)
            for header, section in self.config.iteritems()
            for key, value in section.iteritems()
        }

    def load_config(self):
        if os.path.isfile(self.config_path) is False:
            shutil.copy(self.defaults_path, self.config_path)

        self.config = utilities.load_toml_file(self.config_path)
        if not self.config:
            print("Could not load bringme defaults")

    def save_config(self):
        utilities.save_toml_file(self.config, self.config_path)

control.non_ccr_app_rule(BringRule(), context=None, rdp=False)
