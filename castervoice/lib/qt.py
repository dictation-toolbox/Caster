# pylint: disable=import-error,no-name-in-module

"""
Minimal PySide2/PySide6 compatibility helpers.
"""


try:
    from PySide2 import QtCore, QtGui, QtWidgets  # type: ignore
    QT_API = "PySide2"
except ImportError:  # pragma: no cover
    from PySide6 import QtCore, QtGui, QtWidgets  # type: ignore
    QT_API = "PySide6"


def qt_attr(root, *paths):
    """
    Return the first attribute path that exists on `root`.

    `paths` should be tuples of attribute names, e.g. ("Qt", "Key", "Key_Tab").
    """
    last_error = None
    for path in paths:
        try:
            obj = root
            for name in path:
                obj = getattr(obj, name)
            return obj
        except AttributeError as exc:
            last_error = exc
    if last_error is None:
        raise AttributeError("qt_attr() requires at least one path")
    raise last_error


def qapp_exec(app):
    exec_fn = getattr(app, "exec", None) or getattr(app, "exec_", None)
    if exec_fn is None:
        raise AttributeError("QApplication has no exec/exec_ method")
    return exec_fn()

