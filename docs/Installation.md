# Installation

Caster currently supports the following speech recognition engines on Microsoft Windows Vista through Windows 10.

- Windows Speech Recognition (WSR)
- Dragon NaturallySpeaking (DNS) - Caster only supports Dragon NaturallySpeaking 13 or higher.

### 1. Python

- **First** Download and install [Python v2.7.X  32-bit](https://sourceforge.net/projects/natlink/files/pythonfornatlink/python2.7.14/python2.7.14.exe/download) or higher but not Python 3. These dependencies will change when Natlink utilizes Python 3.

Make sure to select `Add python to path`. This can be done manually by searching for "edit environment variables for your account" and adding your Python27 folder to the list of Path values

### 2. NatLink 

- **Second only for Dragon NaturallySpeaking**.

- Download and install [Natlink](https://sourceforge.net/projects/natlink/files/natlink/natlinktest4.1/). Use `Natlink-4.1 whiskey3` or newer.

### 3. Caster
1. Download Caster from the [master branch](https://github.com/dictation-toolbox/Caster/archive/master.zip).
2. Open up the zip file downloaded
3. Extract the `Caster-master` folder, you can put it anywhere but it is common to use `user\Documents\Caster`.
4. Install dependencies and set up Natlink by running `Caster-master/Install.bat` as administrator. *Note that for this to work correctly Python must be installed to `C:/Python27` and Natlink installed to `C:/NatLink`, their default locations. If this is not the case or if the installation script fails for some other reason then see below for instructions on manual configuration.*

### 4. Setup and launch for Classic Install.

- **Dragon NaturallySpeaking**
  1. Start or reboot Dragon. NatLink should load at the same time, with caster commands available. To test this, open Window's Notepad and try saying `arch brov char delta` producing `abcd` text.
- **Windows Speech Recognition**
  1. In  `C:\Users\<YourUsername>\Documents\Caster`
  2. Start caster by double click on `_caster.py`. 
  3. To test open Window's Notepad and try saying `arch brov char delta` producing `abcd` text. Set up complete!

### Manual configuration

1. Open [command prompt](https://www.wikihow.com/Open-the-Command-Prompt-in-Windows) (CMD) and type the following then press enter.

  - `python -m pip install future six wxPython pywin32`

2. Open the start menu and search for `natlink`, click the file called `Configure NatLink via GUI`.

     ![Configure start](https://mathfly.org/images/configure_start.png)

3. Ensure that the details of your DNS setup are correct in the “info” tab.

4. In the “configure” tab, under “NatLink” and “UserDirectory” click enable. When you are prompted for a folder, give it the folder containing `install.bat` (`C:\Users\<YourUsername>\Documents\Caster`).

     ![Caster-Natlink.jpg](https://i.postimg.cc/d1jN4xcw/Caster-Natlink.jpg)

###  **PIP Install** (Beta) 
If you're using DNS make sure you've installed and configured NatLink first! Open [command prompt](https://www.wikihow.com/Open-the-Command-Prompt-in-Windows) (CMD) and type the following then press enter.

`pip install castervoice` 

At the end of the PIP install instructions a CMD window will guide you of what to expect for WSR or DNS. Setup complete. **Note** If a window does not appear please refer to the troubleshooting section.  

### Troubleshooting FAQ

**Caster Install**

- For WRS double clicking on `_caster.py` or `start_caster.py` opens the file and does not launch Caster. 
  **Note** Depending on your file associations it may launch an editor instead of running the file. Run the file using CMD. Detailed instructions below.
  1. Change the directory to  `Desktop` in CMD.
     Example PIP `cd C:\Users\<YourUsername>\Desktop` or Classic `cd C:\Users\<YourUsername>\Documents\Caster`
  2. Then Classic:`python _caster.py` or PIP: `python start_caster.py` 
- You have followed the PIP install `pip install castervoice` CMD window does not provide instructions during install. Caster does not start with DNS automatically or `start_caster.py` does not appear on the desktop for WSR.
  - Look for `CasterInstall.log` on your desktop to check for error messages.
  - The PIP install is in beta yet please report any issues or error messages that you experience github [issues](https://github.com/dictation-toolbox/Caster/issues) or [gitter chat](https://gitter.im/synkarius/Caster?utm_source=share-link&utm_medium=link&utm_campaign=share-link). 
- To fix `ERROR:action.exec:Execution failed: Function(mouse_alternates): [Error 126] The specified module could not be found`. Triggered by using the `Legion` command
  In order to use Legion, you may need to install [Microsoft Visual C++ Redistributable Packages for Visual Studio 2019 (x86).](https://support.microsoft.com/en-nz/help/2977003/the-latest-supported-visual-c-downloads). We have found that Legion works without this requirement on Windows 10 computers that are up-to-date but not on all Windows 7 computers, even with the VS packages installed. Please raise an issue if you find Legion still doesn't work on Windows 10 after installing the requirement or if you have managed to get Legion working on Windows 7.

**NatLink**

- When using `start_configurenatlink.py` gives  `ImportError: No module named six"` or `ImportError: No module named future"`

  To fix pip Install  `pip install six` or `pip install dragonfly2` in CMD

- Cannot load compatibility module support `(GUID = {dd990001-bb89-1d2-b031-0060088dc929}))`

  [Detailed Instructions](https://qh.antenna.nl/unimacro/installation/problemswithinstallation.html) Typically fixed by installing Microsoft Visual C++ 2010 Service Pack 1 Redistributable Package

  - May need to unRegister and then reRegister Natlink from the GUI

- Running "Configure NatLink via GUI" does not bring up the settings window - try running the program as an administrator:

  1. Open an administrator command prompt by searching for "cmd" in start and either right click, run as administrator or ctrl-shift-enter.

  2. Change directory to the folder where start_configurenatlink.py was installed. This is likely to be 

     `cd C:\NatLink\NatLink\confignatlinkvocolaunimacro`.

  3. Run `python start_configurenatlink.py`.

- The [qh.antenna troubleshooting guide](https://qh.antenna.nl/unimacro/installation/problemswithinstallation.html) has further solutions for NatLink Issues.

**Windows Speech Recognition (WSR)** 

- The WSR User interface does not show up just a terminal window and WSR commands do not work.

  This [Issue]() changed how WSR was loaded in dragonfly `Sapi5SharedEngine containing rules with <n> do not load (-2147352567, 'Exception occurred.', (0, None, None, None, 0, -2147200940), None)` As a workaround  `Sapi5InProcEngine ` was used which does not load the user interface or built-in WSR commands. 

- When starting up or setting up WSR you receive the following error message. 

  ```
  The recognizer language must match the language of the user 
  interface. Please change the recognizer language in the Speech 
  Recognition control panel under Advanced Options.
  ```

  - To fix go to: [Windows Seven and Vista”](https://www.askvg.com/fix-speech-recognition-shows-change-recognizer-language-error-in-windows-vista-and-7/), [Windows 10](https://www.tenforums.com/tutorials/120631-change-speech-recognition-language-windows-10-a.html) and follow the instructions.

**Dragonfly**

- Fix TypeError: command must be a non-empty string, not ['C:\\Python27\\Scripts\\pip.exe', 'search', 'castervoice']
  Update `pip install --upgrade dragonfly2` Dragonfly
- Commands work in some applications but not others that are supported by Caster. To fix verify that the program is not running an administrator/elevated privileges. Dragonfly grammars cannot interact with programs that have administrator/elevated privileges.
  - Advanced [Workaround](https://groups.google.com/d/msg/dragonflyspeech/2VrJKBI2mSo/R4zl6u2mBwAJ) - Editing natlink.exe with hex editor and re-signing with self signed certificate - **Use at your own risk!** Instructions note disadvantages.
  - [Proof of Concept](https://github.com/dictation-toolbox/dragonfly/issues/11) work around but the project needs an active developer with C#.
- To fix `ImportError: No module named win32con`
  Package win32con is out of date or not installed. Try `pip install pywin32`  Alternatively if the error persists use the [Windows installer](https://sourceforge.net/projects/pywin32/files/pywin32/Build%20221/pywin32-221.win32-py2.7.exe/download)
- To fix `lost sys.stder` use `pywin32` for `system wide` features, such as registering COM objects or implementing Windows Services. So you **must** run the following command from an elevated CMD:
  - `python C:\Python27\Scripts\pywin32_postinstall.py -install`

- To fix `ImportError: cannot import name RuleWrap`
  You likely either have the wrong version of Dragonfly installed, or don't have it installed at all.  RuleWrap is a Dragonfly import. Try `pip uninstall dragonfly` (it's okay if it doesn't find the package) then `pip install dragonfly2`.

### Extra information

Caster dependencies
--installed by **Dragonfly**

- pywin32
- dragonfly2
- setuptools
- six
- pyperclip
- enum34
- comtypes
- regex

--installed by **Caster**

- wxpython
- pillow
- toml
- future
- mock

## YouTube Videos 

The following install videos are a out of date but remain for reference.

- [Natlink](https://www.youtube.com/watch?v=dj5xgWSOEXA)

- [Dragonfly](https://www.youtube.com/watch?v=iNAsV4pcnEA) 

- [Caster](https://www.youtube.com/watch?v=wjSwB4cpMDI)

**Alternative Speech Secognition Engines.**

CMU Pocket Sphinx [Install Instructions](https://dragonfly2.readthedocs.io/en/latest/sphinx_engine.html) for dragonfly - Linux only - Currently not supported Caster but it is a work in progress.

[Kaldi backend (native on Linux & Windows)](https://github.com/dictation-toolbox/dragonfly/pull/78) for dragonfly - Possible integration for Windows, Linux not supported at this time. 
