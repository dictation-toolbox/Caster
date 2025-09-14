"""Unit tests for Select-and-Say grammar integration."""

import pytest
from unittest.mock import Mock, patch

from castervoice.rules.core.navigation_rules.select_and_say import (
    SelectAndSay, get_rule, select_text_command, replace_text_command, move_cursor_command
)


class TestSelectAndSayGrammar:
    """Test Select-and-Say grammar structure and integration."""

    def test_grammar_creation(self):
        """Test that SelectAndSay grammar can be created."""
        rule_class, details = get_rule()
        assert rule_class == SelectAndSay
        assert details is not None

        # Create rule instance
        rule = rule_class()
        assert rule.pronunciation == "select and say"

        # Check that mapping contains expected commands
        expected_commands = [
            "select <text>",
            "select <text> through <text2>",
            "replace <text> with <text2>",
            "go to <position> <text>"  # Updated for dragonfly version
        ]

        for command in expected_commands:
            assert command in rule.mapping, f"Missing command: {command}"

    def test_grammar_extras_and_defaults(self):
        """Test grammar extras and defaults configuration."""
        rule = SelectAndSay()

        # Check extras are properly configured
        extra_names = [extra.name for extra in rule.extras]
        assert "text" in extra_names
        assert "text2" in extra_names
        assert "position" in extra_names

        # Check defaults
        assert "text" in rule.defaults
        assert "text2" in rule.defaults
        assert "position" in rule.defaults


class TestSelectAndSayCommands:
    """Test Select-and-Say command functions with mocked dragonfly controller."""

    @patch('castervoice.rules.core.navigation_rules.select_and_say._get_accessibility_controller')
    def test_select_text_command_success(self, mock_get_controller):
        """Test successful text selection."""
        mock_controller = Mock()
        mock_controller.is_editable_focused.return_value = True
        mock_controller.select_text.return_value = True
        mock_get_controller.return_value = mock_controller

        # Test single text selection
        select_text_command("hello")

        mock_controller.is_editable_focused.assert_called_once()
        mock_controller.select_text.assert_called_once()

        # Verify TextQuery was created correctly for dragonfly API
        call_args = mock_controller.select_text.call_args[0]
        query = call_args[0]
        # In dragonfly API, single selection uses end_phrase
        assert hasattr(query, 'end_phrase')

    @patch('castervoice.rules.core.navigation_rules.select_and_say._get_accessibility_controller')
    def test_select_text_range_command(self, mock_get_controller):
        """Test range text selection."""
        mock_controller = Mock()
        mock_controller.is_editable_focused.return_value = True
        mock_controller.select_text.return_value = True
        mock_get_controller.return_value = mock_controller

        # Test range selection
        select_text_command("start", "end")

        # Verify TextQuery was created for range selection
        call_args = mock_controller.select_text.call_args[0]
        query = call_args[0]
        assert hasattr(query, 'start_phrase')
        assert hasattr(query, 'end_phrase')
        assert hasattr(query, 'through')

    @patch('castervoice.rules.core.navigation_rules.select_and_say._get_accessibility_controller')
    def test_select_text_no_control_focused(self, mock_get_controller, capsys):
        """Test behavior when no editable control is focused."""
        mock_controller = Mock()
        mock_controller.is_editable_focused.return_value = False
        mock_get_controller.return_value = mock_controller

        select_text_command("hello")

        # Should not attempt selection
        mock_controller.select_text.assert_not_called()

        # Should print informative message
        captured = capsys.readouterr()
        assert "No editable control is focused" in captured.out

    @patch('castervoice.rules.core.navigation_rules.select_and_say._get_accessibility_controller')
    def test_replace_text_command_success(self, mock_get_controller):
        """Test successful text replacement."""
        mock_controller = Mock()
        mock_controller.is_editable_focused.return_value = True
        mock_controller.replace_text.return_value = True
        mock_get_controller.return_value = mock_controller

        replace_text_command("old", "new")

        mock_controller.replace_text.assert_called_once()

        # Verify parameters
        call_args = mock_controller.replace_text.call_args[0]
        query = call_args[0]
        replacement = call_args[1]
        assert hasattr(query, 'end_phrase')  # Dragonfly API uses end_phrase for single selection
        assert replacement == "new"

    @patch('castervoice.rules.core.navigation_rules.select_and_say._get_accessibility_controller')
    def test_move_cursor_command_success(self, mock_get_controller):
        """Test successful cursor movement."""
        mock_controller = Mock()
        mock_controller.is_editable_focused.return_value = True
        mock_controller.move_cursor.return_value = True
        mock_get_controller.return_value = mock_controller

        move_cursor_command("target", "before")

        mock_controller.move_cursor.assert_called_once()

        # Verify parameters
        call_args = mock_controller.move_cursor.call_args[0]
        query = call_args[0]
        position = call_args[1]
        assert hasattr(query, 'end_phrase')
        # Position should be CursorPosition enum value
        from dragonfly.accessibility import CursorPosition
        assert position == CursorPosition.BEFORE

    @patch('castervoice.rules.core.navigation_rules.select_and_say._get_accessibility_controller')
    def test_controller_not_available(self, mock_get_controller, capsys):
        """Test behavior when dragonfly controller is not available."""
        mock_get_controller.return_value = None

        select_text_command("hello")

        # Should not crash, just return early
        captured = capsys.readouterr()
        # May have printed a message, but should not crash

    @patch('castervoice.rules.core.navigation_rules.select_and_say._get_accessibility_controller')
    def test_error_handling(self, mock_get_controller, capsys):
        """Test error handling for various exception types."""
        from dragonfly.accessibility.base import UnsupportedSelectionError, AccessibilityError

        mock_controller = Mock()
        mock_controller.is_editable_focused.return_value = True
        mock_get_controller.return_value = mock_controller

        # Test UnsupportedSelectionError handling
        mock_controller.select_text.side_effect = UnsupportedSelectionError("Control not supported")
        select_text_command("hello")

        captured = capsys.readouterr()
        assert "does not support" in captured.out

        # Test generic AccessibilityError handling
        mock_controller.select_text.side_effect = AccessibilityError("Generic accessibility error")
        select_text_command("hello2")

        captured = capsys.readouterr()
        assert "Accessibility error" in captured.out


class TestSelectAndSayIntegration:
    """Test integration aspects of Select-and-Say grammar."""

    @patch('castervoice.rules.core.navigation_rules.select_and_say.DRAGONFLY_ACCESSIBILITY_AVAILABLE', False)
    def test_rule_disabled_when_dragonfly_unavailable(self, capsys):
        """Test that rule is properly disabled when dragonfly accessibility is not available."""
        rule_class, details = get_rule()

        assert details.enabled is False
        captured = capsys.readouterr()
        assert "SelectAndSay rule disabled" in captured.out

    @patch('castervoice.rules.core.navigation_rules.select_and_say.DRAGONFLY_ACCESSIBILITY_AVAILABLE', True)
    def test_rule_enabled_when_dragonfly_available(self):
        """Test that rule is enabled when dragonfly accessibility is available."""
        rule_class, details = get_rule()

        # Should not be explicitly disabled
        assert not hasattr(details, 'enabled') or details.enabled is not False