import sys

if sys.platform == "win32":
    from .windows_virtual_desktops import go_to_desktop_number
    from .windows_virtual_desktops import move_current_window_to_desktop
    from .windows_virtual_desktops import close_all_workspaces
else:
    def go_to_desktop_number(n):
        print("Virtual desktop commands are not implemented on this platform")

    def move_current_window_to_desktop(n=1, follow=False):
        print("Virtual desktop commands are not implemented on this platform")

    def close_all_workspaces():
        print("Virtual desktop commands are not implemented on this platform")
