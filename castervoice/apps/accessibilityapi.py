"""
Credit to Wolfmanstout
Command-module for Accessibility API
http://handsfreecoding.org/2018/12/27/enhanced-text-manipulation-using-accessibility-apis/

WIP - Included as a App As it only works with certain applications. 
"""
# ---------------------------------------------------------------------------

from dragonfly import (Grammar, Dictation, Function, Compound, Alternative, Literal, CursorPosition, TextQuery)
from dragonfly import get_accessibility_controller

from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule

accessibility = get_accessibility_controller()


class AccessibilityRule(MergeRule):
    pronunciation = "notepad plus plus"

    mapping = {

        # Accessibility API Mappings
        "go before <text_position_query>": Function(
            lambda text_position_query: accessibility.move_cursor(
                text_position_query, CursorPosition.BEFORE)),
        "go after <text_position_query>": Function(
            lambda text_position_query: accessibility.move_cursor(
                text_position_query, CursorPosition.AFTER)),
        "words <text_query>": Function(accessibility.select_text),
        "words <text_query> delete": Function(
            lambda text_query: accessibility.replace_text(text_query, "")),
        "replace <text_query> with <replacement>": Function(
            accessibility.replace_text),

    }
    extras = [
        Dictation("replacement"),
        Compound(
            name="text_query",
            spec=("[[([<start_phrase>] <start_relative_position> <start_relative_phrase>|<start_phrase>)] <through>] "
                  "([<end_phrase>] <end_relative_position> <end_relative_phrase>|<end_phrase>)"),
            extras=[Dictation("start_phrase", default=""),
                    Alternative([Literal("before"), Literal("after")],
                                name="start_relative_position"),
                    Dictation("start_relative_phrase", default=""),
                    Literal("through", "through", value=True, default=False),
                    Dictation("end_phrase", default=""),
                    Alternative([Literal("before"), Literal("after")],
                                name="end_relative_position"),
                    Dictation("end_relative_phrase", default="")],
            value_func=lambda node, extras: TextQuery(
                start_phrase=str(extras["start_phrase"]),
                start_relative_position=(CursorPosition[extras["start_relative_position"].upper()]
                                         if "start_relative_position" in extras else None),
                start_relative_phrase=str(extras["start_relative_phrase"]),
                through=extras["through"],
                end_phrase=str(extras["end_phrase"]),
                end_relative_position=(CursorPosition[extras["end_relative_position"].upper()]
                                       if "end_relative_position" in extras else None),
                end_relative_phrase=str(extras["end_relative_phrase"]))),
        Compound(
            name="text_position_query",
            spec="<phrase> [<relative_position> <relative_phrase>]",
            extras=[Dictation("phrase", default=""),
                    Alternative([Literal("before"), Literal("after")],
                                name="relative_position"),
                    Dictation("relative_phrase", default="")],
            value_func=lambda node, extras: TextQuery(
                end_phrase=str(extras["phrase"]),
                end_relative_position=(CursorPosition[extras["relative_position"].upper()]
                                       if "relative_position" in extras else None),
                end_relative_phrase=str(extras["relative_phrase"])))
    ]

    defaults = {

    }


context = AppContext(executable="chrome") \
          | AppContext(executable="firefox") \
          | AppContext(executable="gitter") \
          | AppContext(executable="discord")

grammar = Grammar("AccessibilityAPI", context=context)

if settings.SETTINGS["apps"]["accessibilityapi"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(AccessibilityRule())
    else:
        rule = AccessibilityRule(name="accessibility rule")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
