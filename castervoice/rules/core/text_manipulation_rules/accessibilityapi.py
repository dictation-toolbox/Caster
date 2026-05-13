"""
Text Select-and-Say style editing commands backed by Dragonfly's
OS-independent accessibility controller.

Dragonfly currently exposes this support for selected applications and
platforms, so this Caster rule is app-scoped and opt-in.
"""
from dragonfly import (
    Alternative,
    Compound,
    CursorPosition,
    Dictation,
    Function,
    Literal,
    TextQuery,
    get_accessibility_controller,
)

from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule


def _get_controller():
    controller = get_accessibility_controller()
    if controller is None:
        print("Dragonfly accessibility controller is not available.")
    return controller


def _controller_call(method_name, *args):
    controller = _get_controller()
    if controller is None:
        return None
    return getattr(controller, method_name)(*args)


def _cursor_position(extras, name):
    if name not in extras:
        return None
    return CursorPosition[extras[name].upper()]


def make_text_query(node, extras):
    return TextQuery(
        start_phrase=str(extras["start_phrase"]),
        start_relative_position=_cursor_position(extras, "start_relative_position"),
        start_relative_phrase=str(extras["start_relative_phrase"]),
        through=extras["through"],
        end_phrase=str(extras["end_phrase"]),
        end_relative_position=_cursor_position(extras, "end_relative_position"),
        end_relative_phrase=str(extras["end_relative_phrase"]),
    )


def make_text_position_query(node, extras):
    return TextQuery(
        end_phrase=str(extras["phrase"]),
        end_relative_position=_cursor_position(extras, "relative_position"),
        end_relative_phrase=str(extras["relative_phrase"]),
    )


def move_before(text_position_query):
    return _controller_call("move_cursor", text_position_query, CursorPosition.BEFORE)


def move_after(text_position_query):
    return _controller_call("move_cursor", text_position_query, CursorPosition.AFTER)


def select_text(text_query):
    return _controller_call("select_text", text_query)


def delete_text(text_query):
    return _controller_call("replace_text", text_query, "")


def replace_text(text_query, replacement):
    return _controller_call("replace_text", text_query, str(replacement))


class AccessibilityRule(MergeRule):
    pronunciation = "accessibility api"

    mapping = {
        "go before <text_position_query>": Function(move_before),
        "go after <text_position_query>": Function(move_after),
        "words <text_query>": Function(select_text),
        "words <text_query> delete": Function(delete_text),
        "replace <text_query> with <replacement>": Function(replace_text),
    }

    extras = [
        Dictation("replacement"),
        Compound(
            name="text_query",
            spec=("[[([<start_phrase>] <start_relative_position> <start_relative_phrase>|<start_phrase>)] <through>] "
                  "([<end_phrase>] <end_relative_position> <end_relative_phrase>|<end_phrase>)"),
            extras=[
                Dictation("start_phrase", default=""),
                Alternative([Literal("before"), Literal("after")], name="start_relative_position"),
                Dictation("start_relative_phrase", default=""),
                Literal("through", "through", value=True, default=False),
                Dictation("end_phrase", default=""),
                Alternative([Literal("before"), Literal("after")], name="end_relative_position"),
                Dictation("end_relative_phrase", default=""),
            ],
            value_func=make_text_query,
        ),
        Compound(
            name="text_position_query",
            spec="<phrase> [<relative_position> <relative_phrase>]",
            extras=[
                Dictation("phrase", default=""),
                Alternative([Literal("before"), Literal("after")], name="relative_position"),
                Dictation("relative_phrase", default=""),
            ],
            value_func=make_text_position_query,
        ),
    ]

    defaults = {}


def get_rule():
    details = RuleDetails(executable=["gitter", "firefox", "chrome"],
                          ccrtype=CCRType.APP)
    return AccessibilityRule, details
