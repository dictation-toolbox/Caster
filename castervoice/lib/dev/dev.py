import os
import shutil
from subprocess import Popen
import time
import threading
import shlex

from dragonfly import (Function, BringApp, WaitWindow, Dictation, Choice, Grammar,
                       MappingRule, Paste, ShortIntegerRef)

from castervoice.lib import utilities, settings, context, control
from castervoice.lib.dev import devgen
from castervoice.lib.actions import Key, Text

from castervoice.lib.merge.state.actions import ContextSeeker, AsynchronousAction, \
    RegisteredAction
from castervoice.lib.merge.state.actions2 import NullAction, ConfirmAction, \
    BoxAction
from castervoice.lib.merge.state.short import L, S, R
from castervoice.lib.merge.state.stackitems import StackItemRegisteredAction
# from castervoice.lib.tests import testrunner # Deprecated
# from castervoice.lib.tests.test_complexity import run_tests # Deprecated
# from castervoice.lib.tests.testutils import MockAlternative # Deprecated

if os.path.isfile(settings.SETTINGS["paths"]["CONFIGDEBUGTXT_PATH"]) is False:
    configdebug_default = settings.SETTINGS["paths"][
        "BASE_PATH"] + "/bin/data/configdebug.txt"
    configdebug_user = settings.SETTINGS["paths"]["CONFIGDEBUGTXT_PATH"]
    shutil.copy(configdebug_default, configdebug_user)

grammar = Grammar('development')


def experiment():
    '''This function is for test'''


def run_remote_debugger():
    utilities.remote_debug("dev.py")


COUNT = 5


def countdown():
    global COUNT
    print(COUNT)
    COUNT -= 1
    return COUNT == 0


def grep_this(path, filetype):
    c = None
    tries = 0
    while c is None:
        tries += 1
        results = context.read_selected_without_altering_clipboard()
        error_code = results[0]
        if error_code == 0:
            c = results[1]
            break
        if tries > 5:
            return False
    grep = "D:/PROGRAMS/NON_install/AstroGrep/AstroGrep.exe"
    Popen([
        grep, "/spath=\"" + str(path) + "\"", "/stypes=\"" + str(filetype) + "\"",
        "/stext=\"" + str(c) + "\"", "/s"
    ])


def bring_test():
    print(settings.SETTINGS["paths"]["BASE_PATH"].replace("/", "\\"))
    try:
        BringApp("explorer", settings.SETTINGS["paths"]["BASE_PATH"]).execute()
    except Exception:
        utilities.simple_log()


def launch_url(url):
    command = utilities.default_browser_command()
    if not command:
        threading.Thread(target=os.startfile, args=(url, )).start()  # pylint: disable=no-member
    else:
        path = command.replace('%1', url)
        Popen(shlex.split(path))


class DevelopmentHelp(MappingRule):
    mapping = {
        # castervoice development tools
        "(show | open) <url> documentation":
            Function(launch_url),
        "open natlink folder":
            R(BringApp("C:/Windows/explorer.exe",
                       settings.SETTINGS["paths"]["BASE_PATH"].replace("/", "\\")),
              rdescript="Open Natlink Folder"),
        "refresh debug file":
            R(Function(devgen.refresh), rdescript="Dev: Refreshed Debug File"),
        "Agrippa <filetype> <path>":
            Function(grep_this),
#        "run rule complexity test":
#            Function(lambda: run_tests()),
#        "run unit tests":
#            Function(testrunner.run_tests),
        "run remote debugger":
            Function(run_remote_debugger),
    }
    extras = [
        Dictation("text"),
        Choice("path", {
            "natlink": "c:/natlink/natlink",
            "sea": "C:/",
        }),
        Choice("filetype", {
            "java": "*.java",
            "python": "*.py",
        }),
        Choice(
            "url", {
                "caster": "https://dictation-toolbox.github.io/Caster",
                "dragonfly": "https://dragonfly2.readthedocs.io/en/latest/",
            }),
    ]
    defaults = {"text": ""}


class Experimental(MappingRule):

    mapping = {
        # experimental/incomplete commands
        "experiment": Function(experiment),
        "short talk number <n2>": Text("%(n2)d"),
        #     "dredge [<id> <text>]":         Function(dredge),
        "test dragonfly paste": Paste("some text"),
    }
    extras = [Dictation("text"), Dictation("text2"), ShortIntegerRef("n2", 1, 100)]
    defaults = {"text": "", "text2": ""}


LAST_TIME = 0


def print_time():
    global LAST_TIME
    print(str(time.time() - LAST_TIME)[0])
    LAST_TIME = time.time()


def close_last_spoken(spoken):
    first = spoken[0]
    Text("</" + first + ">").execute()


def close_last_rspec(rspec):
    Text("</" + rspec + ">").execute()


def _abc(data):
    print(data)


FINISHER_TEXT = "finisher successful"


class StackTest(MappingRule):
    '''test battery for the ContextStack'''

    mapping = {
        "close last tag":
            ContextSeeker([
                L(
                    S(["cancel"], None),
                    S(["html spoken"], close_last_spoken, use_spoken=True),
                    S(["span", "div"], close_last_rspec, use_rspec=True))
            ]),
        "html":
            R(Text("<html>"), rspec="html spoken"),
        "divider":
            R(Text("<div>"), rspec="div"),
        "span":
            R(Text("<span>"), rspec="span"),
        "backward seeker [<text>]":
            ContextSeeker([
                L(
                    S(["ashes"], Text("ashes1 [%(text)s] ")),
                    S(["bravery"], Text("bravery1 [%(text)s] "))),
                L(
                    S(["ashes"], Text("ashes2 [%(text)s] ")),
                    S(["bravery"], Text("bravery2 [%(text)s] ")))
            ]),
        "forward seeker [<text>]":
            ContextSeeker(forward=[
                L(
                    S(["ashes"], Text("ashes1 [%(text)s] ")),
                    S(["bravery"], Text("bravery1 [%(text)s] "))),
                L(
                    S(["ashes"], Text("ashes2 [%(text)s] ")),
                    S(["bravery"], Text("bravery2 [%(text)s] ")))
            ]),
        "asynchronous test":
            AsynchronousAction([
                L(
                    S(["ashes", "charcoal"], print_time, None),
                    S(["bravery"], Text, "bravery1"))
            ],
                               time_in_seconds=0.2,
                               repetitions=20,
                               finisher=Text(FINISHER_TEXT),
                               blocking=False),
        "ashes":
            RegisteredAction(Text("ashes _ "), rspec="ashes"),
        "bravery":
            RegisteredAction(Text("bravery _ "), rspec="bravery"),
        "charcoal <text> [<n>]":
            R(Text("charcoal _ %(text)s"), rspec="charcoal"),
        "test confirm action":
            ConfirmAction(
                Key("a"), rdescript="Confirm Action Test",
                instructions="some words here"),
        "test box action":
            BoxAction(
                lambda data: _abc(data),
                rdescript="Test Box Action",
                box_type=settings.QTYPE_DEFAULT,
                log_failure=True),
    }
    extras = [Dictation("text"), Dictation("text2"), ShortIntegerRef("n", 1, 5)]
    defaults = {"text": "", "text2": ""}


#def load(): # ToDo: Migrate to Caster 1.0.0
#    global grammar
#    grammar.add_rule(StackTest())
#    grammar.add_rule(DevelopmentHelp())
#    grammar.add_rule(Experimental())
#    grammar.load()


#if settings.SETTINGS["miscellaneous"]["dev_commands"]:
#    load()
