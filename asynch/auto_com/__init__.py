from lib import settings, utilities, control

if settings.SETTINGS["auto_com"]["active"]:
    if control.DEP.NATLINK:
        from asynch.auto_com import toggler
        if settings.SETTINGS["auto_com"]["run_internal"]:
            toggler.initialize_auto_com_internal()
        else:
            if control.DEP.PYHOOK:
                toggler.initialize_auto_com_external()
            else:
                utilities.availability_message("Auto-Command-Mode (external mode)", "pyHook")
    else:
        utilities.availability_message("Auto-Command-Mode", "natlink")