"""UI Automation (UIA) backend for dragonfly accessibility.

This module provides a Windows UI Automation implementation that follows
dragonfly's accessibility backend interface exactly, matching the patterns
established by the IA2 backend.
"""

import logging
import threading
import time
import traceback

import queue

from dragonfly.accessibility import base

try:
    import comtypes
    import comtypes.client
    from comtypes.gen import UIAutomationClient as UIA
    UIA_AVAILABLE = True
except ImportError:
    UIA_AVAILABLE = False
    # Create dummy UIA for type checking
    class _DummyUIA:
        UIA_TextPatternId = 0
        UIA_ValuePatternId = 0
        UIA_EditControlTypeId = 0
        UIA_DocumentControlTypeId = 0
        TextPatternRangeEndpoint_Start = 0
        TextPatternRangeEndpoint_End = 0
        TextUnit_Character = 0
        IUIAutomation = None
        IUIAutomationTextPattern = None
        IUIAutomationValuePattern = None
    UIA = _DummyUIA()


class Controller(object):
    """UI Automation controller following dragonfly's accessibility interface."""

    _log = logging.getLogger("accessibility")

    class Capture(object):
        def __init__(self, closure):
            self.closure = closure
            self.done_event = threading.Event()
            self.exception = None
            self.return_value = None

    def __init__(self):
        if not UIA_AVAILABLE:
            raise ImportError("comtypes required for UIA backend")

        self._context = Context()
        self._closure_queue = queue.Queue(1)
        self.shutdown_event = None

    def start(self):
        """Start the UIA background thread."""
        self.shutdown_event = threading.Event()
        thread = threading.Thread(target=self._start_blocking)
        thread.setDaemon(True)
        thread.start()

    def stop(self):
        """Stop the UIA background thread."""
        if self.shutdown_event:
            self.shutdown_event.set()

    def run_sync(self, closure):
        """Execute closure in UIA thread."""
        capture = self.Capture(closure)
        self._closure_queue.put(capture)
        capture.done_event.wait()
        if capture.exception is not None:
            raise capture.exception
        return capture.return_value

    def _start_blocking(self):
        """Main UIA thread loop matching IA2 pattern."""
        # Import here to run in same thread as COM operations
        import comtypes
        import comtypes.client

        comtypes.CoInitialize()
        try:
            self._context.initialize()

            while not (self.shutdown_event and self.shutdown_event.is_set()):
                try:
                    # Update focused element periodically
                    self._context.update_focus()

                    # Process queued closures
                    while True:
                        try:
                            capture = self._closure_queue.get_nowait()
                        except queue.Empty:
                            break

                        try:
                            capture.return_value = capture.closure(self._context)
                        except base.AccessibilityError as exception:
                            capture.exception = exception
                            # Checked exception, don't print
                        except Exception as exception:
                            capture.exception = exception
                            # Print stack trace for unexpected errors
                            traceback.print_exc()
                        capture.done_event.set()

                    # Small delay to prevent busy waiting
                    time.sleep(0.01)

                except Exception:
                    traceback.print_exc()

        finally:
            comtypes.CoUninitialize()


class Context(object):
    """UIA context managing focused element."""

    _log = logging.getLogger("accessibility.uia")

    def __init__(self):
        self.automation = None
        self.focused = None

    def initialize(self):
        """Initialize UI Automation client."""
        try:
            import comtypes.client
            self.automation = comtypes.client.CreateObject(
                "{ff48dba4-60ef-4201-aa87-54103eef594e}",
                interface=UIA.IUIAutomation
            )
            self._log.debug("UIA client initialized")
        except Exception as e:
            self._log.error("Failed to initialize UIA: %s", e)
            raise

    def update_focus(self):
        """Update the focused element."""
        if not self.automation:
            return

        try:
            focused_element = self.automation.GetFocusedElement()
            if focused_element:
                self.focused = UiaAccessible(focused_element)
            else:
                self.focused = None
        except Exception as e:
            self._log.debug("Failed to get focused element: %s", e)
            self.focused = None


class UiaAccessible(object):
    """Wrapper for UIA element, matching dragonfly's Accessible interface."""

    def __init__(self, element):
        self._element = element

    def as_text(self):
        """Get text interface if element supports TextPattern."""
        try:
            pattern_obj = self._element.GetCurrentPattern(UIA.UIA_TextPatternId)
            if pattern_obj:
                text_pattern = pattern_obj.QueryInterface(UIA.IUIAutomationTextPattern)
                return UiaAccessibleTextNode(self._element, text_pattern)
        except Exception:
            pass
        return None

    def is_editable(self):
        """Check if element is editable."""
        try:
            # Check for editable state
            value_pattern = self._element.GetCurrentPattern(UIA.UIA_ValuePatternId)
            if value_pattern:
                value_pattern_obj = value_pattern.QueryInterface(UIA.IUIAutomationValuePattern)
                return not value_pattern_obj.CurrentIsReadOnly

            # Also check control type for text boxes
            control_type = self._element.CurrentControlType
            return control_type in [UIA.UIA_EditControlTypeId, UIA.UIA_DocumentControlTypeId]
        except Exception:
            return False


