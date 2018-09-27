from difflib import SequenceMatcher
from subprocess import Popen
import time

from dragonfly import (Function, Key, BringApp, Text, WaitWindow, Dictation, Choice,
                       Grammar, MappingRule, Paste)

from caster.lib import utilities, settings, context, control
from caster.lib.dev import devgen
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.state.actions import ContextSeeker, AsynchronousAction, \
    RegisteredAction
from caster.lib.dfplus.state.actions2 import NullAction, ConfirmAction, \
    BoxAction
from caster.lib.dfplus.state.short import L, S, R
from caster.lib.dfplus.state.stackitems import StackItemRegisteredAction
from caster.lib.tests import testrunner
from caster.lib.tests.complexity import run_tests
from caster.lib.tests.testutils import MockAlternative

grammar = Grammar('development')


def experiment():
    '''this function is for tests'''


#     try:
#         for i in range(0, 10000):
#             action = NullAction(rdescript="test_"+str(i))
#             action.show = True
#             action.set_nexus(control.nexus())
#             alt = MockAlternative(u"my", u"spoken", u"words")
#             sia = StackItemRegisteredAction(action, {"_node":alt})
#             control.nexus().state.add(sia)
#     except Exception:
#         utilities.simple_log()

#     from Levenshtein.StringMatcher import StringMatcher
#     try:
#         spoken = "issue certificate shares"
#         for item in ["isctsh", # actual answer, rated worst with sift4
#                      "Issue",
#                      "issue_list",
#                      "issues",
#                      "isbksh",
#                      "cert",
#                      "ctshrs",
#                      "certificate",
#                      "Certificate",
#                      spoken #for reference
#                       ]:
#             s = SequenceMatcher(None, item, spoken) # difflib
#             caster_abbrev = selector._abbreviated_string(spoken).lower() # caster
#
#             l = StringMatcher()
#             l.set_seqs(spoken, item)
#
#
#             print("caster", item, selector._phrase_to_symbol_similarity_score(caster_abbrev, item))
#             print("difflib: ", item, s.ratio())
#             print("levenshtein: ", item, l.ratio())
#             print("sift4: ", item, sift4(item, spoken, None, None))
#             print("\n")
#
#
#         print(str(text), str(text2), sift4(str(text), str(text2), None, None))
#     except Exception:
#         utilities.simple_log()

#     comm = Communicator()
#     comm.get_com("status").error(0)


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


class DevelopmentHelp(MappingRule):
    mapping = {
        # caster development tools
        "(show | open) documentation":
            BringApp(settings.SETTINGS["paths"]["DEFAULT_BROWSER_PATH"]) +
            WaitWindow(executable=settings.get_default_browser_executable()) +
            Key('c-t') + WaitWindow(title="New Tab") +
            Text('http://dragonfly.readthedocs.org/en/latest') + Key('enter'),
        "open natlink folder":
            R(BringApp("C:/Windows/explorer.exe",
                       settings.SETTINGS["paths"]["BASE_PATH"].replace("/", "\\")),
              rdescript="Open Natlink Folder"),
        "refresh debug file":
            Function(devgen.refresh),
        "Agrippa <filetype> <path>":
            Function(grep_this),
        "run rule complexity test":
            Function(lambda: run_tests()),
        "run unit tests":
            Function(testrunner.run_tests),
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
        })
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
    extras = [Dictation("text"), Dictation("text2"), IntegerRefST("n2", 1, 100)]
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
            AsynchronousAction(
                [
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
    extras = [Dictation("text"), Dictation("text2"), IntegerRefST("n", 1, 5)]
    defaults = {"text": "", "text2": ""}


def load():
    global grammar
    grammar.add_rule(StackTest())
    grammar.add_rule(DevelopmentHelp())
    grammar.add_rule(Experimental())
    grammar.load()


if settings.SETTINGS["miscellaneous"]["dev_commands"]:
    load()
