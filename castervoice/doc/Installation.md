# Installation

## YouTube Videos

- [Dragonfly](https://www.youtube.com/watch?v=iNAsV4pcnEA)
- [Caster](https://www.youtube.com/watch?v=wjSwB4cpMDI)

## **Introduction**
Caster currently supports the following speech recognition engines on Microsoft Windows Vista through Windows 10.

* Windows Speech Recognition (WSR)
* Dragon NaturallySpeaking (DNS) - *Caster only supports Dragon NaturallySpeaking 13 or higher.

### 1. Python
* **First** Download and install [Python v2.7.X  32-bit](https://sourceforge.net/projects/natlink/files/pythonfornatlink/python2.7.14/python2.7.14.exe/download) or higher but not Python 3

Make sure to select `Add python to path`. This can be done manually by searching for "edit environment variables for your account" and adding your Python27 folder to the list of Path values

### 2. NatLink
* **Second only for Dragon NaturallySpeaking**. Download [Natlink](https://sourceforge.net/projects/natlink/files/natlink/natlinktest4.1/). Use natlink-4.1 victor or newer.

  * [Install Video instructions](https://www.youtube.com/watch?v=dj5xgWSOEXA)

### 3. Caster

**Third** Download Caster and install dependencies.

1. Download Caster from [master branch](https://github.com/synkarius/caster/archive/master.zip). **Note** If you plan to develop Caster use the [development branch](https://github.com/synkarius/caster/archive/develop.zip).
2. Open up the zip file downloaded
3. Click on the file `caster-master` or `caster-develop` . **Note** Choose based on your speech recognition engine.
  * **Dragon NaturallySpeaking** (DNS) copy and paste its contents into An empty folder, this can be any folder but it is common to use `user\Documents\NatLink`.
  * **Windows Speech Recognition**  (WSR) copy and paste its contents to a new folder. Suggested locations would be a folder on the desktop for ease of access.
4. Check and install Caster dependencies by clicking on `Pip Install Dependencies.bat` in `\caster\bin\inno\dependencies`
	* This can be done manually by pip installing dragonfly2, pywin32, wxpython, pillow, psutil

### 4. Setup and launch

* **Dragon NaturallySpeaking**
  1. Open the start menu and search for "natlink", click the file called "Configure NatLink via GUI" and run it using python 2.7.
  2. Ensure that the details of your DNS setup are correct in the "info" tab.
  3. In the "configure" tab, under "NatLink" and "UserDirectory" click enable. When you are prompted for a folder, give it the location of your caster folder from step three (`user\Documents\NatLink\caster-master`).
  4. Reboot Dragon. NatLink should load at the same time, with caster commands available. To test this, open a notepad window and try saying "arch brov char delta".
* **Windows Speech Recognition** double click on `_caster.py`and it will launch WSR. **Note** Depending on your file associations it may launch an editor instead of running the file. Run the file using  [command prompt](https://www.wikihow.com/Open-the-Command-Prompt-in-Windows). Detailed instructions below.
  1. Change the directory to the to the file path you created in the step above. If the folder `<YourFile>` was named `caster-master`.
   Example `cd C:\Users\<YourUsername>\Desktop\caster-master\`
  2. Then `python _caster.py`

### Troubleshooting FAQ

* Running "Configure NatLink via GUI" does not bring up the settings window - try running the program as an administrator:
  1. Open an administrator command prompt by searching for "cmd" in start and either right click, run as administrator or ctrl-shift-enter.
  2. Change directory to the folder where start_configurenatlink.py was installed. This is likely to be `C:\NatLink\NatLink\confignatlinkvocolaunimacro` so the command would be `cd C:\NatLink\NatLink\confignatlinkvocolaunimacro`.
  3. Run `python start_configurenatlink.py`.
* To fix `ImportError: No module named win32con`
  Package win32con is out of date or not installed. Try `pip install pywin32`  Alternatively if the error persists use the [Windows installer](https://sourceforge.net/projects/pywin32/files/pywin32/Build%20221/pywin32-221.win32-py2.7.exe/download)
* To fix `lost sys.stderr`
  For Caster must use pywin32 for `system wide` features, such as registering COM objects or implementing Windows Services, then you **must** run the following command from an elevated command prompt:

> python C:\Python27\Scripts\pywin32_postinstall.py -install

* To fix `ImportError: cannot import name RuleWrap`
  You likely either have the wrong version of Dragonfly installed, or don't have it installed at all.  RuleWrap is a Dragonfly import. Try `pip uninstall dragonfly` (it's okay if it doesn't find the package) then `pip install dragonfly2`.

### Extra information

Castor dependencies
--installed by **Dragonfly**

* pywin32
* dragonfly2
* setuptools
* six
* pyperclip

--installed by **Caster**

* wxpython
* pillow
* toml

**Alternative Speech Secognition Engines.**

CMU Pocket Sphinx [Install Instructions](https://dragonfly2.readthedocs.io/en/latest/sphinx_engine.html) for dragonfly - Linux only - Currently not supported Caster but it is a work in progress.
