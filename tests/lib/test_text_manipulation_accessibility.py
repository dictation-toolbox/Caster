import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from castervoice.rules.core.text_manipulation_rules import accessibility_text
from castervoice.rules.core.text_manipulation_rules import text_manipulation_support


class _FakeFocusedText(object):

    def __init__(self, text, cursor):
        self.expanded_text = text
        self.cursor = cursor
        self.selected_ranges = []
        self.cursor_offsets = []

    def select_range(self, start, end):
        self.selected_ranges.append((start, end))

    def set_cursor(self, offset):
        self.cursor = offset
        self.cursor_offsets.append(offset)


class _FakeFocused(object):

    def __init__(self, focused_text, editable=True):
        self.focused_text = focused_text
        self.editable = editable

    def is_editable(self):
        return self.editable

    def as_text(self):
        return self.focused_text


class _FakeAccessibilityContext(object):

    def __init__(self, focused):
        self.focused = focused


class _FakeOsController(object):

    def __init__(self, focused):
        self.focused = focused

    def run_sync(self, callback):
        return callback(_FakeAccessibilityContext(self.focused))


class _FakeController(object):

    def __init__(self, focused):
        self.os_controller = _FakeOsController(focused)


class _FakeTextAction(object):
    calls = []

    def __init__(self, spec, *args, **kwargs):
        self.spec = spec

    def execute(self):
        self.calls.append(self.spec)


class _FakeKeyAction(object):
    calls = []

    def __init__(self, spec, *args, **kwargs):
        self.spec = spec

    def execute(self):
        self.calls.append(self.spec)


class TestTextManipulationAccessibility(unittest.TestCase):

    def setUp(self):
        self._old_controller = accessibility_text.dragonfly_get_accessibility_controller
        self._old_text = accessibility_text.Text
        self._old_key = accessibility_text.Key
        _FakeTextAction.calls = []
        _FakeKeyAction.calls = []
        accessibility_text.Text = _FakeTextAction
        accessibility_text.Key = _FakeKeyAction

    def tearDown(self):
        accessibility_text.dragonfly_get_accessibility_controller = self._old_controller
        accessibility_text.Text = self._old_text
        accessibility_text.Key = self._old_key

    def _install_focused_text(self, text, cursor, editable=True):
        focused_text = _FakeFocusedText(text, cursor)
        focused = _FakeFocused(focused_text, editable=editable)
        controller = _FakeController(focused)
        accessibility_text.dragonfly_get_accessibility_controller = lambda: controller
        return focused_text

    def test_select_phrase_uses_current_line_to_the_right(self):
        text = "alpha target\nbeta target"
        focused_text = self._install_focused_text(text, 0)

        self.assertTrue(accessibility_text.select_phrase("target", "right", 0, 1, "dictation"))

        self.assertEqual([(6, 12)], focused_text.selected_ranges)

    def test_left_window_includes_requested_previous_line_with_crlf(self):
        text = "one target\r\ntwo target\r\nthree target"
        focused_text = self._install_focused_text(text, text.index("three"))
        expected_start = text.index("target", text.index("two"))

        self.assertTrue(accessibility_text.select_phrase("target", "left", 1, 1, "dictation"))

        self.assertEqual([(expected_start, expected_start + len("target"))], focused_text.selected_ranges)

    def test_text_node_delimiter_limits_current_line_window(self):
        text = "first target" + accessibility_text.TEXT_NODE_DELIMITER + "second target"
        focused_text = self._install_focused_text(text, len(text))
        expected_start = text.index("target", text.index("second"))

        self.assertTrue(accessibility_text.select_phrase("target", "left", 0, 1, "dictation"))

        self.assertEqual([(expected_start, expected_start + len("target"))], focused_text.selected_ranges)

    def test_right_window_includes_requested_next_line(self):
        text = "alpha\nbeta target\ngamma target"
        focused_text = self._install_focused_text(text, 0)
        expected_start = text.index("target")

        self.assertTrue(accessibility_text.select_phrase("target", "right", 1, 1, "dictation"))

        self.assertEqual([(expected_start, expected_start + len("target"))], focused_text.selected_ranges)

    def test_move_until_phrase_sets_requested_boundary(self):
        text = "alpha beta gamma"
        focused_text = self._install_focused_text(text, text.index(" gamma"))

        self.assertTrue(accessibility_text.move_until_phrase("left", "before", "beta", 0, 1, "dictation"))

        self.assertEqual([6], focused_text.cursor_offsets)

    def test_select_until_phrase_uses_cursor_to_requested_boundary(self):
        text = "alpha beta gamma"
        focused_text = self._install_focused_text(text, text.index(" beta"))

        self.assertTrue(accessibility_text.select_until_phrase("right", "beta", "after", 0, 1, "dictation"))

        self.assertEqual([(5, 10)], focused_text.selected_ranges)

    def test_replace_phrase_escapes_percent_for_text_action(self):
        text = "alpha target"
        focused_text = self._install_focused_text(text, 0)

        self.assertTrue(accessibility_text.replace_phrase_with_phrase("target", "100%", "right", 0, 1, "dictation"))

        self.assertEqual([(6, 12)], focused_text.selected_ranges)
        self.assertEqual(["100%%"], _FakeTextAction.calls)

    def test_remove_phrase_includes_preceding_space_for_dictation(self):
        text = "alpha target beta"
        focused_text = self._install_focused_text(text, text.index(" beta"))

        self.assertTrue(accessibility_text.remove_phrase_from_text("target", "left", 0, 1, "dictation"))

        self.assertEqual([(5, 12)], focused_text.selected_ranges)
        self.assertEqual(["backspace"], _FakeKeyAction.calls)

    def test_non_editable_focus_falls_back_without_selection(self):
        text = "alpha target"
        focused_text = self._install_focused_text(text, 0, editable=False)

        self.assertFalse(accessibility_text.select_phrase("target", "right", 0, 1, "dictation"))

        self.assertEqual([], focused_text.selected_ranges)

    def test_support_function_returns_before_clipboard_fallback_when_accessibility_handles_it(self):
        with mock.patch.object(text_manipulation_support.accessibility_text, "select_phrase", return_value=True):
            with mock.patch.object(text_manipulation_support, "get_application") as get_application:
                text_manipulation_support.select_phrase("target", "right", 0, 1, "dictation")

        self.assertFalse(get_application.called)


if __name__ == "__main__":
    unittest.main()
