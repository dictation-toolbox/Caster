# SETTINGS["auto_com"] = {}
#         SETTINGS["auto_com"]["active"] = True
#         SETTINGS["auto_com"]["interval"] = 1
#         SETTINGS["auto_com"]["run_internal"] = False
#         SETTINGS["auto_com"]["ASCII"] = 126
#         SETTINGS["auto_com"]["executables"] = ["eclipse", "WDExpress", "notepad++"]
from lib import settings, utilities, control

if control.DEP.NATLINK:
    import natlink

if settings.SETTINGS["auto_com"]["active"]:
    if control.DEP.NATLINK:
        if settings.SETTINGS["auto_com"]["run_internal"]:
            ''''''
        else:
            import hooks
            hooks.initialize_auto_com_external()
    else:
        utilities.report("Auto-Command-Mode feature not available with WSR")