class UiaAccessibleTextNode(object):
    """UIA text node matching dragonfly's AccessibleTextNode interface."""

    _log = logging.getLogger("accessibility.uia.textnode")

    def __init__(self, element, text_pattern):
        self._element = element
        self._text_pattern = text_pattern
        self._expanded_text = None
        self._cursor_offset = None

        # Initialize text and cursor
        self._update_text_info()

    def _update_text_info(self):
        """Update cached text and cursor information."""
        try:
            # Get all text from document range
            doc_range = self._text_pattern.DocumentRange
            if doc_range:
                self._expanded_text = doc_range.GetText(-1)  # -1 = all text
            else:
                self._expanded_text = ""

            # Get cursor position
            try:
                selection = self._text_pattern.GetSelection()
                if selection and selection.Length > 0:
                    first_selection = selection.GetElement(0)
                    doc_range = self._text_pattern.DocumentRange
                    if doc_range:
                        self._cursor_offset = abs(doc_range.CompareEndpoints(
                            UIA.TextPatternRangeEndpoint_Start,
                            first_selection,
                            UIA.TextPatternRangeEndpoint_Start
                        ))
                    else:
                        self._cursor_offset = 0
                else:
                    self._cursor_offset = 0
            except Exception:
                self._cursor_offset = 0

        except Exception as e:
            self._log.debug("Failed to update text info: %s", e)
            self._expanded_text = ""
            self._cursor_offset = 0

    @property
    def expanded_text(self):
        """Get expanded text content."""
        if self._expanded_text is None:
            self._update_text_info()
        return self._expanded_text or ""

    @property
    def cursor(self):
        """Get cursor offset."""
        if self._cursor_offset is None:
            self._update_text_info()
        return self._cursor_offset or 0

    def select_range(self, start_offset, end_offset):
        """Select text range by character offsets."""
        try:
            doc_range = self._text_pattern.DocumentRange
            if not doc_range:
                return

            # Create text range for selection
            text_range = doc_range.Clone()

            # Move start position
            text_range.MoveEndpointByUnit(
                UIA.TextPatternRangeEndpoint_Start,
                UIA.TextUnit_Character,
                start_offset
            )

            # Move end position
            current_end = len(self.expanded_text)
            move_end = end_offset - current_end
            text_range.MoveEndpointByUnit(
                UIA.TextPatternRangeEndpoint_End,
                UIA.TextUnit_Character,
                move_end
            )

            # Select the range
            text_range.Select()
            self._log.debug("Selected range %d-%d", start_offset, end_offset)

        except Exception as e:
            self._log.error("Failed to select range: %s", e)
            raise base.UnsupportedSelectionError("Text selection not supported")

    def set_cursor(self, offset):
        """Set cursor position."""
        try:
            doc_range = self._text_pattern.DocumentRange
            if not doc_range:
                return

            # Create collapsed range at offset
            cursor_range = doc_range.Clone()

            # Move to position
            cursor_range.MoveEndpointByUnit(
                UIA.TextPatternRangeEndpoint_Start,
                UIA.TextUnit_Character,
                offset
            )

            # Collapse to start
            cursor_range.MoveEndpointByUnit(
                UIA.TextPatternRangeEndpoint_End,
                UIA.TextUnit_Character,
                offset - len(self.expanded_text)
            )

            # Set cursor
            cursor_range.Select()
            self._cursor_offset = offset
            self._log.debug("Set cursor to %d", offset)

        except Exception as e:
            self._log.error("Failed to set cursor: %s", e)

    def get_bounding_box(self, offset):
        """Get bounding box for character at offset."""
        try:
            doc_range = self._text_pattern.DocumentRange
            if not doc_range:
                return BoundingBox(0, 0, 0, 0)

            # Create single-character range at offset
            char_range = doc_range.Clone()

            # Move to position
            char_range.MoveEndpointByUnit(
                UIA.TextPatternRangeEndpoint_Start,
                UIA.TextUnit_Character,
                offset
            )

            # Set end to one character after start
            char_range.MoveEndpointByUnit(
                UIA.TextPatternRangeEndpoint_End,
                UIA.TextUnit_Character,
                offset + 1 - len(self.expanded_text)
            )

            # Get bounding rectangles
            rects = char_range.GetBoundingRectangles()
            if rects and len(rects) >= 4:
                # Return first rectangle
                return BoundingBox(rects[0], rects[1], rects[2], rects[3])

        except Exception as e:
            self._log.debug("Failed to get bounding box: %s", e)

        # Return default box
        return BoundingBox(0, 0, 1, 1)


class BoundingBox(object):
    """Bounding box matching dragonfly's interface."""

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __str__(self):
        return "x=%s, y=%s, width=%s, height=%s" % (self.x, self.y, self.width, self.height)