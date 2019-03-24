from dragonfly import ActionBase
from castervoice.lib import context, control
from castervoice.lib.actions import Text, Key


class Store(ActionBase):
    def __init__(self, space=" ", remove_cr=False):
        ActionBase.__init__(self)
        self.space = space
        self.remove_cr = remove_cr

    def _execute(self, data=None):
        _, orig = context.read_selected_without_altering_clipboard(False)
        text = orig.replace(" ", self.space) if orig else ""
        control.nexus().temp = text.replace("\n", "") if self.remove_cr else text
        return True


class Retrieve(ActionBase):
    def __init__(self, action_if_no_text="", action_if_text=""):
        ActionBase.__init__(self)
        self.action_if_no_text = action_if_no_text
        self.action_if_text = action_if_text

    @classmethod
    def text(cls):
        return control.nexus().temp

    def _execute(self, data=None):
        output = control.nexus().temp
        Text(output).execute()
        if output:
            Key(self.action_if_text).execute()
        else:
            Key(self.action_if_no_text).execute()
        return True
