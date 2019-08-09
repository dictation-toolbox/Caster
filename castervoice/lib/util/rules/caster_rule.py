from dragonfly import MappingRule, Function, RunCommand, Playback

from castervoice.lib.ctrl.dependencies import pip_path, update
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


class _DependencyUpdate(RunCommand):
    synchronous = True

    # pylint: disable=method-hidden
    def process_command(self, proc):
        # Process the output from the command.
        RunCommand.process_command(self, proc)
        # Only reboot dragon if the command was successful and online_mode is true
        # 'pip install ...' may exit successfully even if there were connection errors.
        if proc.wait() == 0 and update:
            Playback([(["reboot", "dragon"], 0.0)]).execute()


class CasterRule(MappingRule):
    mapping = {
        # update management
        "update caster":
            R(_DependencyUpdate([pip_path, "install", "--upgrade", "castervoice"])),
        "update dragonfly":
            R(_DependencyUpdate([pip_path, "install", "--upgrade", "dragonfly2"])),

        # ccr de/activation
        "enable caster":
            R(Function(_NEXUS.merger.merge, time=MergeInf.RUN, name="numbers")),
        "disable caster":
            R(Function(_NEXUS.merger.ccr_off)),
    }


def get_rule():
    return CasterRule, RuleDetails(name="caster rule", rdp_mode_exclusion=True)
