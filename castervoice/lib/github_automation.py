# -*- coding: utf-8 -*-

import io
import os
import shutil
import sys
import traceback
from __builtin__ import True
from subprocess import Popen
import toml
import time

from castervoice.lib.actions import Key, Text
from castervoice.lib.context import read_selected_without_altering_clipboard
from castervoice.lib.utilities import load_toml_file
from castervoice.lib import settings
from castervoice.lib.ccr.recording.bringme import _rebuild_items

_USER_DIR = os.path.expanduser("~").replace("\\", "/") + "/.caster"

if os.path.isfile(settings.SETTINGS["paths"]["GIT_FOLDER_REMOTE_URL_PATH"]) is False:
    git_match_default = settings.SETTINGS["paths"]["GIT_FOLDER_REMOTE_URL_DEFAULT_PATH"]
    git_match_user = settings.SETTINGS["paths"]["GIT_FOLDER_REMOTE_URL_PATH"]
    shutil.copy(git_match_default, git_match_user)

def rebuild_local_remote_items(config):
    # logger.debug('Github rebuilding extras')
    return {
        key: (os.path.expandvars(value), header)
        for header, section in config.iteritems() for key, value in section.iteritems()
    }

def github_checkoutupdate_pull_request(new):
    # Function to fetch a PR
    try:
        import natlink
        if context:
            print("Checking out pull request locally.")
            Key("c-l/20").execute()
            print("Checking out pull request locally 2.")
            url = read_selected_without_altering_clipboard()
            print(url[1])
            if url[0] == 0:
                split_string = url[1].split("/pull/")
                repo_url = split_string[0]
                pr_name = split_string[1]
                CONFIG = load_toml_file(settings.SETTINGS["paths"]["GIT_FOLDER_REMOTE_URL_PATH"])
                if not CONFIG:
                    # logger.warn("Could not load bringme defaults")
                    raise Exception("Could not load local_remote_git_match.toml")

                items = rebuild_local_remote_items(CONFIG)
                if repo_url in items:
                    local_directory = items[repo_url][0]
                    print(local_directory)
                    local_directory = local_directory.replace("\\", "\\\\")
                    print(local_directory)
                    # needs a settings path entry for git-bash.exe or preferred terminal?
                    TERMINAL_PATH = settings.SETTINGS["paths"]["TERMINAL_PATH"]
                    fetch_command = "git fetch " + repo_url + ".git pull/" + pr_name + "/head"
                    if TERMINAL_PATH != "":
                        terminal = Popen(TERMINAL_PATH, cwd=local_directory)
                                            # This can be improved with a wait command
                        time.sleep(2)
                        print("Checking out pull request locally 3.")
                        Text(fetch_command).execute()
                        time.sleep(0.2)
                        print("Checking out pull request locally 4.")
                        Key("enter").execute() # fetch is safe enough so will run this
                        time.sleep(0.2)
                        if new:
                            print("Checking out pull request locally 5.")
                            branch_name_base = repo_url.replace("https://github.com/", "")
                            checkout_command = "git checkout -b " + branch_name_base + "/pull/" + pr_name + " FETCH_HEAD"
                            Text(checkout_command).execute()
                        else:
                            print("Checking out pull request locally 5.")
                            branch_name_base = repo_url.replace("https://github.com/", "")
                            checkout_command = "git checkout " + branch_name_base + "/pull/" + pr_name
                            Text(checkout_command).execute()
                            Key("enter").execute() # checkout is safe enough so will run this
                            merge_command = "git merge FETCH_HEAD"
                            time.sleep(0.2)
                            Text(merge_command).execute()
                    else:
                        raise Exception('TERMINAL_PATH in <user_dir>/.caster/data/settings.toml is not set')
                else:
                    raise Exception("Repository not found in " + settings.SETTINGS["paths"]["GIT_FOLDER_REMOTE_URL_PATH"])
    except Exception as e:
        print (e)
