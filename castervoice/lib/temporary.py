from dragonfly import ActionBase, Paste
from castervoice.lib import context
from castervoice.lib.actions import Text, Key
'''
Stores the currently highlighted text in a temporary variable,
to be Retrieved after some other action. If no text was
highlighted, an empty string will be stored.
Sample usage:
"find that": Store() + Key("c-f") + Retrieve() + Key("enter")

In order to enable use with web URLs, Store() takes a string,
space, which will replace all space characters, and a bool,
remove_cr, which if true will remove any newlines in the
selection, to avoid them triggering the request early.
Sample usage:
"wikipedia that":
    Store(space="+", remove_cr=True) + Key("c-t") +
    Text("https://en.wikipedia.org/w/index.php?search=") +
    Retrieve() + Key("enter")

There are cases where you may want the same function to do
different things depending on whether or not text was highlighted.
The action_if_no_text and action_if_text arguments to Retrieve()
are calls to Key() and allow this.
For example, you may want to finish inside a set of brackets
if no text was highlighted, but outside if there was text.
Sample usage:
"insert bold text":
    Store() + Text("\\textbf{}") + Key("left") +
    Retrieve(action_if_text="right")

NOTE:
If the highlighted text is the same as what is currently on the
clipboard, an empty string will be stored. This is a necessary
side-effect of being able to detect when no text is highlighted.
'''
_TEMP = ""


class Store(ActionBase):
    def __init__(self, space=" ", remove_cr=False):
        ActionBase.__init__(self)
        self.space = space
        self.remove_cr = remove_cr

    def _execute(self, data=None):
        global _TEMP
        _, orig = context.read_selected_without_altering_clipboard(False)
        text = orig.replace(" ", self.space) if orig else ""
        _TEMP = text.replace("\n", "") if self.remove_cr else text
        return True


class Retrieve(ActionBase):
    def __init__(self, action_if_no_text="", action_if_text=""):
        ActionBase.__init__(self)
        self.action_if_no_text = action_if_no_text
        self.action_if_text = action_if_text

    @classmethod
    def text(cls):
        return _TEMP

    def _execute(self, data=None):
        output = _TEMP
        Paste(output).execute()
        if output:
            Key(self.action_if_text).execute()
        else:
            Key(self.action_if_no_text).execute()
        return True
