# Automatic CCR module and Command Mode switching

Caster can automatically turn CCR modules on and off based on the foreground window, as well as command mode. There's a section of the settings file that looks like the following which must be modified to activate this feature:

```json
"auto_com": {
    "active": true,
    "change_language": true,
    "change_language_only": false,
    "executables": [
        "AptanaStudio3.exe",
        "pycharm.exe",
        "notepad++.exe",
        "javaw.exe",
        "eclipse.exe",
        "studio64.exe"
    ],
    "interval": 2
}
```

Here are what the values do.

`active` : switches to command mode for executables listed in the `executables` section

`change language` : switches CCR module -- for this to work, the CCR module has to "register" itself like so:

```python
settings.register_language(".cpp", "c++")
settings.register_language(".h", "c++")
```

`change language only` : language and not command mode

`interval` : time in seconds for pinging the foreground window
