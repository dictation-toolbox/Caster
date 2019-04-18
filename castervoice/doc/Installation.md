# Installation

Caster currently supports the following speech recognition engines on Microsoft Windows Vista through Windows 10.

- Windows Speech Recognition (WSR)
- Dragon NaturallySpeaking (DNS) - *Caster only supports Dragon NaturallySpeaking 13 or higher.

### 1. Python

- **First** Download and install [Python v2.7.X  32-bit](https://sourceforge.net/projects/natlink/files/pythonfornatlink/python2.7.14/python2.7.14.exe/download) or higher but not Python 3

Make sure to select `Add python to path`. This can be done manually by searching for "edit environment variables for your account" and adding your Python27 folder to the list of Path values

### 2. NatLink

- **Second only for Dragon NaturallySpeaking**.

- Download and install [Natlink](https://sourceforge.net/projects/natlink/files/natlink/natlinktest4.1/). Use `Natlink-4.1 whiskey3` or newer.

- Create a new folder in your Documents `C:\Users\<YourUsername>\Documents` called `Caster` with a capital C.

  1. Open the start menu and search for `natlink`, click the file called `Configure NatLink via GUI`.

       ![Configure start](https://mathfly.org/images/configure_start.png)

  2. Ensure that the details of your DNS setup are correct in the “info” tab.

  3. In the “configure” tab, under “NatLink” and “UserDirectory” click  enable. When you are prompted for a folder, give it the location of the empty folder folder (`C:\Users\<YourUsername>\Documents\Caster`).

       ![Caster-Natlink.jpg](https://i.postimg.cc/d1jN4xcw/Caster-Natlink.jpg)

**Third** download Caster and install dependencies. Choose **PIP** or **Classic** Install.

**PIP** install is convenient way to install Caster and uses it's development branch. **Classic** install enables the user to track changes with Caster code using git. Git allows users to contribute their own code to the Caster project. 

- **PIP Install** (Beta) - If you're using DNS make sure you've installed and configured NatLink first! Open [command prompt](https://www.wikihow.com/Open-the-Command-Prompt-in-Windows) (CMD) and type the following then press enter.

`pip install castervoice` 

At the end of the PIP install instructions a CMD window will guide you of what to expect for WSR or DNS. Setup complete. **Note** If a window does not appear please refer to the troubleshooting section.  

- **Classic Install**

 The classic install is for Caster development or as an alternative install method.  **Note**: If you wish to contribute Castor code instructions for creating your own fork can be found in [Contributing.md](https://github.com/dictation-toolbox/Caster/blob/develop/castervoice/doc/Contributing.md) and you can skip to step 3.

1. Download and Install [git](https://git-scm.com/downloads)

2. Open [command prompt](https://www.wikihow.com/Open-the-Command-Prompt-in-Windows) (CMD)  `cd C:\Users\<YourUsername>\Documents` 

3. `git clone https://github.com/dictation-toolbox/Caster.git` then run one of the following command

   `git checkout develop` Development branch

   `git checkout master` Master branch

4. Check and install Caster dependencies from CMD. Change the directory to the install directory selected in this step 

5. Change directory example `cd C:\Users\<YourUsername>\Documents\Caster`

   Then `pip install -r requirements.txt`

### 4. Setup and launch for Classic Install.

- **Dragon NaturallySpeaking**
  1. Start or reboot Dragon. NatLink should load at the same time, with caster commands available. To test this, open a notepad window and try saying `arch brov char delta` producing `abcd` text.
- **Windows Speech Recognition**
  1.  In  `C:\Users\<YourUsername>\Documents\Caster`
  2.  Start caster by double click on `_caster.py`. 
  3.  To test open a notepad window and try saying `arch brov char delta` producing `abcd` text. Set up complete!

### Troubleshooting FAQ

**Caster Install**

- For WRS double clicking on `_caster.py` or `start_caster.py` opens the file and does not launch Caster. 
  **Note** Depending on your file associations it may launch an editor instead of running the file. Run the file using CMD. Detailed instructions below.
  1. Change the directory to  `Desktop` in CMD.
     Example PIP `cd C:\Users\<YourUsername>\Desktop` or Classic `cd C:\Users\<YourUsername>\Documents\Caster`
  2. Then Classic:`python _caster.py` or PIP: `python start_caster.py` 

- You have followed the PIP install `pip install castervoice` CMD window does not provide instructions during install. Caster does not start with DNS automatically or `start_caster.py` does not appear on the desktop for WSR.

  -  Look for `CasterInstall.log` on your desktop to check for error messages.
  - The PIP install is in beta yet please report any issues or error messages that you experience github [issues](https://github.com/dictation-toolbox/Caster/issues) or [gitter chat](https://gitter.im/synkarius/Caster?utm_source=share-link&utm_medium=link&utm_campaign=share-link). 


**NatLink**

- When using `start_configurenatlink.py` gives  `ImportError: No module named six"` or `ImportError: No module named future"`

  To fix pip Install  `pip install six` or `pip install dragonfly2` in CMD

- Cannot load compatibility module support `(GUID = {dd990001-bb89-1d2-b031-0060088dc929}))`

  [Detailed Instructions](https://qh.antenna.nl/unimacro/installation/problemswithinstallation.html) Typically fixed by installing Microsoft Visual C++ 2010 Service Pack 1 Redistributable Package

- Running "Configure NatLink via GUI" does not bring up the settings window - try running the program as an administrator:

  1. Open an administrator command prompt by searching for "cmd" in start and either right click, run as administrator or ctrl-shift-enter.

  2. Change directory to the folder where start_configurenatlink.py was installed. This is likely to be 

     `cd C:\NatLink\NatLink\confignatlinkvocolaunimacro`.

  3. Run `python start_configurenatlink.py`.

- The [qh.antenna troubleshooting guide](https://qh.antenna.nl/unimacro/installation/problemswithinstallation.html) has further solutions for NatLink Issues.

**Dragonfly**

- Fix TypeError: command must be a non-empty string, not ['C:\\Python27\\Scripts\\pip.exe', 'search', 'castervoice']
  Update `pip install --upgrade dragonfly2` Dragonfly
- Commands work in some applications but not others that are supported by Caster. To fix verify that the program is not running an administrator/elevated privileges. Dragonfly grammars cannot interact with programs that have administrator/elevated privileges.
  - Advanced [Workaround](https://groups.google.com/d/msg/dragonflyspeech/2VrJKBI2mSo/R4zl6u2mBwAJ) - Editing natlink.exe with hex editor and re-signing with self signed certificate - **Use at your own risk!** Instructions note disadvantages.
  - [Proof of Concept](https://github.com/dictation-toolbox/dragonfly/issues/11) work around but the project needs an active developer with C#.
- To fix `ImportError: No module named win32con`
  Package win32con is out of date or not installed. Try `pip install pywin32`  Alternatively if the error persists use the [Windows installer](https://sourceforge.net/projects/pywin32/files/pywin32/Build%20221/pywin32-221.win32-py2.7.exe/download)
- To fix `lost sys.stder` use `pywin32` for `system wide` features, such as registering COM objects or implementing Windows Services. So you **must** run the following command from an elevated CMD:

> python C:\Python27\Scripts\pywin32_postinstall.py -install

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

## YouTube Videos 

The following install videos are a out of date but remain for reference.

- [Natlink](https://www.youtube.com/watch?v=dj5xgWSOEXA)

- [Dragonfly](https://www.youtube.com/watch?v=iNAsV4pcnEA) 

- [Caster](https://www.youtube.com/watch?v=wjSwB4cpMDI)

  

**Alternative Speech Secognition Engines.**

CMU Pocket Sphinx [Install Instructions](https://dragonfly2.readthedocs.io/en/latest/sphinx_engine.html) for dragonfly - Linux only - Currently not supported Caster but it is a work in progress.
