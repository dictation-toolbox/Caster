# monkey patch for Daanzu's 64-bit executable fix; will monkeypatch until this is part of Dragonfly
import win32gui
import win32con
from ctypes          import windll, pointer, c_wchar, c_ulong
# from .rectangle      import Rectangle, unit
# from .monitor        import monitors
# from .window_movers  import window_movers

def _get_window_module(self):
    # Get this window's process ID.
    pid = c_ulong()
    windll.user32.GetWindowThreadProcessId(self._handle, pointer(pid))

    # Get the process handle of this window's process ID.
    #  Access permission flags:
    #  0x0410 = PROCESS_QUERY_INFORMATION | PROCESS_VM_READ
    handle = windll.kernel32.OpenProcess(0x0410, 0, pid)

    # Retrieve and return the process's executable path.
    buf_len = c_ulong(256)
    buf = (c_wchar * buf_len.value)()
    try:
        # QueryFullProcessImageNameW requires Vista or above, but works for all bitness
        windll.kernel32.QueryFullProcessImageNameW(handle, 0, pointer(buf), pointer(buf_len))
    except Exception, e:
        # GetModuleFileNameExW works in XP, but fails with 32-bit python querying 64-bit processes in Windows 8
        windll.psapi.GetModuleFileNameExW(handle, 0, pointer(buf), buf_len)
        return ""
    finally:
        # Don't leak handle
        windll.kernel32.CloseHandle(handle)
    buf = buf[:]
    buf = buf[:buf.index("\0")]
    return str(buf)

from dragonfly import Window
Window._get_window_module = _get_window_module
Window.executable = property(fget=_get_window_module)

import win32con
from dragonfly         import ActionBase, ActionError

def _execute(self, data=None):
    executable = self.executable
    title = self.title
    if data and isinstance(data, dict):
        if executable:  executable = (executable % data).lower()
        if title:       title = (title % data).lower()

    windows = Window.get_all_windows()
    for window in windows:
        if not window.is_visible:
            continue
        if (window.executable.endswith("natspeak.exe")
            and window.classname == "#32770"
            and window.get_position().dy < 50):
            # If a window matches the above, it is very probably
            #  the results-box of DNS.  We ignore this because
            #  its title is the words of the last recognition,
            #  which will often interfere with a search for
            #  a window with a spoken title.
            continue

        if executable:
            if window.executable.lower().find(executable) == -1:
                continue
        if title:
            if window.title.lower().find(title) == -1:
                continue
        try:
            window.set_foreground()
            return
        except Exception:
            pass
    raise ActionError("Failed to find window (%s)."  % self._str)

from dragonfly import FocusWindow
FocusWindow._execute = _execute