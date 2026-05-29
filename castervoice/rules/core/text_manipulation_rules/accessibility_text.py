import re

from castervoice.lib.actions import Key, Text

try:
    from dragonfly.accessibility import get_accessibility_controller as dragonfly_get_accessibility_controller
except Exception:
    try:
        from dragonfly import get_accessibility_controller as dragonfly_get_accessibility_controller
    except Exception:
        dragonfly_get_accessibility_controller = None


TEXT_NODE_DELIMITER = u"\u00a6"


def _previous_boundary(text, index):
    position = max(0, min(index, len(text))) - 1
    while position >= 0:
        character = text[position]
        if character == "\n":
            if position > 0 and text[position - 1] == "\r":
                return (position - 1, position + 1)
            return (position, position + 1)
        if character == "\r":
            if position + 1 < len(text) and text[position + 1] == "\n":
                return (position, position + 2)
            return (position, position + 1)
        if character == TEXT_NODE_DELIMITER:
            return (position, position + 1)
        position -= 1
    return None


def _next_boundary(text, index):
    position = max(0, min(index, len(text)))
    while position < len(text):
        character = text[position]
        if character == "\r":
            if position + 1 < len(text) and text[position + 1] == "\n":
                return (position, position + 2)
            return (position, position + 1)
        if character == "\n" or character == TEXT_NODE_DELIMITER:
            return (position, position + 1)
        position += 1
    return None


def _window_start(text, cursor, number_of_lines_to_search):
    start = cursor
    lines_to_include = max(0, number_of_lines_to_search) + 1
    for _ in range(lines_to_include):
        boundary = _previous_boundary(text, start)
        if boundary is None:
            return 0
        start = boundary[0]
    return boundary[1]


def _window_end(text, cursor, number_of_lines_to_search):
    end = cursor
    lines_to_include = max(0, number_of_lines_to_search) + 1
    for _ in range(lines_to_include):
        boundary = _next_boundary(text, end)
        if boundary is None:
            return len(text)
        end = boundary[1]
    return boundary[0]


def _phrase_pattern(phrase, dictation_versus_character):
    if dictation_versus_character == "character":
        return re.escape(phrase)
    if dictation_versus_character == "dictation":
        # Keep the same word-boundary behavior as text_manipulation_support.
        return r"(?:[^A-Za-z]|\A)({})(?:[^A-Za-z]|\Z)".format(phrase.lower())
    raise ValueError("dictation_versus_character must be 'character' or 'dictation'")


def get_start_end_position(text, phrase, direction, occurrence_number, dictation_versus_character):
    pattern = _phrase_pattern(phrase, dictation_versus_character)
    lowered_text = text.lower()
    matches = re.finditer(pattern, lowered_text)
    if dictation_versus_character == "character":
        ranges = [(match.start(), match.end()) for match in matches]
    else:
        ranges = [(match.start(1), match.end(1)) for match in matches]

    if not ranges:
        return None

    try:
        if direction == "left":
            return ranges[-1 * occurrence_number]
        if direction == "right":
            return ranges[occurrence_number - 1]
    except IndexError:
        return None

    return None


def _get_controller():
    if dragonfly_get_accessibility_controller is None:
        return None
    try:
        return dragonfly_get_accessibility_controller()
    except Exception:
        return None


def _get_focused_text(accessibility_context):
    focused = getattr(accessibility_context, "focused", None)
    if not focused:
        return None
    try:
        if hasattr(focused, "is_editable") and not focused.is_editable():
            return None
        focused_text = focused.as_text()
    except Exception:
        return None

    if not focused_text:
        return None
    if getattr(focused_text, "cursor", None) is None:
        return None
    if getattr(focused_text, "expanded_text", None) is None:
        return None
    return focused_text


def _snapshot(controller):
    if not controller or not getattr(controller, "os_controller", None):
        return None

    def capture(accessibility_context):
        focused_text = _get_focused_text(accessibility_context)
        if not focused_text:
            return None
        text = focused_text.expanded_text
        cursor = max(0, min(focused_text.cursor, len(text)))
        return {"text": text, "cursor": cursor}

    try:
        return controller.os_controller.run_sync(capture)
    except Exception:
        return None


def _controller_and_snapshot():
    controller = _get_controller()
    snapshot = _snapshot(controller)
    if not snapshot:
        return (None, None)
    return (controller, snapshot)


def _search_window(snapshot, direction, number_of_lines_to_search):
    text = snapshot["text"]
    cursor = snapshot["cursor"]
    if direction == "left":
        start = _window_start(text, cursor, number_of_lines_to_search)
        return (text[start:cursor], start)
    if direction == "right":
        end = _window_end(text, cursor, number_of_lines_to_search)
        return (text[cursor:end], cursor)
    return (None, None)


