#Rule Construction

This page demonstrates how to get started making Dragonfly and Caster rules. Let's start with a very simple Dragonfly `MappingRule`. The following is a complete Python file which will work with Dragon. (For WSR, see the WSR page.)

```
# the following line imports all the dragonfly stuff we'll be using -- obviously you must have Dragonfly installed
from dragonfly import *

# now we make our MappingRule object with only two commands
class MyRule(MappingRule):
  mapping = {
    "some words I speak":         Key("a, b, c"),
    "command number two":         Text("here is a hashtag: #"),
  }
```

Done. Name this file `_example1.py`, put it in your Natlink `User Directory` folder (configurable in the Natlink configuration GUI `start_configurenatlink.py`) and reboot Dragon. When you do, saying "some words I speak" will trigger the first command, causing the keys A, B, C to be pressed. Same for the second command. (It is a Text action rather than a Key action, but in the example the effects are similar.)
