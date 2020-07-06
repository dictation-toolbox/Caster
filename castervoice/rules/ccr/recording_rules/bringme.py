import os
import sys
import shlex
import threading
import time
from subprocess import Popen
import re

import six
if six.PY2:
    from castervoice.lib.util.pathlib import Path
else:
    from pathlib import Path  # pylint: disable=import-error

from dragonfly import Function, Choice, Dictation, ContextAction
from castervoice.lib.context import AppContext

from castervoice.lib import settings, utilities, context, contexts
from castervoice.lib import printer
from castervoice.lib.actions import Text, Key
from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.selfmod.selfmodrule import BaseSelfModifyingRule
from castervoice.lib.merge.state.short import R


class BringRule(BaseSelfModifyingRule):
    """
    BringRule adds entries to a 2-layered map which can be described as
    {type: {extra: target}}
    type: used for internal organization; types include website, file, folder, etc.
    extra: the word or words used to label the target
    target: a url or file/folder location
    """

    pronunciation = "bring me"

    # Contexts
    _browser_context = AppContext(["chrome", "firefox"])
    _explorer_context = AppContext("explorer.exe") | contexts.DIALOGUE_CONTEXT
    _terminal_context = contexts.TERMINAL_CONTEXT
    # Paths
    _terminal_path = settings.settings(["paths", "TERMINAL_PATH"])
    _explorer_path = str(Path("C:\\Windows\\explorer.exe"))
    _source_dir =  Path(settings.SETTINGS["paths"]["BASE_PATH"]).parents[0]
    _user_dir = settings.SETTINGS["paths"]["USER_DIR"]
    _home_dir = Path.home()

    def __init__(self, **kwargs):
        super(BringRule, self).__init__(settings.settings(["paths", "SM_BRINGME_PATH"]), **kwargs)

    def _initialize(self):
        """
        Sets up defaults for first time only.
        """
        if len(self._config.get_copy()) == 0:
            self._bring_reset_defaults()

    def _deserialize(self):
        """
        This _deserialize creates mapping which uses the user-made extras.
        """
        self._initialize()

        self._smr_mapping = {
            "bring me <program>": R(Function(self._bring_program)),
            "bring me <website>": R(Function(self._bring_website)),
            "bring me <folder> [in <app>]": R(Function(self._bring_folder)),
            "bring me <file>": R(Function(self._bring_file)),
            "refresh bring me": R(Function(self._load_and_refresh)),
            "<launch_type> to bring me as <key>": R(Function(self._bring_add)),
            "to bring me as <key>": R(Function(self._bring_add_auto)),
            "remove <key> from bring me": R(Function(self._bring_remove)),
            "restore bring me defaults": R(Function(self._bring_reset_defaults)),
        }
        self._smr_extras = [
            Choice(
                "launch_type", {
                    "[current] program": "program",
                    "website": "website",
                    "folder": "folder",
                    "file": "file",
                }),
            Choice("app", {
                "terminal": "terminal",
                "explorer": "explorer",
            }),
            # Sanitize free dictation for spec, words and apostrophes only.
            Dictation("key").apply(lambda key: re.sub(r'[^A-Za-z\'\s]+', '', key).lower()),
        ]
        self._smr_extras.extend(self._rebuild_items())
        self._smr_defaults = {"app": None}

    def _rebuild_items(self):
        # E.g. [Choice("folder", {"my pictures": ...}), ...]
        config_copy = self._config.get_copy()
        return [
            Choice(header,
                   {key: os.path.expandvars(value)
                    for key, value in section.items()})
            for header, section in config_copy.items()
        ]

    def _refresh(self, *args):
        """
        :param args: in this case, args is the pre-altered copy of the state map to replace the current map with
        """
        self._config.replace(args[0])
        self.reset()

    def _load_and_refresh(self):
        """

        """
        self.reset()

    def _bring_add(self, launch_type, key):
        # Add current program or highlighted text to bring me
        if launch_type == "program":
            path = utilities.get_active_window_path()
            if not path:
                # dragonfly.get_current_engine().speak("program not detected")
                printer.out("Program path for bring me not found ")
        elif launch_type == 'file':
            files = utilities.get_selected_files(folders=False)
            path = files[0] if files else None # or allow adding multiple files
        elif launch_type == 'folder':
            files = utilities.get_selected_files(folders=True)
            path = files[0] if files else None # or allow adding multiple folders
        else:
            Key("a-d/5").execute()
            fail, path = context.read_selected_without_altering_clipboard()
            if fail == 2:
                # FIXME: A better solution would be to specify a number of retries and the time interval.
                time.sleep(0.1)
                _, path = context.read_selected_without_altering_clipboard()
                if not path:
                    printer.out("Selection for bring me not found ")
            Key("escape").execute()
        if not path:
            # logger.warn('Cannot add %s as %s to bringme: cannot get path', launch, key)
            return

        config_copy = self._config.get_copy()
        config_copy[launch_type][str(key)] = path
        self._refresh(config_copy)

    def _bring_remove(self, key):
        # Remove item from bring me
        config_copy = self._config.get_copy()
        deleted = False
        key = str(key)
        for section in config_copy.keys():
            if key in config_copy[section]:
                del config_copy[section][key]
                deleted = True
                break
        if deleted:
            self._refresh(config_copy)

    def _bring_reset_defaults(self):
        """
        Restore bring me list to defaults
        """
        self._refresh(BringRule._bm_defaults)

    def _bring_add_auto(self, key):
        """
        Adds an entry for a program, a website, or a folder (without specifying),
        depending on which context get detected (if either).
        """
        def add(launch_type):
            return Function(lambda: self._bring_add(launch_type, key))

        ContextAction(add("program"), [
            (BringRule._browser_context, add("website")),
            (BringRule._explorer_context, add("folder")),
        ]).execute()

    # =================== BringMe actions --> these do not change state

    def _bring_website(self, website):
        browser = utilities.default_browser_command()
        Popen(shlex.split(browser.replace('%1', website)))

    def _bring_folder(self, folder, app):
        if not app:
            ContextAction(Function(lambda: Popen([BringRule._explorer_path, folder])), [
                (BringRule._terminal_context, Text("cd \"%s\"\n" % folder)),
                (BringRule._explorer_context, Key("c-l/5") + Text("%s\n" % folder))
            ]).execute()
        elif app == "terminal":
            Popen([BringRule._terminal_path, "--cd=" + folder.replace("\\", "/")])
        elif app == "explorer":
            Popen([BringRule._explorer_path, folder])

    def _bring_program(self, program):
        Popen(program)

    def _bring_file(self, file):
        threading.Thread(target=os.startfile, args=(file, )).start()  # pylint: disable=no-member

    # =================== BringMe default setup:
    _bm_defaults = {
        "website": {
            # Documentation
            "caster documentation": "https://caster.readthedocs.io/en/latest/",
            "dragonfly documentation": "https://dragonfly2.readthedocs.io/en/latest/",

            # Caster Support
            "dragonfly gitter": "https://gitter.im/dictation-toolbox/dragonfly",
            "caster gitter": "https://gitter.im/dictation-toolbox/Caster",
            "caster discord": "https://discord.gg/9eAAsCJ",

            # General URLs
            "google": "https://www.google.com",
        },
        "folder": {
            # OS folder Navigation
            "libraries | home": str(Path(_home_dir)),
            "my pictures": str(Path(_home_dir).joinpath("Pictures")),
            "my documents": str(Path(_home_dir).joinpath("Documents")),

            # Caster User Dir Navigation
            "caster source": str(Path(_source_dir)),
            "caster user": str(Path(_user_dir)),
            "caster hooks": str(Path(_user_dir).joinpath("hooks")),
            "caster transformers": str(Path(_user_dir).joinpath("transformers")),
            "caster rules": str(Path(_user_dir).joinpath("rules")),
            "caster data": str(Path(_user_dir).joinpath("data")),
            "caster settings": str(Path(_user_dir).joinpath("settings")),
            "sick you lee": str(Path(_user_dir).joinpath("sikuli")),
        },
        "program": {
            "notepad": str(Path("C:\\Windows\\notepad.exe")),
        },
        "file": {
            # User Settings
            "caster settings file": str(Path(_user_dir).joinpath("settings/settings.toml")),
            "caster rules file": str(Path(_user_dir).joinpath("settings/rules.toml")),
            "caster bring me file": str(Path(_user_dir).joinpath("settings/sm_bringme.toml")),
            "caster hooks file": str(Path(_user_dir).joinpath("settings/hooks.toml")),
            "caster companion file": str(Path(_user_dir).joinpath("settings/companion_config.toml")),
            "caster transformers file": str(Path(_user_dir).joinpath("settings/transformers.toml")),

            # Caster Data
            "caster alias file": str(Path(_user_dir).joinpath("data/sm_aliases.toml")),
            "caster chain aliases file": str(Path(_user_dir).joinpath("data/sm_chain_aliases.toml")),
            "caster clipboard file": str(Path(_user_dir).joinpath("data/clipboard.json")),
            "caster record from history file": str(Path(_user_dir).joinpath("data/sm_history.toml")),
            "caster log file": str(Path(_user_dir).joinpath("log.txt")),

            # Simplified Transformer
            "caster transformer file": str(Path(_user_dir).joinpath("transformers/words.txt")),
        }
    }

def get_rule():
    details = RuleDetails(name="bring me",
                          transformer_exclusion=True)
    return [BringRule, details]
