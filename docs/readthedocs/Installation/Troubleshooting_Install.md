## Troubleshooting Install

In the previous install documentation, each speech recognition engine has its own troubleshooting section. However this troubleshooting section applies to all engines as it relates to issues installing Caster and Dragonfly.

**Caster**

On startup Caster checks for missing python dependencies.  When a dependency is missing, Caster will print out the appropriate commands to the status window for the end-user to fix the issue in command prompt/terminal.

- To fix `ERROR:action.exec:Execution failed: Function(mouse_alternates): [Error 126] The specified module could not be found`. Triggered by using the `Legion` command.
  In order to use Legion, you may need to install [Microsoft Visual C++ Redistributable Packages for Visual Studio 2019 (x86).](https://support.microsoft.com/en-nz/help/2977003/the-latest-supported-visual-c-downloads). We have found that Legion works without this requirement on Windows 10 computers that are up-to-date but not on all Windows 7 computers, even with the VS packages installed. Please raise an issue if you find Legion still doesn't work on Windows 10 after installing the requirement or if you have managed to get Legion working on Windows 7.

**Dragonfly**

- If commands work in some applications but not others that are supported by Caster, verify that the program is not running as administrator with elevated privileges. Dragonfly grammars cannot interact with programs that have administrator/elevated privileges. To fix:
    - Run the .bat file as administrator. **Note** this means the entirety of Caster and Dragonfly will run as administrator which poses a significant security risk in general. Use this method with caution.
    - [Proof of Concept](https://github.com/dictation-toolbox/dragonfly/issues/11) work around but the project needs an active developer with C#. This allows Caster and Dragonfly to only elevate specific functionality that is necessary such as Key/Text actions and application context details.
    - Advanced [Workaround](https://groups.google.com/d/msg/dragonflyspeech/2VrJKBI2mSo/R4zl6u2mBwAJ) - Editing natlink.exe with hex editor and re-signing with self signed certificate - **Use at your own risk!** Instructions note disadvantages.
- Fix `TypeError: command must be a non-empty string, not ['C:\\Python27\\Scripts\\pip.exe', 'search', 'castervoice']`
  
    - Update Dragonfly `python -m pip install dragonfly2 --upgrade` in command prompt
- To fix `ImportError: No module named win32con`
  Package win32con is out of date or not installed. Try `python -m pip install pywin32`.  Alternatively if the error persists use the [Windows installer](https://sourceforge.net/projects/pywin32/files/pywin32/Build%20221/pywin32-221.win32-py2.7.exe/download)
- To fix `lost sys.stder` use `pywin32` for `system wide` features, such as registering COM objects or implementing Windows Services. Depending on Python version, run the following command from an elevated CMD:
  
    - `python C:\Python27\Scripts\pywin32_postinstall.py -install`
- To fix `ImportError: cannot import name RuleWrap`
  You likely either have the wrong version of Dragonfly installed or don't have it installed at all.  RuleWrap is a Dragonfly import. Try `pip uninstall dragonfly` (it's okay if it doesn't find the package) then `pip install dragonfly2`.
