_API = None


def _load_api():
    global _API
    if _API is False:
        return None
    if _API is None:
        try:
            from dragonfly.accessibility import CursorPosition
            from dragonfly.accessibility import TextQuery
            from dragonfly.accessibility import get_accessibility_controller
            from dragonfly.accessibility import utils
            _API = (CursorPosition, TextQuery, get_accessibility_controller, utils)
        except Exception:
            _API = False
    return _API or None


def _get_controller():
    api = _load_api()
    if not api:
        return None
    try:
        controller = api[2]()
        if controller is None or not controller.is_editable_focused():
            return None
        return controller
    except Exception:
        return None


def _get_text_info(controller, query):
    return _load_api()[3].get_text_info(controller.os_controller, query)


def _get_cursor_offset(controller):
    return _load_api()[3].get_cursor_offset(controller.os_controller)


def _matches_direction(direction, cursor_offset, text_info):
    if cursor_offset is None or text_info is None:
        return False
    if direction == "left":
        return text_info.end <= cursor_offset
    if direction == "right":
        return text_info.start >= cursor_offset
    return False


def _phrase_query(phrase):
    return _load_api()[1](end_phrase=phrase)


def _range_query(direction, before_after, phrase):
    if (direction == "left" and before_after == "before") or (direction == "right" and before_after == "after"):
        return _load_api()[1](through=True, end_phrase=phrase)
    position = _load_api()[0].AFTER if direction == "left" else _load_api()[0].BEFORE
    return _load_api()[1](through=True, end_relative_position=position, end_relative_phrase=phrase)


def _replace_query(controller, direction, query, replacement):
    text_info = _get_text_info(controller, query)
    if not _matches_direction(direction, _get_cursor_offset(controller), text_info):
        return False
    if replacement == "" and text_info.start == text_info.end:
        return False
    try:
        controller.replace_text(query, replacement)
    except Exception:
        return False
    return True


def _select_query(controller, direction, query):
    text_info = _get_text_info(controller, query)
    if not _matches_direction(direction, _get_cursor_offset(controller), text_info):
        return False
    try:
        return controller.select_text(query)
    except Exception:
        return False


def replace_nearest_phrase(direction, phrase, replacement):
    controller = _get_controller()
    if not controller:
        return False
    return _replace_query(controller, direction, _phrase_query(phrase), replacement)


def remove_nearest_phrase(direction, phrase, remove_space=False):
    controller = _get_controller()
    if not controller:
        return False
    phrases = [" " + phrase, phrase] if remove_space else [phrase]
    for candidate in phrases:
        if _replace_query(controller, direction, _phrase_query(candidate), ""):
            return True
    return False


def move_nearest_phrase(direction, before_after, phrase):
    controller = _get_controller()
    if not controller:
        return False
    query = _phrase_query(phrase)
    text_info = _get_text_info(controller, query)
    if not _matches_direction(direction, _get_cursor_offset(controller), text_info):
        return False
    position = _load_api()[0].BEFORE if before_after == "before" else _load_api()[0].AFTER
    try:
        return controller.move_cursor(query, position)
    except Exception:
        return False


def select_nearest_phrase(direction, phrase):
    controller = _get_controller()
    if not controller:
        return False
    return _select_query(controller, direction, _phrase_query(phrase))


def select_until_nearest_phrase(direction, before_after, phrase):
    controller = _get_controller()
    if not controller:
        return False
    return _select_query(controller, direction, _range_query(direction, before_after, phrase))


def remove_until_nearest_phrase(direction, before_after, phrase):
    controller = _get_controller()
    if not controller:
        return False
    return _replace_query(controller, direction, _range_query(direction, before_after, phrase), "")
