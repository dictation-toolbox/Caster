import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from castervoice.rules.core.text_manipulation_rules import text_manipulation_support as support


class FakeFocusedText(object):
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


class FakeAccessibilityContext(object):
    def __init__(self, focused_text):
        self.focused = focused_text


class FakeOsController(object):
    def __init__(self, focused_text):
        self.focused_text = focused_text

    def run_sync(self, callback):
        return callback(FakeAccessibilityContext(self.focused_text))


class FakeController(object):
    def __init__(self, focused_text):
        self.os_controller = FakeOsController(focused_text)


class TextManipulationAccessibilityTest(unittest.TestCase):
    def test_get_accessibility_phrase_range_searches_left_of_cursor(self):
        text = "alpha beta gamma beta delta"
        focused_text = FakeFocusedText(text, text.index(" delta"))

        self.assertEqual(
            (17, 21),
            support.get_accessibility_phrase_range(focused_text, "beta", "left", 0, 1, "dictation")
        )

    def test_get_accessibility_phrase_range_searches_right_of_cursor(self):
        text = "alpha beta gamma beta delta"
        focused_text = FakeFocusedText(text, text.index("gamma"))

        self.assertEqual(
            (17, 21),
            support.get_accessibility_phrase_range(focused_text, "beta", "right", 0, 1, "dictation")
        )

    def test_get_accessibility_phrase_range_respects_line_window(self):
        text = "alpha target\nbeta target beta\nomega target"
        focused_text = FakeFocusedText(text, text.index("\nomega"))

        self.assertEqual(
            (18, 24),
            support.get_accessibility_phrase_range(focused_text, "target", "left", 0, 1, "dictation")
        )

    def test_get_accessibility_until_range_uses_requested_boundary(self):
        text = "alpha beta gamma"
        focused_text = FakeFocusedText(text, text.index(" beta"))

        self.assertEqual(
            (5, 10),
            support.get_accessibility_until_range(focused_text, "beta", "right", "after", 0, 1, "dictation")
        )

    def test_accessibility_select_phrase_uses_focused_text(self):
        text = "alpha beta gamma"
        focused_text = FakeFocusedText(text, text.index(" gamma"))

        with mock.patch.object(support, "get_accessibility_text", return_value=(FakeController(focused_text), focused_text)):
            self.assertTrue(support.accessibility_select_phrase("beta", "left", 0, 1, "dictation"))

        self.assertEqual((6, 10), focused_text.selected_range)

    def test_accessibility_move_until_phrase_sets_cursor(self):
        text = "alpha beta gamma"
        focused_text = FakeFocusedText(text, text.index(" gamma"))

        with mock.patch.object(support, "get_accessibility_text", return_value=(FakeController(focused_text), focused_text)):
            self.assertTrue(support.accessibility_move_until_phrase("left", "before", "beta", 0, 1, "dictation"))

        self.assertEqual(6, focused_text.cursor)


if __name__ == "__main__":
    unittest.main()
