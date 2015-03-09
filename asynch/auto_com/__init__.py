from lib import settings, utilities, control

if settings.SETTINGS["auto_com"]["active"]:
    if control.DEP.NATLINK:
        from asynch.auto_com import toggler
        if settings.SETTINGS["auto_com"]["run_internal"]:
            toggler.initialize_auto_com_internal()
        else:
            toggler.initialize_auto_com_external()
    else:
        utilities.report("Auto-Command-Mode feature not available with WSR")