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

### 3. Dragonfly
* **Third** Install Dragonfly from [Command Prompt](https://www.wikihow.com/Open-the-Command-Prompt-in-Windows) or Windows Power Shell. Type `pip install dragonfly2` or `python -m pip install dragonfly2` and press enter

**Note** If migrating from [t4ngo/dragonfly](https://github.com/t4ngo/dragonfly) to [Danesprite/dragonfly](https://github.com/Danesprite/dragonfly/issues). Simply close Dragon NaturallySpeaking and run `pip uninstall dragonfly` then `pip install dragonfly2` from command line to use the danesprite's new distribution.

### 4. Caster
* **Fourth** Detailed instructions for Caster below.

1. Download Caster from [master branch](https://github.com/synkarius/caster/archive/master.zip).
   **Note** If you plan to develop Caster use the [development branch](https://github.com/synkarius/caster/archive/develop.zip).
2. Open up the zip file downloaded
3. Click on the file `caster-master` or `caster-develop` .
   **Note** Choose based on your speech recognition engine.

* **Dragon NaturallySpeaking** (DNS) copy and paste its contents into `C:\NatLink\NatLink\MacroSystem` or If you installed `Natlink`  in an alternate location  `...\NatLink\MacroSystem`
* **Windows Speech Recognition**  (WSR) copy and paste its contents to a new folder. Suggested locations would be a folder on the desktop for ease of access.

1. Check and install Caster dependencies by clicking on `Pip Install Dependencies.bat` in `\caster\bin\inno\dependencies`
	* This can be done manually by pip installing pywin32, wxpython, pillow, psutil
2. **Final Step**. Launching Caster with a speech recognition engine.
   ​	 **Note** Choose based on your speech recognition engine

* **Dragon NaturallySpeaking** simply Launch DNS and Caster will automatically load.
* **Windows Speech Recognition**  double click on `_caster.py`and it will launch WSR.
  **Note** Pending on your file associations it may launch an editor instead of running the file. Run the file using  [command prompt](https://www.wikihow.com/Open-the-Command-Prompt-in-Windows). Detailed instructions below.

1. Change the directory to the to the file path you created in the step above. If the folder `<YourFile>` was named `caster-master`.
   Example `cd C:\Users\<YourUsername>\Desktop\caster-master\`
2. Then`python _caster.py`

### Troubleshooting FAQ

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

**Alternative Speech Secognition Engines.**

CMU Pocket Sphinx [Install Instructions](https://dragonfly2.readthedocs.io/en/latest/sphinx_engine.html) for dragonfly - Linux only - Currently not supported Caster but it is a work in progress.
