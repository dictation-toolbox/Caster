# Aenea Compatibility

Caster can be used with [Aenea](https://github.com/dictation-toolbox/aenea), a client-server library for using voice macros from Dragon NaturallySpeaking and Dragonfly on remote/non-Windows hosts (Linux or MacOS).

Aenea-Caster compatibility includes:

* Using Aenea's `Key`, `Text` and `Mouse` actions in place of dragonfly's so that input occurs on the Aenea server instead.
* Importing `aenea.ProxyAppContext` as dragonfly's `AppContext` class so that some app grammars will use the server's context instead. You might have to adjust the context parameters in some files.
* Supporting Caster's clipboard functionality, such as the `"stoosh"` and `"spark"` commands, by synchronising the Aenea server's clipboard with the client system's clipboard. This requires a server plugin.

To use Aenea-Caster compatibility, do the following:

1. Make sure that Aenea is setup correctly by following the [instructions](https://github.com/dictation-toolbox/aenea).
2. Change the `use_aenea` setting in your Caster settings.toml file to true.
3. Copy the copypaste.py and copypaste.yapsy-plugin files from [magneto-host/server/linux_x11/plugins](https://github.com/Danesprite/magneto-host/tree/master/server/linux_x11/plugins) into your server plugins directory (usually *aenea/server/linux\_x11/plugins* or *aenea/server/osx/plugins*).
4. Install dependencies for the copypaste plugin: `pip install yapsy subprocess32 pyperclip`
5. Start/restart Dragon and the Aenea server.

To use this functionality in your own grammar files, import `Key`, `Text`, `Mouse`, `AppContext` and/or `Clipboard` as below:

``` Python
from caster.lib.actions import Key, Text, Mouse
from caster.lib.clipboard import Clipboard
from caster.lib.context import AppContext

```

If the `use_aenea` setting is false, these lines will just import dragonfly's classes.

App grammars for Windows-only programs such as Dragon and cmd.exe still import from dragonfly. If you have other grammars that should run actions on the client instead, just import the classes from `dragonfly` normally instead of from `caster.lib.X`.

**Note**: Caster's mouse grid features won't work through Aenea, although it is probably possible to make them work through an additional server plugin.
