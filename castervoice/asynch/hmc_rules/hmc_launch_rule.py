from dragonfly import Function, MappingRule

from castervoice.asynch.hmc import h_launch
from castervoice.lib import settings
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.actions import AsynchronousAction
from castervoice.lib.merge.state.short import R, S, L


def receive_settings(data):
    settings.SETTINGS = data
    settings.save_config()
    # TODO: apply new settings


def settings_window():
    h_launch.launch(settings.QTTYPE_SETTINGS)
    on_complete = AsynchronousAction.hmc_complete(lambda data: receive_settings(data))
    AsynchronousAction(
        [L(S(["cancel"], on_complete))],
        time_in_seconds=1,
        repetitions=300,
        blocking=False).execute()


class HMCLaunchRule(MappingRule):
    mapping = {
        "launch caster settings":
            R(Function(settings_window)),
    }


def get_rule():
    details = RuleDetails(name="settings window launcher")
    return HMCLaunchRule, details
