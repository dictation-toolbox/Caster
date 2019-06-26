from castervoice.lib.imports import *
from castervoice.asynch.hmc import h_launch

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
            R(Function(kill, nexus=_NEXUS)),
        "complete":
            R(Function(complete, nexus=_NEXUS))
    }

class HMCHistoryRule(MergeRule):
    mapping = {
        # specific to macro recorder
        "check <n>":
            R(Function(hmc_checkbox, nexus=_NEXUS)),
        "check from <n> to <n2>":
            R(Function(hmc_recording_check_range, nexus=_NEXUS)),
        "exclude <n>":
            R(Function(hmc_recording_exclude, nexus=_NEXUS)),
        "[make] repeatable":
            R(Function(hmc_recording_repeatable, nexus=_NEXUS))
    }
    extras = [
        IntegerRefST("n", 1, 25),
        IntegerRefST("n2", 1, 25),
    ]

class HMCDirectoryRule(MergeRule):
    mapping = {
        # specific to directory browser
        "browse":
            R(Function(hmc_directory_browse, nexus=_NEXUS))
    }

class HMCConfirmRule(MergeRule):
    mapping = {
        # specific to confirm
        "confirm":
            R(Function(hmc_confirm, value=True, nexus=_NEXUS)),
        "disconfirm":
            R(Function(hmc_confirm, value=False, nexus=_NEXUS),
              rspec="hmc_cancel")
    }

class HMCSettingsRule(MergeRule):
    mapping = {
        "kill homunculus": R(Function(kill)),
        "complete": R(Function(hmc_settings_complete)),
    }

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
            R(Function(settings_window, nexus=_NEXUS)),
    }

if settings.SETTINGS["feature_rules"]["hmc"]:
    control.non_ccr_app_rule(HMCRule(), AppContext(title=settings.HOMUNCULUS_VERSION), rdp=False)
    control.non_ccr_app_rule(HMCHistoryRule(), AppContext(title=settings.HMC_TITLE_RECORDING), rdp=False)
    control.non_ccr_app_rule(HMCDirectoryRule(), AppContext(title=settings.HMC_TITLE_DIRECTORY), rdp=False)
    control.non_ccr_app_rule(HMCConfirmRule(), AppContext(title=settings.HMC_TITLE_CONFIRM), rdp=False)
    control.non_ccr_app_rule(HMCSettingsRule(), AppContext(title=settings.SETTINGS_WINDOW_TITLE), rdp=False)
    control.non_ccr_app_rule(LaunchRule(), context=None, rdp=False)

if not settings.SETTINGS["feature_rules"]["hmc"]:
    print("WARNING: Tk Window controls have been disabled -- this is not advised!")
