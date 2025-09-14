"""Select-and-Say PoC grammar using dtactions.a11y.

This rule provides voice-driven text selection and navigation capabilities
using the dtactions accessibility layer. It demonstrates cross-platform
Select-and-Say functionality similar to Dragon's built-in commands.

Voice Commands:
- "select <text>" - Select first occurrence of text
- "select <text> through <text>" - Select from first to second text (inclusive)
- "replace <text> with <text>" - Replace first occurrence of text
- "go to start of <text>" - Move cursor to start of found text
- "go to end of <text>" - Move cursor to end of found text

The grammar gracefully handles cases where no accessible control is focused
or when the requested text cannot be found.
"""

from dragonfly import Function, Dictation, Choice

try:
    from dtactions.a11y import get_adapter, TextQuery, CursorPosition
    from dtactions.a11y.exceptions import UnsupportedControlError, NotFoundError, NotEditableError
    DTACTIONS_AVAILABLE = True
except ImportError:
    DTACTIONS_AVAILABLE = False

from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


def _safe_get_adapter():
    """Safely get accessibility adapter with error handling."""
    if not DTACTIONS_AVAILABLE:
        print("dtactions.a11y not available - install dtactions[a11y_win] for Select-and-Say")
        return None

    try:
        return get_adapter()
    except UnsupportedControlError as e:
        print(f"Accessibility adapter not available: {e}")
        return None


def select_text_command(text1, text2=None):
    """Select text using accessibility adapter.

    Args:
        text1: Start text to find
        text2: End text (optional, for range selection)
    """
    adapter = _safe_get_adapter()
    if adapter is None:
        return

    try:
        if not adapter.is_editable_focused():
            print("No editable control is focused")
            return

        # Create query based on parameters
        if text2:
            query = TextQuery(start=str(text1), end=str(text2), through=True)
            print(f"Selecting from '{text1}' through '{text2}'")
        else:
            query = TextQuery(start=str(text1))
            print(f"Selecting '{text1}'")

        adapter.select_text(query)

    except NotFoundError:
        if text2:
            print(f"Could not find text from '{text1}' to '{text2}'")
        else:
            print(f"Could not find text '{text1}'")
    except UnsupportedControlError:
        print("Current control does not support text selection")
    except Exception as e:
        print(f"Text selection failed: {e}")


def replace_text_command(find_text, replacement_text):
    """Replace text using accessibility adapter.

    Args:
        find_text: Text to find and replace
        replacement_text: Replacement text
    """
    adapter = _safe_get_adapter()
    if adapter is None:
        return

    try:
        if not adapter.is_editable_focused():
            print("No editable control is focused")
            return

        query = TextQuery(start=str(find_text))
        print(f"Replacing '{find_text}' with '{replacement_text}'")

        adapter.replace_text(query, str(replacement_text))

    except NotFoundError:
        print(f"Could not find text '{find_text}' to replace")
    except NotEditableError:
        print("Current control is read-only")
    except UnsupportedControlError:
        print("Current control does not support text replacement")
    except Exception as e:
        print(f"Text replacement failed: {e}")


def move_cursor_command(text, position_name):
    """Move cursor relative to found text.

    Args:
        text: Text to find as reference point
        position_name: Where to position cursor ("start" or "end")
    """
    adapter = _safe_get_adapter()
    if adapter is None:
        return

    try:
        if not adapter.is_editable_focused():
            print("No editable control is focused")
            return

        # Map voice command to CursorPosition
        position_map = {
            "start": CursorPosition.START,
            "end": CursorPosition.END
        }

        position = position_map.get(position_name, CursorPosition.START)
        query = TextQuery(start=str(text))

        print(f"Moving cursor to {position_name} of '{text}'")
        adapter.move_cursor(query, position)

    except NotFoundError:
        print(f"Could not find text '{text}'")
    except UnsupportedControlError:
        print("Current control does not support cursor positioning")
    except Exception as e:
        print(f"Cursor positioning failed: {e}")


class SelectAndSay(MergeRule):
    """Select-and-Say grammar using dtactions.a11y accessibility layer."""

    pronunciation = "select and say"

    mapping = {
        # Basic text selection
        "select <text>":
            R(Function(select_text_command), rspec="select text"),

        # Range selection (from text1 through text2)
        "select <text> through <text2>":
            R(Function(select_text_command), rspec="select text range"),

        # Text replacement
        "replace <text> with <text2>":
            R(Function(replace_text_command), rspec="replace text"),

        # Cursor positioning
        "go to <position> of <text>":
            R(Function(move_cursor_command), rspec="move cursor"),
    }

    extras = [
        Dictation("text"),
        Dictation("text2"),
        Choice("position", {
            "start": "start",
            "end": "end"
        })
    ]

    defaults = {
        "text": "",
        "text2": "",
        "position": "start"
    }


def get_rule():
    """Return rule and details for Caster's rule management system."""
    details = RuleDetails(ccrtype=CCRType.GLOBAL)

    if not DTACTIONS_AVAILABLE:
        details.enabled = False
        print("SelectAndSay rule disabled: dtactions.a11y not available")
        print("Install with: pip install dtactions[a11y_win]")

    return SelectAndSay, details