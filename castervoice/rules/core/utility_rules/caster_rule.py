from dragonfly import MappingRule, Function, RunCommand, Playback

from castervoice.lib import control, utilities
from castervoice.lib.ctrl.dependencies import find_pip  # pylint: disable=no-name-in-module
from castervoice.lib.ctrl.updatecheck import update
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R

_PIP = find_pip()


class _DependencyUpdate(RunCommand):
    synchronous = True

    # pylint: disable=method-hidden
    def process_command(self, proc):
        # Process the output from the command.
        RunCommand.process_command(self, proc)
        # Only reboot dragon if the command was successful and online_mode is true
        # 'pip install ...' may exit successfully even if there were connection errors.
        if proc.wait() == 0 and update:
            Function(utilities.reboot).execute()


class CasterRule(MappingRule):
    mapping = {
        "clear caster log":
            R(Function(utilities.clear_log)),
        "reboot caster":
            R(Function(utilities.reboot)),
        "update dragonfly":
            R(_DependencyUpdate([_PIP, "install", "--upgrade", "dragonfly2"])),
        # update management ToDo: Fully implement castervoice PIP install
        #"update caster":   
        #    R(_DependencyUpdate([_PIP, "install", "--upgrade", "castervoice"])),

        # ccr de/activation
        "enable (c c r|ccr)":
            R(Function(lambda: control.nexus().set_ccr_active(True))),
        "disable (c c r|ccr)":
            R(Function(lambda: control.nexus().set_ccr_active(False))),
    }


def get_rule():
    return CasterRule, RuleDetails(name="caster rule")
