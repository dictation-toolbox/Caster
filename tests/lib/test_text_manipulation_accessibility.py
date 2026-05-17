import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from castervoice.rules.core.text_manipulation_rules import text_manipulation_support as support


class _FakeFocusedText(object):

    def __init__(self, text, cursor):
        self.expanded_text = text
        self.cursor = cursor
        self.selected_range = None

    def as_text(self):
        return self

    def select_range(self, start, end):
        self.selected_range = (start, end)

    def set_cursor(self, offset):
        self.cursor = offset


class _FakeAccessibilityContext(object):

    def __init__(self, focused_text):
        self.focused = focused_text


class _FakeOsController(object):

    def __init__(self, focused_text):
        self.focused_text = focused_text

    def run_sync(self, callback):
        return callback(_FakeAccessibilityContext(self.focused_text))


class _FakeController(object):

    def __init__(self, focused_text):
        self.os_controller = _FakeOsController(focused_text)


class TestTextManipulationAccessibility(unittest.TestCase):

    def test_target_range_uses_left_side_of_cursor(self):
        text = "alpha beta gamma beta delta"
        cursor = text.index(" delta")
        snapshot = {"text": text, "cursor": cursor}

        self.assertEqual(
            (17, 21),
            support._get_accessibility_target_range(snapshot, "beta", "left", 0, 1, "dictation")
        )

    def test_target_range_uses_right_side_of_cursor(self):
        text = "alpha beta gamma beta delta"
        cursor = text.index("gamma")
        snapshot = {"text": text, "cursor": cursor}

        self.assertEqual(
            (17, 21),
            support._get_accessibility_target_range(snapshot, "beta", "right", 0, 1, "dictation")
        )

    def test_target_range_respects_current_line_window(self):
        text = "alpha target\nbeta target beta\nomega target"
        cursor = text.index("\nomega")
        snapshot = {"text": text, "cursor": cursor}

        self.assertEqual(
            (18, 24),
            support._get_accessibility_target_range(snapshot, "target", "left", 0, 1, "dictation")
        )

    def test_until_range_selects_from_cursor_to_phrase_boundary(self):
        text = "alpha beta gamma"
        cursor = text.index(" beta")
        snapshot = {"text": text, "cursor": cursor}

        self.assertEqual(
            (5, 10),
            support._get_accessibility_until_range(snapshot, "beta", "right", "after", 0, 1, "dictation")
        )

    def test_select_phrase_uses_focused_accessibility_text(self):
        text = "alpha beta gamma"
        focused_text = _FakeFocusedText(text, text.index(" gamma"))
        controller = _FakeController(focused_text)
        snapshot = {"text": text, "cursor": focused_text.cursor}

        with mock.patch.object(support, "_get_accessibility_context", return_value=(controller, snapshot)):
            self.assertTrue(support._accessibility_select_phrase("beta", "left", 0, 1, "dictation"))

        self.assertEqual((6, 10), focused_text.selected_range)

    def test_move_until_phrase_sets_cursor_to_requested_boundary(self):
        text = "alpha beta gamma"
        focused_text = _FakeFocusedText(text, text.index(" gamma"))
        controller = _FakeController(focused_text)
        snapshot = {"text": text, "cursor": focused_text.cursor}

        with mock.patch.object(support, "_get_accessibility_context", return_value=(controller, snapshot)):
            self.assertTrue(support._accessibility_move_until_phrase("left", "before", "beta", 0, 1, "dictation"))

        self.assertEqual(6, focused_text.cursor)


if __name__ == "__main__":
    unittest.main()
