# Accessibility API Integration Plan

This document defines a practical path for issue [#814](https://github.com/dictation-toolbox/Caster/issues/814): integrating OS accessibility APIs to improve Select-and-Say style text navigation and editing.

## Goals

- Keep grammar-facing actions engine-agnostic and OS-agnostic.
- Add a thin adapter contract so platform-specific backends can be swapped.
- Start with read-only navigation and selection primitives, then add write/edit primitives.

## Adapter Contract (v1)

Grammar code should target a small interface, not platform APIs directly.

```python
class AccessibilityAdapter:
    def get_focused_element(self): ...
    def get_text_context(self): ...
    def get_caret_range(self): ...
    def select_range(self, start: int, end: int): ...
    def move_caret(self, offset: int): ...
```

## Suggested Backend Order

1. Windows UI Automation (UIA) first.
2. Optional MSAA bridge for legacy apps.
3. Linux AT-SPI and macOS AX adapters after contract stabilizes.

## Milestones

1. Discovery and tool validation.
2. Spike implementation for focused element and caret inspection.
3. First grammar integration for text selection/navigation commands.
4. Cross-platform adapter stubs and fallback behavior docs.

## Discovery Checklist

- Verify focused element access for: VS Code, browser textareas, terminal, and common editors.
- Measure latency for caret reads and selection operations.
- Document unsupported app classes and fallback command behavior.
- Capture reproducible traces for edge cases (virtualized controls, shadow DOM/electron widgets).

## Deliverables

- Adapter contract module and backend selector.
- Integration notes for pywinauto/UIA tooling.
- Test matrix for supported apps and known limitations.
- User-facing docs that explain capability by OS and app type.

## Out of Scope (v1)

- Full parity across all OSes in one release.
- Automatic recovery for every custom widget implementation.

