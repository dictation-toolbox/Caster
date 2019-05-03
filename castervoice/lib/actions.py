from dragonfly import Key, Mouse
from dragonfly import Text as TextBase

from castervoice.lib import settings

class Text(TextBase):
    # dragonfly default is 0.02, too slow!
    _pause_default = 0.003
    def __init__(self, spec=None, static=False, pause=_pause_default, autofmt=False, use_hardware=False):
        TextBase.__init__(self, spec=spec, static=static, pause=pause, autofmt=autofmt, use_hardware=use_hardware)

# Override imported dragonfly actions with aenea's if the 'use_aenea' setting
# is set to true.
if settings.SETTINGS["miscellaneous"]["use_aenea"]:
    try:
        from aenea import Key, Text, Mouse
    except ImportError:
        print("Unable to import aenea actions. Dragonfly actions will be used "
              "instead.")
