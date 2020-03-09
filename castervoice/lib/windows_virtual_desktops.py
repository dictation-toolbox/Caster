from dragonfly import Window, Key
from ctypes import windll
# https://github.com/mrob95/py-VirtualDesktopAccessor
try:
    import pyvda  # pylint: disable=import-error
except Exception as e:
    # This could fail on linux or windows <10
    print("Importing package pyvda failed with exception %s" % str(e))

ASFW_ANY = -1


def go_to_desktop_number(n):
    # Helps make sure that the target desktop gets focus
    windll.user32.AllowSetForegroundWindow(ASFW_ANY)
    pyvda.GoToDesktopNumber(n)


def move_current_window_to_desktop(n=1, follow=False):
    window_handle = Window.get_foreground().handle
    pyvda.MoveWindowToDesktopNumber(window_handle, n)
    if follow:
        go_to_desktop_number(n)


def close_all_workspaces():
    total = pyvda.GetDesktopCount()
    go_to_desktop_number(total)
    Key("wc-f4/10:" + str(total-1)).execute()
