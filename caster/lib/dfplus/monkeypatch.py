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
