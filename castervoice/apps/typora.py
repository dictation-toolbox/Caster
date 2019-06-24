"""
__author__ = 'LexiconCode'
Command-module for Typora
Official Site "https://typora.io/"
"""
# ---------------------------------------------------------------------------
from dragonfly import Dictation, Grammar, Repeat

from castervoice.lib import control, settings
from castervoice.lib.actions import Key, Text
from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.state.short import R
# ---------------------------------------------------------------------------


class TyporaRule(MergeRule):
    pronunciation = "tie poor a"

    mapping = {
        # File
        "new file":
            R(Key("c-n"), rdescript="Typora: New Markdown Document"),
        "new window":
            # Listed but not implemented
            R(Key("cs-n"), rdescript="Typora: New Window"),
        # "new tab":      R(Key(""), rdescript="Typora: New Tab"), # Not implemented in Windows OS
        "open file":
            R(Key("c-o"), rdescript="Typora: Open File"),
        "go [to] file":
            R(Key("c-p"), rdescript="Typora: Open Quickly"),
        "reopen [closed] file":
            R(Key("cs-t"), rdescript="Typora: Reopen Closed File"),
        "save as":
            R(Key("cs-s"), rdescript="Typora: Save As"),
        "close file":
            R(Key("c-w"), rdescript="Typora: Close"),
        # Edit
        # "new paragraph": R(Key("enter"), rdescript="Typora: New Paragraph") * Repeat(extra="h"), # Caster: "shock"
        "new line <h>":
            R(Key("s-enter"), rdescript="Typora: New Line") * Repeat(extra="h"),
        "copy [as] markdown":
            R(Key("cs-c"), rdescript="Typora: Copy as Markdown"),
        "delete row <n>":
            R(Key("cs-backspace"), rdescript="Typora: Delete Row") * Repeat(extra="n"),
        "select [cell | scope]":
            R(Key("c-e"), rdescript="Typora: Select Style Scope or Cell"),
        "[select] word <n>":
            R(Key("c-d"), rdescript="Typora: Select Word") * Repeat(extra="n"),
        "delete word <n>":
            R(Key("cs-d"), rdescript="Typora: Delete Word") * Repeat(extra="n"),
        # "jump [to] top":    R(Key("c-home"), rdescript="Typora: Jump to Top"), # Caster: "sauce wally"
        # "jump [to] selection":  R(Key("c-j"), rdescript="Typora: Jump to Selection"), # Caster: "dunce wally"
        "jump [to] buttom":
            R(Key("c-end"), rdescript="Typora: Jump to Buttom"),
        "find":  # Say "escape" to exit the find/replace context
            R(Key("c-f"), rdescript="Typora: Find"),
        "find next":
            R(Key("f3"), rdescript="Typora: Find Next"),
        "replace":
            R(Key("c-h"), rdescript="Typora: Replace"),
        # Paragraph
        "heading <h>":
            R(Key("c-%(h)d"), rdescript="Typora: Heading size 0 through 6"),
        "paragraph":
            R(Key("c-o"), rdescript="Typora: Paragraph"),
        "increase heading [level] <h>":
            R(Key("c-equal"), rdescript="Typora: Increase Heading Level") * Repeat(extra="h"),
        "decrease heading [level] <h>":
            R(Key("c-minus"), rdescript="Typora: Decrease Heading Level") * Repeat(extra="h"),
        "table":
            R(Key("c-t"), rdescript="Typora: Table"),  # could be automated.
        "code fences":
            R(Key("cs-k"), rdescript="Typora: Code Fences"),
        "math block":
            R(Key("cs-m"), rdescript="Typora: Math Block"),
        "quote":
            R(Key("cs-q"), rdescript="Typora: Quote"),
        "ordered list":
            R(Key("cs-["), rdescript="Typora: Ordered List"),
        "indent <h>":
            R(Key("cs-]"), rdescript="Typora: Indent") * Repeat(extra="h"),
        "out dent <h>":
            R(Key("cs-["), rdescript="Typora: Outdent") * Repeat(extra="h"),
        # Format
        "strong | bold":
            R(Key("c-b"), rdescript="Typora: Strong"),
        "emphasis | italicize":
            R(Key("c-i"), rdescript="Typora: Emphasis"),
        "underline":
            R(Key("c-u"), rdescript="Typora: Underline"),
        "code":
            R(Key("cs-`"), rdescript="Typora: Code"),
        "strike":
            R(Key("as-5"), rdescript="Typora: Strike"),
        "hyperlink":
            R(Key("c-k"), rdescript="Typora: Hyperlink"),
        "image":
            R(Key("cs-i"), rdescript="Typora: Image"),
        "clear [format]":
            R(Key("c-\\"), rdescript="Typora: Clear Format"),
        # View
        "[toggle] sidebar":
            R(Key("cs-l"), rdescript="Typora: Toggle Sidebar"),
        "outline":
            R(Key("cs-1"), rdescript="Typora: Outline"),
        "articles":
            R(Key("sc-2"), rdescript="Typora: Articles"),
        "file tree":
            R(Key("cs-3"), rdescript="Typora: File Tree"),
        "source code [mode]":
            R(Key("c-slash"), rdescript="Typora: Source Code Mode"),
        "focus mode":
            R(Key("f8"), rdescript="Typora: Focus Mode"),
        "typewriter [mode]":
            R(Key("f9"), rdescript="Typora: Typewriter Mode"),
        "[toggle] fullscreen":
            R(Key("f11"), rdescript="Typora: Toggler Fullscreen"),
        "actual size":
            R(Key("cs-0"), rdescript="Typora: Actual Size"),
        "zoom in <n>":
            R(Key("cs-="), rdescript="Typora: Zoom In") * Repeat(extra="n"),
        "zoom out <n>":
            R(Key("cs--"), rdescript="Typora: Zoom Out") * Repeat(extra="n"),
        "switch documnets":
            R(Key("c-tab"), rdescript="Typora: Switch Between Opened Documnets"),
        "toggle [dev] tools":
            R(Key("cs-f12"), rdescript="Typora: Toggle DevTools"),

    }

    extras = [
        Dictation("text"),
        IntegerRefST("h", 0, 6),
        IntegerRefST("n", 1, 30),
    ]

    defaults = {
        "n": 1,
        "h": 1
    }


# ---------------------------------------------------------------------------

context = AppContext(executable="typora")
control.non_ccr_app_rule(TyporaRule(), context=context)