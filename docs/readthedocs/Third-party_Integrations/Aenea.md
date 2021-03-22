# Aenea Compatibility

Caster can be used with [Aenea](https://github.com/dictation-toolbox/aenea), a client-server library for using voice macros from Dragon NaturallySpeaking and Dragonfly on remote/non-Windows hosts (Linux or MacOS).

Aenea-Caster compatibility includes:

* Using Aenea's `Key`, `Text` and `Mouse` actions in place of Dragonfly's so that input occurs on the Aenea server instead.
* Importing `aenea.ProxyAppContext` as Dragonfly's `AppContext` class so that some app grammars will use the server's context instead. 
* Supporting Caster's clipboard functionality, such as the `"stoosh"` and `"spark"` commands, by synchronising the Aenea server's clipboard with the client system's clipboard. This requires a server plugin.

To use Aenea-Caster compatibility, do the following:

1. Make sure that Aenea is setup correctly with following the [instructions](https://github.com/dictation-toolbox/aenea).
1. Copy `aenea.json`, which is usually created in `C:\NatLink\NatLink\MacroSystem` in the course of the Aenea install, to your NatLink User Directory. You can find this directory by running `Configure NatLink by GUI` and looking for the box titled UserDirectory. Often it is `C:\Users\<YourUsername>\Documents\Caster`.
1. Change the `use_aenea` setting in your Caster settings.toml file to true. You may find settings.toml in `C:\Users\<YourUsername>\AppData\Local\caster\settings`.
1. Copy the copypaste.py and copypaste.yapsy-plugin files from [magneto-host/server/linux_x11/plugins](https://github.com/Danesprite/magneto-host/tree/master/server/linux_x11/plugins) into your server plugins directory (usually *aenea/server/linux\_x11/plugins* or *aenea/server/osx/plugins*).
1. Install dependencies for the copypaste plugin: `python -m pip install yapsy subprocess32 pyperclip`
1. Start/restart Dragon and the Aenea server.

To use this functionality in your own grammar files, import `Key`, `Text`, `Mouse`, and/or `Clipboard` as below:

``` Python
from castervoice.lib.actions import Key, Text, Mouse
from castervoice.lib.clipboard import Clipboard
```

If using `ContextAction` include the following import.

```text
from castervoice.lib.context import AppContext
```

If the `use_aenea` setting is false, the above lines will just import Dragonfly's classes.

App grammars for Windows-only programs such as Dragon and cmd.exe still import from Dragonfly. If you have other grammars that should run actions on the client instead, just import the classes from `dragonfly` normally instead of from `caster.lib.X`.

**Note**: Caster's mouse grid features currently will not work through Aenea, although it is probably possible to make them work through an additional server plugin.
