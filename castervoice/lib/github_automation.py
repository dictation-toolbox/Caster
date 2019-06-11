# -*- coding: utf-8 -*-

import io
import os
import shutil
import sys
import traceback
from __builtin__ import True
from subprocess import Popen, PIPE
import toml
import time

from castervoice.lib.actions import Key, Text
from castervoice.lib.context import read_selected_without_altering_clipboard
from castervoice.lib.utilities import load_toml_file
from castervoice.lib import settings
from castervoice.lib.ccr.recording.bringme import _rebuild_items

_USER_DIR = os.path.expanduser("~").replace("\\", "/") + "/.caster"

if os.path.isfile(settings.SETTINGS["paths"]["GIT_REPO_LOCAL_REMOTE_PATH"]) is False:
    git_match_default = settings.SETTINGS["paths"]["GIT_REPO_LOCAL_REMOTE_DEFAULT_PATH"]
    git_match_user = settings.SETTINGS["paths"]["GIT_REPO_LOCAL_REMOTE_PATH"]
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
        Key("c-l/20").execute()
        url = read_selected_without_altering_clipboard()
        if url[0] == 0:
            split_string = url[1].split("/pull/")
            repo_url = split_string[0]
            pr_name = split_string[1].split("/")[0]
            CONFIG = load_toml_file(settings.SETTINGS["paths"]["GIT_REPO_LOCAL_REMOTE_PATH"])
            if not CONFIG:
                # logger.warn("Could not load bringme defaults")
                raise Exception("Could not load " + settings.SETTINGS["paths"]["GIT_REPO_LOCAL_REMOTE_PATH"])

            items = rebuild_local_remote_items(CONFIG)
            if repo_url in items:
                local_directory = items[repo_url][0]
                local_directory = local_directory.replace("\\", "\\\\")
                directory_command = "cd " + local_directory
                TERMINAL_PATH = settings.SETTINGS["paths"]["TERMINAL_PATH"]
                AHK_PATH = settings.SETTINGS["paths"]["AHK_PATH"]
                if TERMINAL_PATH != "" and AHK_PATH != "":
                    # find the equivalent ahk script with the same name as this one
                    ahk_script = __file__.replace(".py", ".ahk")
                    pattern_match = "MINGW64"  # the string we expect to find in the title of git bash when loaded
                    # open the script which checks that git bash window is open or not
                    p = Popen([AHK_PATH, ahk_script, "exists", pattern_match], stdout=PIPE)
                    # retrieve the output from the ahk script
                    stdout, stderr = p.communicate()
                    # terminates the ahk script if not already done so
                    p.terminate()
                    # ready fetch command string to be appended to
                    fetch_command = ""
                    # if an existing git bash window has been activated
                    if stdout == pattern_match + " activated":
                        # set the first portion of the fetch command
                        fetch_command += directory_command + " && "
                    # if an existing git bash window is not already open
                    elif stdout == pattern_match + " does not exist":
                        # open up a new git bash terminal
                        terminal = Popen(TERMINAL_PATH, cwd=local_directory)
                        # open the script which checks that git bash windoow is ready or not for input
                        p = Popen([AHK_PATH, ahk_script, "create", pattern_match], stdout=PIPE)
                        # retrieve the output from the AHK script
                        stdout, stderr = p.communicate()
                        # terminates the ahk script if not already done so
                        p.terminate()
                        # if the git bash terminal is not ready
                        if stdout != pattern_match + " ready":
                            raise Exception("Error: git bash terminal took too long to load.")
                    # adds to the fetch command string that which will fetch from the particular repository in question
                    fetch_command += "git fetch " + repo_url + ".git pull/" + pr_name + "/head"
                    # if fetching from a new pull request
                    if new:
                        branch_name_base = repo_url.replace("https://github.com/", "")
                        checkout_command = "git checkout -b " + branch_name_base + "/pull/" + pr_name + " FETCH_HEAD"
                        # type in the full command into the git bash window
                        Text(fetch_command + " && " + checkout_command).execute()
                    else:  # otherwise if it is an update to an existing pull request
                        branch_name_base = repo_url.replace("https://github.com/", "")
                        checkout_command = "git checkout " + branch_name_base + "/pull/" + pr_name
                        # type in the full command into the git bash window
                        Text(fetch_command + " && " + checkout_command).execute()
                        Key("enter").execute()  # checkout is safe enough so will run this
                        merge_command = "git merge FETCH_HEAD"
                        time.sleep(3)  # allow time for the fetch commands complete before typing in the next one
                        Text(merge_command).execute()
                else:
                    raise Exception('TERMINAL_PATH in <user_dir>/.caster/data/settings.toml is not set, or AHK_PATH in castrvoice/lib/settings.py')
            else:
                raise Exception("Repository URL: " + repo_url + " not found in " + settings.SETTINGS["paths"]["GIT_REPO_LOCAL_REMOTE_PATH"])
    except Exception as e:
        print (e)
