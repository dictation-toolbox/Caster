

from dragonfly import Mimic

from lib import utilities, settings


AUTO_ENABLED_LANGUAGE = None
LAST_EXTENSION = None

def toggle_language():
    global AUTO_ENABLED_LANGUAGE, LAST_EXTENSION
    filename, folders, title = utilities.get_window_title_info()
    extension = None
    if filename != None:
        extension = "." + filename.split(".")[-1]
    
    if LAST_EXTENSION != extension:
        if extension != None and extension in settings.SETTINGS["ccr"]["registered_extensions"]:
            words_to_mimic = ["enable"] + settings.SETTINGS["ccr"]["registered_extensions"][extension].split(" ")
            Mimic(*words_to_mimic).execute()
            AUTO_ENABLED_LANGUAGE = settings.SETTINGS["ccr"]["registered_extensions"][extension]
            LAST_EXTENSION = extension
        elif AUTO_ENABLED_LANGUAGE != None:
            words_to_mimic = ["disable"] + AUTO_ENABLED_LANGUAGE.split(" ")
            Mimic(*words_to_mimic).execute()
            AUTO_ENABLED_LANGUAGE = None
    
    LAST_EXTENSION = extension
