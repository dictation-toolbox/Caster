from dragonfly import (Function, Grammar, AppContext)

from caster.lib.asynch.hmc import h_launch
from caster.lib import control
from caster.lib import settings, utilities
from caster.lib.dfplus.additions import IntegerRefST
from caster.lib.dfplus.merge import gfilter
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.actions import AsynchronousAction
from caster.lib.dfplus.state.short import R, L, S

_NEXUS = control.nexus()


def kill(nexus):
    nexus.comm.get_com("hmc").kill()


def complete(nexus):
    nexus.comm.get_com("hmc").complete()


def hmc_checkbox(n, nexus):
    # can easily check multiple boxes, use a comma-separated list of numbers instead of str(n)
    nexus.comm.get_com("hmc").do_action("check", [int(n)])


def hmc_focus(field, nexus):
    # can easily check multiple boxes, use a comma-separated list of numbers instead of str(n)
    nexus.comm.get_com("hmc").do_action("focus", str(field))


def hmc_recording_check_range(n, n2, nexus):
    nexus.comm.get_com("hmc").do_action("check_range", [int(n), int(n2)])


def hmc_recording_exclude(n, nexus):
    nexus.comm.get_com("hmc").do_action("exclude", int(n))


def hmc_recording_repeatable(nexus):
    nexus.comm.get_com("hmc").do_action("repeatable")


def hmc_directory_browse(nexus):
    nexus.comm.get_com("hmc").do_action("dir")


def hmc_confirm(value, nexus):
    nexus.comm.get_com("hmc").do_action(value)


def hmc_settings_complete(nexus):
    nexus.comm.get_com("hmc").complete()


class HMCRule(MergeRule):
    mapping = {
        "kill homunculus":
            R(Function(kill, nexus=_NEXUS), rdescript="Kill Helper Window"),
        "complete":
            R(Function(complete, nexus=_NEXUS), rdescript="Complete Input")
    }


grammar = Grammar("hmc", context=AppContext(title=settings.HOMUNCULUS_VERSION))
r1 = HMCRule()
gfilter.run_on(r1)
grammar.add_rule(r1)
if settings.SETTINGS["feature_rules"]["hmc"]:
    grammar.load()


class HMCHistoryRule(MergeRule):
    mapping = {
        # specific to macro recorder
        "check <n>":
            R(Function(hmc_checkbox, nexus=_NEXUS), rdescript="Check Checkbox"),
        "check from <n> to <n2>":
            R(Function(hmc_recording_check_range, nexus=_NEXUS), rdescript="Check Range"),
        "exclude <n>":
            R(Function(hmc_recording_exclude, nexus=_NEXUS),
              rdescript="Uncheck Checkbox"),
        "[make] repeatable":
            R(Function(hmc_recording_repeatable, nexus=_NEXUS),
              rdescript="Make Macro Repeatable")
    }
    extras = [
        IntegerRefST("n", 1, 25),
        IntegerRefST("n2", 1, 25),
    ]


grammar_history = Grammar(
    "hmc history", context=AppContext(title=settings.HMC_TITLE_RECORDING))
r2 = HMCHistoryRule()
gfilter.run_on(r2)
grammar_history.add_rule(r2)
if settings.SETTINGS["feature_rules"]["hmc"]:
    grammar_history.load()


class HMCDirectoryRule(MergeRule):
    mapping = {
        # specific to directory browser
        "browse":
            R(Function(hmc_directory_browse, nexus=_NEXUS), rdescript="Browse Computer")
    }


grammar_directory = Grammar(
    "hmc directory", context=AppContext(title=settings.HMC_TITLE_DIRECTORY))
r3 = HMCDirectoryRule()
gfilter.run_on(r3)
grammar_directory.add_rule(r3)
if settings.SETTINGS["feature_rules"]["hmc"]:
    grammar_directory.load()


class HMCConfirmRule(MergeRule):
    mapping = {
        # specific to confirm
        "confirm":
            R(Function(hmc_confirm, value=True, nexus=_NEXUS),
              rdescript="HMC: Confirm Action"),
        "disconfirm":
            R(Function(hmc_confirm, value=False, nexus=_NEXUS),
              rspec="hmc_cancel",
              rdescript="HMC: Cancel Action")
    }


grammar_confirm = Grammar(
    "hmc confirm", context=AppContext(title=settings.HMC_TITLE_CONFIRM))
r4 = HMCConfirmRule()
gfilter.run_on(r4)
grammar_confirm.add_rule(r4)
if settings.SETTINGS["feature_rules"]["hmc"]:
    grammar_confirm.load()


class HMCSettingsRule(MergeRule):
    mapping = {
        "kill homunculus": R(Function(kill), rdescript="Kill Settings Window"),
        "complete": R(Function(hmc_settings_complete), rdescript="Complete Input"),
    }


grammar_settings = Grammar(
    "hmc settings", context=AppContext(title=settings.SETTINGS_WINDOW_TITLE))
r5 = HMCSettingsRule()
gfilter.run_on(r5)
grammar_settings.add_rule(r5)
if settings.SETTINGS["feature_rules"]["hmc"]:
    grammar_settings.load()


def receive_settings(data):
    settings.SETTINGS = data
    settings.save_config()
    # TODO: apply new settings


def settings_window(nexus):
    h_launch.launch(settings.WXTYPE_SETTINGS)
    on_complete = AsynchronousAction.hmc_complete(lambda data: receive_settings(data),
                                                  nexus)
    AsynchronousAction(
        [L(S(["cancel"], on_complete))],
        time_in_seconds=1,
        repetitions=300,
        blocking=False).execute()


class LaunchRule(MergeRule):
    mapping = {
        "launch settings window":
            R(Function(settings_window, nexus=_NEXUS),
              rdescript="Launch Settings Window"),
    }


grammarw = Grammar("Caster Windows")
r6 = LaunchRule()
gfilter.run_on(r6)
grammarw.add_rule(r6)
if settings.SETTINGS["feature_rules"]["hmc"]:
    grammarw.load()

if not settings.SETTINGS["feature_rules"]["hmc"]:
    print("WARNING: Tk Window controls have been disabled -- this is not advised!")
