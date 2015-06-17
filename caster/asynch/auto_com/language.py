from caster.lib import utilities, settings, ccr, control


AUTO_ENABLED_LANGUAGE = None
LAST_EXTENSION = None

def toggle_language():
    global AUTO_ENABLED_LANGUAGE, LAST_EXTENSION
    filename, folders, title = utilities.get_window_title_info()
    extension = None
    if filename != None:
        extension = "." + filename.split(".")[-1]
    
    if LAST_EXTENSION != extension:
        message=None
        if extension != None and extension in settings.SETTINGS["ccr"]["registered_extensions"]:
            chosen_extension=settings.SETTINGS["ccr"]["registered_extensions"][extension]
            ccr.set_active_command(1, chosen_extension)
            AUTO_ENABLED_LANGUAGE = chosen_extension
            LAST_EXTENSION = extension
            message="Enabled '"+chosen_extension+"'"
        elif AUTO_ENABLED_LANGUAGE != None:
            message="Disabled '"+AUTO_ENABLED_LANGUAGE+"'"
            ccr.set_active_command(0, AUTO_ENABLED_LANGUAGE)
            AUTO_ENABLED_LANGUAGE = None
        if message!=None:
            if settings.SETTINGS["miscellaneous"]["status_window_enabled"]:
                control.nexus().comm.get_com("status").text(message)
    
    LAST_EXTENSION = extension
