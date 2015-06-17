from caster.lib import settings, utilities, control
 
if settings.SETTINGS["auto_com"]["active"]:
    if control.nexus().dep.NATLINK:
        from caster.asynch.auto_com import toggler
        toggler.initialize_auto_com_internal()
    else:
        utilities.availability_message("Auto-Command-Mode", "natlink")