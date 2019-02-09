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


class TyporaRule(MergeRule):
    pronunciation = "tie poor a"

    mapping = {
        # File
        "new markdown":
            R(Key("c-n"), rdescript="Typora: New Markdown Document"),
        "new window":
            R(Key("cs-n"), rdescript="Typora: New Window"),
        # "new tab":
        # R(Key(""), rdescript="Typora: New Tab"), # Not implemented in Windows OS
        "open file":
            R(Key("c-o"), rdescript="Typora: Open File"),
        "open [file] quickly":
            R(Key("c-p"), rdescript="Typora: Open Quickly"),
        "reopen [closed] file":
            R(Key("cs-t"), rdescript="Typora: Reopen Closed File"),
        "save as":
            R(Key("cs-s"), rdescript="Typora: Save As"),
        "close file":
            R(Key("c-w"), rdescript="Typora: Close"),
        # Edit
        "new paragraph":
            R(Key("enter"), rdescript="Typora: New Paragraph") * Repeat(extra="n"),
        "new line":
            R(Key("s-enter"), rdescript="Typora: New Line") * Repeat(extra="n"),
        "copy [as] markdown":
            R(Key("cs-c"), rdescript="Typora: Copy as Markdown"),
        "delete row":
            R(Key("cs-backspace"), rdescript="Typora: Delete Row") * Repeat(extra="n"),
        "select [cell | scope]":
            R(Key("c-e"), rdescript="Typora: Select Style Scope or Cell"),
        "select word":
            R(Key("c-d"), rdescript="Typora: Select Word") * Repeat(extra="n"),
        "delete word":
            R(Key("cs-d"), rdescript="Typora: Delete Word") * Repeat(extra="n"),
        "jump [to] top":
            R(Key("c-home"), rdescript="Typora: Jump to Top"),
        "jump [to] selection":
            R(Key("c-j"), rdescript="Typora: Jump to Selection"),
        "jump [to] buttom":
            R(Key("c-end"), rdescript="Typora: Jump to Buttom"),
        "find":
            R(Key("c-f"), rdescript="Typora: Find"),
        "find next":
            R(Key("f3"), rdescript="Typora: Find Next"),
        "replace":
            R(Key("c-h"), rdescript="Typora: Replace"),
        # Paragraph
        "heading <n>":
            R(Key("c-%(n)d"), rdescript="Typora: Heading 1 to 6"),
        "paragraph":
            R(Key("c-o"), rdescript="Typora: Paragraph"),
        "increase heading level":
            R(Key("c-equal"), rdescript="Typora: Increase Heading Level") * Repeat(extra="n"),
        "decrease heading level":
            R(Key("c-minus"), rdescript="Typora: Decrease Heading Level") * Repeat(extra="n"),
        "table":
            R(Key("c-t"), rdescript="Typora: Table"),
        "code fences":
            R(Key("cs-k"), rdescript="Typora: Code Fences"),
        "math block":
            R(Key("cs-m"), rdescript="Typora: Math Block"),
        "quote":
            R(Key("cs-q"), rdescript="Typora: Quote"),
        "ordered list":
            R(Key("cs-["), rdescript="Typora: Ordered List"),
        "indent":
            R(Key("cs-]"), rdescript="Typora: Indent") * Repeat(extra="n"),
        "outdent":
            R(Key("c-["), rdescript="Typora: Outdent") * Repeat(extra="n"),
        # Format
        "strong":
            R(Key("c-b"), rdescript="Typora: Strong"),
        "emphasis":
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
        "clear format":
            R(Key("cs-backspace"), rdescript="Typora: Clear Format"),
        # View
        "toggle sidebar":
            R(Key("cs-l"), rdescript="Typora: Toggle Sidebar"),
        "outline":
            R(Key("cs-1"), rdescript="Typora: Outline"),
        "articles":
            R(Key("sc-2"), rdescript="Typora: Articles"),
        "file tree":
            R(Key("cs-3"), rdescript="Typora: File Tree"),
        "source [code] mode":
            R(Key("c-backspace"), rdescript="Typora: Source Code Mode"),
        "focus mode":
            R(Key("f8"), rdescript="Typora: Focus Mode"),
        "typewriter mode":
            R(Key("f9"), rdescript="Typora: Typewriter Mode"),
        "toggler fullscreen":
            R(Key("f11"), rdescript="Typora: Toggler Fullscreen"),
        "actual size":
            R(Key("cs-0"), rdescript="Typora: Actual Size"),
        "zoom in":
            R(Key("cs-="), rdescript="Typora: Zoom In") * Repeat(extra="n"),
        "zoom out":
            R(Key("cs--"), rdescript="Typora: Zoom Out") * Repeat(extra="n"),
        "switch [between opened] documnets":
            R(Key("c-tab"), rdescript="Typora: Switch Between Opened Documnets"),
        "toggle [dev] tools":
            R(Key("cs-i"), rdescript="Typora: Toggle DevTools"),

    }
    extras = [
        Dictation("text"),
        IntegerRefST("n", 1, 6),
    ]


# ---------------------------------------------------------------------------

context = AppContext(executable="typora")
grammar = Grammar("typora", context=context)

if settings.SETTINGS["apps"]["typora"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(TyporaRule())
        print("added Typora")
    else:
        rule = TyporaRule(name="typora")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
