from castervoice.lib.imports import *


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


class EclipseRule(MergeRule):
    pronunciation = "eclipse"

    mapping = {
        "prior tab [<n>]":
            R(Key("cs-f6"))*
            Repeat(extra="n"),  # these two must be set up in the eclipse preferences
        "next tab [<n>]":
            R(Key("c-f6"))*Repeat(extra="n"),
        "open resource":
            R(Key("cs-r")),
        "open type":
            R(Key("cs-t")),
        "jump to source":
            R(Key("f3")),
        "editor select":
            R(Key("c-e")),
        "step over [<n>]":
            R(Key("f6/50")*Repeat(extra="n")),
        "step into":
            R(Key("f5")),
        "step out [of]":
            R(Key("f7")),
        "resume":
            R(Key("f8")),
        "(debug | run) last":
            R(Key("f11")),
        "mark occurrences":
            R(Key("as-o")),

        # "terminate" changes to the settings for this hotkey: (when: in dialogs and windows)
        "terminate":
            R(Key("c-f2")),
        "refractor symbol":
            R(Key("sa-r")),
        "symbol next [<n>]":
            R(Key("c-k"))*Repeat(extra="n"),
        "symbol prior [<n>]":
            R(Key("cs-k"))*Repeat(extra="n"),
        "format code":
            R(Key("cs-f")),
        "do imports":
            R(Key("cs-o")),
        "comment line":
            R(Key("c-slash")),
        "build it":
            R(Key("c-b")),
        "split view horizontal":
            R(Key("cs-underscore")),
        "split view vertical":
            R(Key("cs-lbrace")),

        #Line Ops
        "find everywhere":
            R(Key("ca-g")),
        "find word <text> [<back>] [<go>]":
            R(Key("c-f") + Function(ec_con.regex_off) + Function(ec_con.find)),
        "find regex <text> [<back>] [<go>]":
            R(Key("c-f") + Function(ec_con.regex_on) + Function(ec_con.find)),
        "find <a> [<b> [<c>]] [<back>] [<go>]":
            R(Key("c-f") + Function(ec_con.find)),
        "find <punctuation> [<back>] [<go>]":
            R(Key("c-f") + Function(ec_con.find)),
    }
    extras = [
        Dictation("text"),
        Dictation("mim"),
        IntegerRefST("n", 1, 3000),
        alphanumeric.get_alphabet_choice("a"),
        alphanumeric.get_alphabet_choice("b"),
        alphanumeric.get_alphabet_choice("c"),
        Choice("punctuation", {"hash tag": "#"}),
        Boolean("back"),
        Boolean("go"),
    ]
    defaults = {
        "n": 1,
        "mim": "",
        "a": None,
        "b": None,
        "c": None,
        "punctuation": None,
        "back": False,
        "go": False
    }


class EclipseCCR(MergeRule):
    pronunciation = "eclipse jump"
    non = EclipseRule

    mapping = {
        #Line Ops
        "configure":
            R(Paste(ec_con.analysis_chars) +
                Key("left:2/5, c-f/20, backslash, rbracket, enter") +
                Function(ec_con.analyze_for_configure)),
        "jump in [<n>]":
            R(Key("c-f, a-o") + Paste(r"[\(\[\{\<]") + Function(ec_con.regex_on) +
                Key("enter:%(n)d/5, escape, right")),
        "jump out [<n>]":
            R(Key("c-f, a-o") + Paste(r"[\)\] \}\>]") + Function(ec_con.regex_on) +
                Key("enter:%(n)d/5, escape, right")),
        "jump back [<n>]":
            R(Key("c-f/5, a-b") + Paste(r"[\)\]\}\>]") + Function(ec_con.regex_on) +
                Key("enter:%(n)d/5, escape, left")),
        "[go to] line <n>":
            R(Key("c-l") + Pause("50") + Text("%(n)d") + Key("enter") + Pause("50")),
        "shackle <n> [<back>]":
            R(Key("c-l") + Key("right, cs-left") + Function(ec_con.lines_relative)),
    }
    extras = [
        Dictation("text"),
        IntegerRefST("n", 1, 1000),
        Boolean("back"),
    ]
    defaults = {"n": 1, "back": False}


context = AppContext(
    executable="javaw", title="Eclipse") | AppContext(
        executable="eclipse", title="Eclipse") | AppContext(executable="AptanaStudio3")
control.ccr_app_rule(EclipseRule(), context=context)