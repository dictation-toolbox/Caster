# -*- coding: utf-8 -*-

import io
import os
# import re
import sys
import traceback
from __builtin__ import True
from subprocess import Popen
import toml
import time

from castervoice.lib.actions import Key, Text
from castervoice.lib.context import AppContext, read_selected_without_altering_clipboard
from castervoice.lib.utilities import load_toml_file
from castervoice.lib import settings

_USER_DIR = os.path.expanduser("~").replace("\\", "/") + "/.caster"

def _rebuild_items(config):
    # logger.debug('Bring me rebuilding extras')
    return {
        key: (os.path.expandvars(value), header)
        for header, section in config.iteritems() for key, value in section.iteritems()
    }

def github_branch_pull_request():
    # Function to fetch a PR and make a new branch
    try:
        import natlink
        context = AppContext(executable="chrome") | AppContext(executable="iexplore") | AppContext(executable="firefox")
        if context:
            print("Checking out pull request locally.")
            Key("c-l/20").execute()
            print("Checking out pull request locally 2.")
            url = read_selected_without_altering_clipboard()
            print(url[1])
            if url[0] == 0:
                split_string = url[1].split("/pull/")
                CONFIG = load_toml_file(_USER_DIR + "/data/local_remote_git_match.toml")
                items = _rebuild_items(CONFIG)
                local_directory = items[split_string[0]][0]
                print(local_directory)
                local_directory = local_directory.replace("\\", "\\\\")
                print(local_directory)
                # needs a settings path entry for git-bash.exe or preferred terminal?
                TERMINAL_PATH = settings.SETTINGS["paths"]["TERMINAL_PATH"]
                if TERMINAL_PATH != "":
                    terminal = Popen(TERMINAL_PATH)
                else:
                    raise Exception('TERMINAL_PATH in <user_dir>/.caster/data/settings.toml is not set')
                # This can be improved with a wait command
                time.sleep(2)
                print("Checking out pull request locally 3.")
                Text("cd ").execute()
                time.sleep(0.2)
                print("Checking out pull request locally 4.")
                Text(local_directory).execute()
                time.sleep(0.2)
                print("Checking out pull request locally 5.")
                Key("enter").execute()
                time.sleep(0.2)
                print("Checking out pull request locally 6.")
                fetch_command = "git fetch " + split_string[0] + ".git pull/" + split_string[1] + "/head"
                Text(fetch_command).execute()
                time.sleep(0.2)
                print("Checking out pull request locally 7.")
                Key("enter").execute() # fetch is safe enough so will run this
                time.sleep(0.2)
                print("Checking out pull request locally 8.")
                split_string[0] = split_string[0].replace("https://github.com/", "")
                checkout_command = "git checkout -b " + split_string[0] + "/pull/" + split_string[1] + " FETCH_HEAD"
                Text(checkout_command).execute()
            # Still need to add stuff like this:
            # CONFIG = utilities.load_toml_file(settings.SETTINGS["paths"]["BRINGME_PATH"])
# if not CONFIG:
    # CONFIG = utilities.load_toml_file(settings.SETTINGS["paths"]["BRINGME_DEFAULTS_PATH"])
# if not CONFIG:
    #logger.warn("Could not load bringme defaults")
    # print("Could not load bringme defaults")
    # print("Could not load bringme defaults")
    except Exception as e:
        print (e)
