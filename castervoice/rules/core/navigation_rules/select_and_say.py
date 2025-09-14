"""Select-and-Say grammar using dragonfly accessibility.

This rule provides voice-driven text selection and navigation capabilities
using dragonfly's built-in accessibility layer. It demonstrates cross-platform
Select-and-Say functionality similar to Dragon's built-in commands.

Voice Commands:
- "select <text>" - Select first occurrence of text
- "select <text> through <text>" - Select from first to second text (inclusive)
- "replace <text> with <text>" - Replace first occurrence of text
- "go to before <text>" - Move cursor before found text
- "go to after <text>" - Move cursor after found text

The grammar gracefully handles cases where no accessible control is focused
or when the requested text cannot be found.
"""

import logging
from dragonfly import Function, Dictation, Choice

try:
    from dragonfly.accessibility import get_accessibility_controller
    from dragonfly.accessibility.utils import TextQuery
    from dragonfly.accessibility import CursorPosition
    from dragonfly.accessibility.base import AccessibilityError, UnsupportedSelectionError
    DRAGONFLY_ACCESSIBILITY_AVAILABLE = True
except ImportError:
    DRAGONFLY_ACCESSIBILITY_AVAILABLE = False

from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R

# Global controller instance
_accessibility_controller = None
_log = logging.getLogger(__name__)


def _get_accessibility_controller():
    """Get accessibility controller with error handling."""
    global _accessibility_controller

    if not DRAGONFLY_ACCESSIBILITY_AVAILABLE:
        _log.warning("dragonfly accessibility not available - update dragonfly for Select-and-Say")
        return None

    try:
        if _accessibility_controller is None:
            _accessibility_controller = get_accessibility_controller()
        return _accessibility_controller
    except Exception as e:
        _log.error(f"Accessibility controller not available: {e}")
        return None


def select_text_command(text, text2=None):
    """Select text using dragonfly accessibility.

    Args:
        text: Start text to find
        text2: End text (optional, for range selection)
    """
    controller = _get_accessibility_controller()
    if controller is None:
        return

    try:
        if not controller.is_editable_focused():
            _log.info("No editable control is focused")
            return

        # Create query based on parameters
        if text2:
            # Range selection: "select hello through world"
            query = TextQuery(start_phrase=str(text), end_phrase=str(text2), through=True)
            _log.info(f"Selecting from '{text}' through '{text2}'")
        else:
            # Single text selection: "select hello"
            # For single phrase, use end_phrase only
            query = TextQuery(end_phrase=str(text))
            _log.info(f"Selecting '{text}'")

        success = controller.select_text(query)
        if not success:
            if text2:
                _log.warning(f"Could not find text from '{text}' to '{text2}'")
            else:
                _log.warning(f"Could not find text '{text}'")

    except UnsupportedSelectionError:
        _log.warning("Current control does not support text selection")
    except AccessibilityError as e:
        _log.error(f"Accessibility error: {e}")
    except Exception as e:
        _log.error(f"Text selection failed: {e}")


def replace_text_command(text, text2):
    """Replace text using dragonfly accessibility.

    Args:
        text: Text to find and replace
        text2: Replacement text
    """
    controller = _get_accessibility_controller()
    if controller is None:
        return

    try:
        if not controller.is_editable_focused():
            _log.info("No editable control is focused")
            return

        # Create query for text to replace
        query = TextQuery(end_phrase=str(text))
        _log.info(f"Replacing '{text}' with '{text2}'")

        success = controller.replace_text(query, str(text2))
        if not success:
            _log.warning(f"Could not find text '{text}' to replace")

    except UnsupportedSelectionError:
        _log.warning("Current control does not support text replacement")
    except AccessibilityError as e:
        _log.error(f"Accessibility error: {e}")
    except Exception as e:
        _log.error(f"Text replacement failed: {e}")


def move_cursor_command(text, position):
    """Move cursor relative to found text.

    Args:
        text: Text to find as reference point
        position: Where to position cursor ("before" or "after")
    """
    controller = _get_accessibility_controller()
    if controller is None:
        return

    try:
        if not controller.is_editable_focused():
            _log.info("No editable control is focused")
            return

        # Map voice command to CursorPosition
        position_map = {
            "before": CursorPosition.BEFORE,
            "after": CursorPosition.AFTER
        }

        cursor_pos = position_map.get(position, CursorPosition.BEFORE)
        query = TextQuery(end_phrase=str(text))

        _log.info(f"Moving cursor {position} '{text}'")
        success = controller.move_cursor(query, cursor_pos)
        if not success:
            _log.warning(f"Could not find text '{text}'")

    except UnsupportedSelectionError:
        _log.warning("Current control does not support cursor positioning")
    except AccessibilityError as e:
        _log.error(f"Accessibility error: {e}")
    except Exception as e:
        _log.error(f"Cursor positioning failed: {e}")


class SelectAndSay(MergeRule):
    """Select-and-Say grammar using dragonfly's accessibility layer."""

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
        "go to <position> <text>":
            R(Function(move_cursor_command), rspec="move cursor"),
    }

    extras = [
        Dictation("text"),
        Dictation("text2"),
        Choice("position", {
            "before": "before",
            "after": "after"
        })
    ]

    defaults = {
        "text": "",
        "text2": "",
        "position": "before"
    }


def get_rule():
    """Return rule and details for Caster's rule management system."""
    details = RuleDetails(ccrtype=CCRType.GLOBAL)

    if not DRAGONFLY_ACCESSIBILITY_AVAILABLE:
        details.enabled = False
        _log.warning("SelectAndSay rule disabled: dragonfly accessibility not available")
        _log.info("Update dragonfly to enable Select-and-Say functionality")

    return SelectAndSay, details