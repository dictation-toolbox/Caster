import re

from dragonfly import Function

from castervoice.lib import settings, context
from castervoice.lib.actions import Text
from castervoice.lib.merge.selfmod.selfmodrule import BaseSelfModifyingRule
from castervoice.asynch.hmc import h_launch
from castervoice.lib.merge.state.actions import AsynchronousAction
from castervoice.lib.merge.state.actions2 import NullAction
from castervoice.lib.merge.state.short import R, S, L


class BaseAliasRule(BaseSelfModifyingRule):
    """
    Alias rules allow for highlighting text on the screen, then
    using a GUI component to create an instant Text command.
    """

    mapping = {"default alias command": NullAction()}

    def __init__(self, config_path, **kwargs):
        super(BaseAliasRule, self).__init__(config_path, **kwargs)

    def _deserialize(self):
        mapping = {}
        pronunciation = self.get_pronunciation()
        # recreate all saved aliases
        commands = self._config.get_copy()
        for spec in commands:
            text = commands[spec]
            mapping[spec] = R(Text(text), rdescript="{}: {}".format(pronunciation, spec))
        # add command for creating new aliases
        mapping["{} [<s>]".format(pronunciation)] = R(
            Function(lambda s: self._alias(s)), rdescript="Create {}".format(pronunciation))
        # add command for deleting all aliases
        mapping["delete {}es".format(pronunciation)] = R(
            Function(lambda: self._delete_all()), rdescript="Delete {}".format(pronunciation))
        self._smr_mapping = mapping

    def _refresh(self, *args):
        if len(args) > 1 and args[0] != "":
            spec = str(args[0])
            text = str(args[1])
            self._config.put(spec, text)
            self._config.save()
        self.reset()

    def _alias(self, spec):
        """
        Takes highighted text and makes a Text action of it and the passed spec.
        Uses an AsynchronousAction to wait for a GUI to get the aliased word.

        :param spec: str
        :return:
        """
        text = BaseAliasRule._read_highlighted(10)
        if text is not None:
            if spec:
                spec = re.sub(r'[^A-Za-z\'\s]+', '', str(spec)).lower() # Sanitize free dictation for spec, words and apostrophes only.
                self._refresh(spec, str(text))
            else:
                h_launch.launch(settings.QTYPE_INSTRUCTIONS, data="Enter_spec_for_command|")
                on_complete = AsynchronousAction.hmc_complete(
                    lambda data: self._refresh(data[0].replace("\n", ""), text))
                AsynchronousAction(
                    [L(S(["cancel"], on_complete))],
                    time_in_seconds=0.5,
                    repetitions=300,
                    blocking=False).execute()

    def _delete_all(self):
        self._config.replace({})
        self._refresh()

    @staticmethod
    def _read_highlighted(max_tries):
        for i in range(0, max_tries):
            result = context.read_selected_without_altering_clipboard(True)
            if result[0] == 0:
                return result[1]
        return None
