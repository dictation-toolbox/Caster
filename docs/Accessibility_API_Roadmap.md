# Accessibility API integration roadmap (Issue #814)

This document proposes an incremental path for integrating OS accessibility APIs into Caster, with focus on reliability and cross-platform abstraction.

## Goals

- Provide a small, engine-agnostic API that grammar rules can call.
- Keep platform-specific implementation details out of rule code.
- Start with read-only capabilities and controlled write actions.
- Preserve low latency for common text manipulation commands.

## Proposed architecture

### 1) Core interface (`castervoice/lib/accessibility/`)

Define a minimal interface (Python protocol/ABC) for operations Caster rules need:

- `get_focused_element()`
- `get_selected_text()`
- `replace_selected_text(text)`
- `move_caret(direction, unit, count)`
- `select_range(start, end)`
- `invoke_action(name)`

This layer is intentionally independent from Dragonfly/Natlink internals.

### 2) Platform adapters

Create separate adapters behind the same interface:

- **Windows**: UIA first, optional MSAA fallback.
- **Linux**: AT-SPI/IA2 where available.
- **macOS**: Accessibility API adapter.

Each adapter should expose feature flags so rules can gracefully degrade when a capability is unavailable.

### 3) Capability registry

At startup, detect available backend and publish capabilities (for example: supports range selection, supports role tree traversal, supports editable check).

Rules should branch on capabilities, not platform names.

## Implementation phases

### Phase A — read-only introspection

- Focused element metadata (role/name/editable state)
- Current selection text retrieval
- Basic diagnostics logger

### Phase B — safe text actions

- Replace selected text
- Caret move by character/word/line (where supported)
- Predictable error surface with explicit exceptions

### Phase C — richer navigation

- Paragraph/sentence movement
- Find next/previous control by role
- Action invocation (press/default)

## Performance & reliability notes

- Cache focused element identity only for short intervals.
- Invalidate cache on focus change events.
- Prefer explicit timeouts for accessibility calls.
- Normalize backend errors to common exception classes.

## Testing plan

- Unit tests for interface contract and error normalization.
- Backend smoke tests on CI where possible.
- Manual matrix for major targets:
  - VS Code
  - Browser text areas/contenteditable
  - Native editors (Notepad/TextEdit/Gedit equivalent)

## Relationship to `dtactions`

If maintained by the Dictation Toolbox ecosystem, this abstraction can be extracted later into `dtactions` once the interface stabilizes. Starting in Caster allows faster iteration with real grammar usage.

## Scope boundaries

This roadmap does **not** attempt to replicate all Dragon Select-and-Say behavior in one step. It focuses on a narrow, testable API that enables progressive improvements without breaking existing command paths.
