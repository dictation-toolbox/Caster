from dragonfly import Window, Key
from ctypes import windll

# https://github.com/mirober/pyvda
try:
    from pyvda import VirtualDesktop, AppView, get_virtual_desktops  # pylint: disable=import-error
except Exception as e:
    # This could fail on linux or windows <10
    print("Importing package pyvda failed with exception %s" % str(e))

ASFW_ANY = -1

def go_to_desktop_number(n):
    # Helps make sure that the target desktop gets focus
    windll.user32.AllowSetForegroundWindow(ASFW_ANY)
    VirtualDesktop(n).go()

def move_current_window_to_desktop(n=1, follow=False):
    hwnd = Window.get_foreground().handle
    AppView(hwnd).move(VirtualDesktop(n))
    if follow:
        go_to_desktop_number(n)

def close_all_workspaces():
    desktops = get_virtual_desktops()
    total = len(desktops)
    if total <= 1:
        print("Only one desktop exists; nothing to close.")
        return
    go_to_desktop_number(total - 1)
    Key("wc-f4/10:" + str(total - 1)).execute()
