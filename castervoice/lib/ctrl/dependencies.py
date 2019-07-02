'''
Created on Oct 7, 2015

@author: synkarius
'''
from castervoice.lib import settings
import time


def version_minimum():
    try:
        import pkg_resources
        version = "0.13.0"  # Minimum Version of Dragonfly2 need for Caster
        pkg_resources.require("dragonfly2 >= %s" % (version))
    except Exception:  # pylint: disable=broad-except
        pass
        print("\nCaster: Requires at least Dragonfly version %s" \
            "\n Update Dragonfly 'pip install --upgrade dragonfly2' from cmd.\n" % (version))
        time.sleep(15)


version_minimum()


class DependencyMan:
    def __init__(self):
        with open('D:\\Backup\\Library\\Documents\\Caster\\requirements.txt') as f:
            requirements = f.read().splitlines()
        self.list = requirements
        warnings = 0
        for dep in self.list:
            is_optional = dep[0] == "win32ui"
            try:
                exec ("import " + dep[0])
            except ImportError:
                if not dep[0] in settings.SETTINGS["one time warnings"]:
                    warnings += 1
                    settings.SETTINGS["one time warnings"][dep[0]] = True

                    urgency = "You can get it at " if is_optional else "If you wish to use those features, you can get it at "
                    print("\n" + dep[0] + " is required for ", dep[2],
                          " features. " + urgency + dep[3] + "\n")
            else:
                name = dep[0] if not is_optional else dep[1]
                exec ("self." + name.upper() + "=True")
        if warnings > 0:
            settings.save_config()

    NATLINK = False
    PIL = False
    PYWIN32 = False
    WX = False
