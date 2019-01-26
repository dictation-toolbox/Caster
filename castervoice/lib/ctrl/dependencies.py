'''
Created on Oct 7, 2015

@author: synkarius
'''
from castervoice.lib import settings


class DependencyMan:
    def __init__(self):

        self.list = [
            ("PIL", None, ["Legion"], "https://pypi.python.org/pypi/Pillow"),
            #("wx", None, ["Settings Window"], "http://www.wxpython.org"),
            ("win32ui", "pywin32", ["very many essential"],
             "http://sourceforge.net/projects/pywin32")
        ]
        warnings = 0
        for dep in self.list:
            is_win32ui = dep[0] == "win32ui"
            try:
                exec ("import " + dep[0])
            except ImportError:
                if not dep[0] in settings.SETTINGS["one time warnings"]:
                    warnings += 1
                    settings.SETTINGS["one time warnings"][dep[0]] = True
                    urgency = "You can get it at " if is_win32ui else "If you wish to use those features, you can get it at "
                    print("\n" + dep[0] + " is required for ", dep[2],
                          " features. " + urgency + dep[3] + "\n")
            else:
                name = dep[0] if not is_win32ui else dep[1]
                exec ("self." + name.upper() + "=True")
        if warnings > 0:
            settings.save_config()

    NATLINK = False
    PIL = False
    PYWIN32 = False
    WX = False
