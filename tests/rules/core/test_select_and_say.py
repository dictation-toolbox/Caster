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
            "go to <position> of <text>"
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
    """Test Select-and-Say command functions with mocked adapter."""

    @patch('castervoice.rules.core.navigation_rules.select_and_say.get_adapter')
    def test_select_text_command_success(self, mock_get_adapter):
        """Test successful text selection."""
        mock_adapter = Mock()
        mock_adapter.is_editable_focused.return_value = True
        mock_get_adapter.return_value = mock_adapter

        # Test single text selection
        select_text_command("hello")

        mock_adapter.is_editable_focused.assert_called_once()
        mock_adapter.select_text.assert_called_once()

        # Verify TextQuery was created correctly
        call_args = mock_adapter.select_text.call_args[0]
        query = call_args[0]
        assert query.start == "hello"
        assert query.end is None

    @patch('castervoice.rules.core.navigation_rules.select_and_say.get_adapter')
    def test_select_text_range_command(self, mock_get_adapter):
        """Test range text selection."""
        mock_adapter = Mock()
        mock_adapter.is_editable_focused.return_value = True
        mock_get_adapter.return_value = mock_adapter

        # Test range selection
        select_text_command("start", "end")

        # Verify TextQuery was created for range selection
        call_args = mock_adapter.select_text.call_args[0]
        query = call_args[0]
        assert query.start == "start"
        assert query.end == "end"
        assert query.through is True

    @patch('castervoice.rules.core.navigation_rules.select_and_say.get_adapter')
    def test_select_text_no_control_focused(self, mock_get_adapter, capsys):
        """Test behavior when no editable control is focused."""
        mock_adapter = Mock()
        mock_adapter.is_editable_focused.return_value = False
        mock_get_adapter.return_value = mock_adapter

        select_text_command("hello")

        # Should not attempt selection
        mock_adapter.select_text.assert_not_called()

        # Should print informative message
        captured = capsys.readouterr()
        assert "No editable control is focused" in captured.out

    @patch('castervoice.rules.core.navigation_rules.select_and_say.get_adapter')
    def test_replace_text_command_success(self, mock_get_adapter):
        """Test successful text replacement."""
        mock_adapter = Mock()
        mock_adapter.is_editable_focused.return_value = True
        mock_get_adapter.return_value = mock_adapter

        replace_text_command("old", "new")

        mock_adapter.replace_text.assert_called_once()

        # Verify parameters
        call_args = mock_adapter.replace_text.call_args[0]
        query = call_args[0]
        replacement = call_args[1]
        assert query.start == "old"
        assert replacement == "new"

    @patch('castervoice.rules.core.navigation_rules.select_and_say.get_adapter')
    def test_move_cursor_command_success(self, mock_get_adapter):
        """Test successful cursor movement."""
        mock_adapter = Mock()
        mock_adapter.is_editable_focused.return_value = True
        mock_get_adapter.return_value = mock_adapter

        move_cursor_command("target", "start")

        mock_adapter.move_cursor.assert_called_once()

        # Verify parameters
        call_args = mock_adapter.move_cursor.call_args[0]
        query = call_args[0]
        position = call_args[1]
        assert query.start == "target"
        # Position should be mapped to enum value
        from dtactions.a11y import CursorPosition
        assert position == CursorPosition.START

    @patch('castervoice.rules.core.navigation_rules.select_and_say._safe_get_adapter')
    def test_adapter_not_available(self, mock_safe_get_adapter, capsys):
        """Test behavior when dtactions adapter is not available."""
        mock_safe_get_adapter.return_value = None

        select_text_command("hello")

        # Should not crash, just return early
        captured = capsys.readouterr()
        # May have printed a message, but should not crash

    @patch('castervoice.rules.core.navigation_rules.select_and_say.get_adapter')
    def test_error_handling(self, mock_get_adapter, capsys):
        """Test error handling for various exception types."""
        from dtactions.a11y.exceptions import NotFoundError, UnsupportedControlError

        mock_adapter = Mock()
        mock_adapter.is_editable_focused.return_value = True
        mock_get_adapter.return_value = mock_adapter

        # Test NotFoundError handling
        mock_adapter.select_text.side_effect = NotFoundError("Text not found")
        select_text_command("missing")

        captured = capsys.readouterr()
        assert "Could not find text" in captured.out

        # Test UnsupportedControlError handling
        mock_adapter.select_text.side_effect = UnsupportedControlError("Control not supported")
        select_text_command("hello")

        captured = capsys.readouterr()
        assert "does not support" in captured.out


class TestSelectAndSayIntegration:
    """Test integration aspects of Select-and-Say grammar."""

    @patch('castervoice.rules.core.navigation_rules.select_and_say.DTACTIONS_AVAILABLE', False)
    def test_rule_disabled_when_dtactions_unavailable(self, capsys):
        """Test that rule is properly disabled when dtactions is not available."""
        rule_class, details = get_rule()

        assert details.enabled is False
        captured = capsys.readouterr()
        assert "SelectAndSay rule disabled" in captured.out

    @patch('castervoice.rules.core.navigation_rules.select_and_say.DTACTIONS_AVAILABLE', True)
    def test_rule_enabled_when_dtactions_available(self):
        """Test that rule is enabled when dtactions is available."""
        rule_class, details = get_rule()

        # Should not be explicitly disabled
        assert not hasattr(details, 'enabled') or details.enabled is not False