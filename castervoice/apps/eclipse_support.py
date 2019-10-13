import re

from castervoice.lib.actions import Key

from castervoice.lib import utilities, context
from castervoice.lib.actions import Text
from castervoice.lib.merge.state.actions2 import UntilCancelled


class EclipseController(object):
    def __init__(self):
        self.regex = False
        self.analysis_chars = r"\]"

    def regex_on(self):
        if not self.regex:
            Key("a-x").execute()  # turn on regex
        self.regex = True

    def regex_off(self):
        if self.regex:
            Key("a-x").execute()  # turn off regex
        self.regex = False

    def analyze_for_configure(self):
        '''solves the problem of the editor not being smart about toggles by using text
        to see which toggles are active'''
        '''regex toggle check'''
        Key("escape").execute()  # get out of Find
        result = context.read_nmax_tries(10)
        if result == self.analysis_chars:
            self.regex = False
            Key("backspace").execute()
        elif result == self.analysis_chars[1]:
            self.regex = True
            Key("delete, backspace").execute()
        else:
            print("Eclipse configuration failed (%s)" % result)

    def lines_relative(self, back, n):
        if back:  #backward
            try:
                num = context.read_nmax_tries(10)
                txt = str(int(num) - int(n) + 1)  # +1 to include current line
                Text(txt).execute()
            except ValueError:
                utilities.simple_log()
                return
            Key("enter").execute()
        else:  #forward
            Key("escape, end, home, home").execute(
            )  # end-home-home to include all of current line

        # forward or backward
        Key("s-down:" + str(int(n)) + "/5, s-left").execute()

    def find(self, back, go, text=None, punctuation=None, a=None, b=None, c=None):
        '''set direction'''

        key = "b" if back else "o"
        Key("a-" + key).execute()
        '''figure out what to search for'''
        if text is not None:
            text = str(text)
            '''simple vowel-removal regex'''
            if self.regex:
                text = re.sub("[aeiouAEIOU]+", r".*", text)
                if text.endswith(r".*"):
                    text = text[:-2]
        elif punctuation is not None:
            text = str(punctuation)
            self.regex_off()
        elif a is not None:
            a = str(a)
            b = str(b) if b is not None else ""
            c = str(c) if c is not None else ""
            text = a + b + c
            self.regex_off()
        Text(text).execute()
        '''"go" indicates that we should keep looking'''
        if go:
            u = UntilCancelled(Key("enter"), 2)
            u.show = False
            u.execute()
        else:
            Key("enter, escape").execute()


ec_con = EclipseController()