def _target_range(snapshot, phrase, direction, number_of_lines_to_search,
                  occurrence_number, dictation_versus_character):
    window_text, base_offset = _search_window(snapshot, direction, number_of_lines_to_search)
    if window_text is None:
        return None

    match = get_start_end_position(window_text, phrase, direction, occurrence_number,
                                   dictation_versus_character)
    if not match:
        return None
    return (base_offset + match[0], base_offset + match[1])


def _until_range(snapshot, phrase, direction, before_after, number_of_lines_to_search,
                 occurrence_number, dictation_versus_character):
    target = _target_range(snapshot, phrase, direction, number_of_lines_to_search,
                           occurrence_number, dictation_versus_character)
    if not target:
        return None

    cursor = snapshot["cursor"]
    left_index, right_index = target
    if direction == "left":
        target_index = left_index if before_after == "before" else right_index
    elif direction == "right":
        target_index = right_index if before_after == "after" else left_index
    else:
        return None
    return (min(cursor, target_index), max(cursor, target_index))


def _select_range(controller, start, end):
    if start == end:
        return False

    def select(accessibility_context):
        focused_text = _get_focused_text(accessibility_context)
        if not focused_text:
            return False
        focused_text.select_range(start, end)
        return True

    try:
        return bool(controller.os_controller.run_sync(select))
    except Exception:
        return False


def _set_cursor(controller, offset):
    def move(accessibility_context):
        focused_text = _get_focused_text(accessibility_context)
        if not focused_text:
            return False
        focused_text.set_cursor(offset)
        return True

    try:
        return bool(controller.os_controller.run_sync(move))
    except Exception:
        return False


def _replace_range(controller, start, end, replacement):
    if not _select_range(controller, start, end):
        return False
    try:
        if replacement:
            Text(str(replacement).replace("%", "%%")).execute()
        else:
            Key("backspace").execute()
    except Exception:
        # Once the accessibility selection has been made, do not fall back into
        # the clipboard path and risk acting on the already-selected range twice.
        return True
    return True


def select_phrase(phrase, direction, number_of_lines_to_search, occurrence_number,
                  dictation_versus_character):
    controller, snapshot = _controller_and_snapshot()
    if not controller:
        return False
    target = _target_range(snapshot, phrase, direction, number_of_lines_to_search,
                           occurrence_number, dictation_versus_character)
    if not target:
        return False
    return _select_range(controller, target[0], target[1])


def select_until_phrase(direction, phrase, before_after, number_of_lines_to_search,
                        occurrence_number, dictation_versus_character):
    controller, snapshot = _controller_and_snapshot()
    if not controller:
        return False
    target = _until_range(snapshot, phrase, direction, before_after, number_of_lines_to_search,
                          occurrence_number, dictation_versus_character)
    if not target:
        return False
    return _select_range(controller, target[0], target[1])


def move_until_phrase(direction, before_after, phrase, number_of_lines_to_search,
                      occurrence_number, dictation_versus_character):
    controller, snapshot = _controller_and_snapshot()
    if not controller:
        return False
    target = _target_range(snapshot, phrase, direction, number_of_lines_to_search,
                           occurrence_number, dictation_versus_character)
    if not target:
        return False
    return _set_cursor(controller, target[0] if before_after == "before" else target[1])


def replace_phrase_with_phrase(replaced_phrase, replacement_phrase, direction,
                               number_of_lines_to_search, occurrence_number,
                               dictation_versus_character):
    controller, snapshot = _controller_and_snapshot()
    if not controller:
        return False
    target = _target_range(snapshot, replaced_phrase, direction, number_of_lines_to_search,
                           occurrence_number, dictation_versus_character)
    if not target:
        return False
    return _replace_range(controller, target[0], target[1], replacement_phrase)


def remove_phrase_from_text(phrase, direction, number_of_lines_to_search, occurrence_number,
                            dictation_versus_character):
    controller, snapshot = _controller_and_snapshot()
    if not controller:
        return False
    target = _target_range(snapshot, phrase, direction, number_of_lines_to_search,
                           occurrence_number, dictation_versus_character)
    if not target:
        return False
    start, end = target
    if dictation_versus_character != "character" and start > 0 and snapshot["text"][start - 1] == " ":
        start -= 1
    return _replace_range(controller, start, end, "")


def delete_until_phrase(direction, phrase, before_after, number_of_lines_to_search,
                        occurrence_number, dictation_versus_character):
    controller, snapshot = _controller_and_snapshot()
    if not controller:
        return False
    target = _until_range(snapshot, phrase, direction, before_after, number_of_lines_to_search,
                          occurrence_number, dictation_versus_character)
    if not target:
        return False
    return _replace_range(controller, target[0], target[1], "")
