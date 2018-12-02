from dragonfly import Key, Text, Mouse

from caster.lib import settings

# Override imported dragonfly actions with aenea's if the 'use_aenea' setting
# is set to true.
if settings.SETTINGS["miscellaneous"]["use_aenea"]:
    try:
        from aenea import Key, Text, Mouse
    except ImportError:
        print("Unable to import aenea actions. Dragonfly actions will be used "
              "instead.")
