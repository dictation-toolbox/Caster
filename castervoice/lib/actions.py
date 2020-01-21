from dragonfly import Key, Mouse
from dragonfly import Text as TextBase

from castervoice.lib import settings

class Text(TextBase):
    # dragonfly _pause_default 0.02 is too slow! Caster default 0.003
    _pause_default = settings.settings(["miscellaneous", "dragonfly_pause_default"])
    def __init__(self, spec=None, static=False, pause=_pause_default, autofmt=False, use_hardware=False):
        TextBase.__init__(self, spec=spec, static=static, pause=pause, autofmt=autofmt, use_hardware=use_hardware)

# Override imported dragonfly actions with aenea's if the 'use_aenea' setting
# is set to true.
if settings.settings(["miscellaneous", "use_aenea"]):
    try:
        from aenea import Key, Text, Mouse
    except ImportError:
        print("Unable to import aenea actions. Dragonfly actions will be used "
              "instead.")
