# -*- coding: utf-8 -*-

import io
import os
#from pywinauto import application
import shutil
import sys
import traceback
from __builtin__ import True
from subprocess import Popen, call, PIPE
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


stdout = ""


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
                # fetch_command = "git fetch " + repo_url + ".git pull/" + pr_name + "/head"
                if TERMINAL_PATH != "" and AHK_PATH != "":
                    #app = application.Application()
                    #app.start(TERMINAL_PATH)

                    # This can be improved with a wait command
                    # time.sleep(5)
                    #ahk_script = os.path.splitext(os.path.basename(__file__))[0] + ".ahk"
                    ahk_script = __file__.replace(".py",".ahk")
                    pattern_match = "MINGW64"
                    # p = call([AHK_PATH, ahk_script, "exists"], stdout=PIPE)
                    p = Popen([AHK_PATH, ahk_script, "exists"], stdout=PIPE)
                    stdout, stderr = p.communicate()
                    p.terminate()
                    #raise stdout
                    #raise stderr
                    raise Exception("exists msg: stdout = " + str(stdout) + ", stderr = " + str(stderr))

                    fetch_command = ""
                    if stdout == pattern_match + " activated":
                        fetch_command += directory_command + " && "
                    elif stdout == pattern_match + " does not exist":
                        terminal = Popen(TERMINAL_PATH, cwd=local_directory)
                        p = Popen([AHK_PATH, ahk_script, "create"], stdout=PIPE)
                        #p = call([AHK_PATH, ahk_script, "create"], stdout=PIPE)
                        stdout, stderr = p.communicate()
                        #raise stdout
                        #raise stderr
                        raise Exception("create msg: stdout = " + str(stdout) + ", stderr = " + str(stderr))
                        p.terminate()
                    fetch_command += "git fetch " + repo_url + ".git pull/" + pr_name + "/head"
                    if stdout != pattern_match + " ready":
                        raise Exception("Error: git bash terminal was not ready.")
                    if new:
                        branch_name_base = repo_url.replace("https://github.com/", "")
                        checkout_command = "git checkout -b " + branch_name_base + "/pull/" + pr_name + " FETCH_HEAD"
                        #Text(directory_command + " && " + fetch_command + " && " + checkout_command).execute()
                        Text(fetch_command + " && " + checkout_command).execute()
                    else:
                        branch_name_base = repo_url.replace("https://github.com/", "")
                        checkout_command = "git checkout " + branch_name_base + "/pull/" + pr_name
                        #Text(directory_command + " && " + fetch_command + " && " + checkout_command).execute()
                        Text(fetch_command + " && " + checkout_command).execute()
                        Key("enter").execute() # checkout is safe enough so will run this
                        merge_command = "git merge FETCH_HEAD"
                        time.sleep(3)
                        Text(merge_command).execute()
                else:
                    raise Exception('TERMINAL_PATH in <user_dir>/.caster/data/settings.toml is not set')
            else:
                raise Exception("Repository URL: " + repo_url + " not found in " + settings.SETTINGS["paths"]["GIT_REPO_LOCAL_REMOTE_PATH"])
    except Exception as e:
        print (e, stdout, ", ", stderr)
