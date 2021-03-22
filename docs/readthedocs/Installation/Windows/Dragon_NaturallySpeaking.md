# Dragon NaturallySpeaking- Classic Install

**Install Dragon NaturallySpeaking** (DPI / DNS)- Caster only supports Dragon NaturallySpeaking 13 and Windows 7 or higher.

After installing Dragon Naturally Speaking, you can configure the DNS settings based on your preference.

- Disabling the DNS Browser plug-ins due to instability of Internet browsers and DNS is recommended.
- Disable all the checkboxes in the “Correction” menu, except for the “Automatically add words to the active vocabulary” option.
    - Under the “Commands” menu check the “Require click to select…” checkboxes.  Otherwise you will find yourself accidentally clicking buttons or menu items instead of inserting text into your editor. I’ve disabled the other checkboxes in that menu as well.
- Set the “speed versus accuracy” slider in the “Miscellaneous” menu to a fairly high value.
- Uncheck the “Use the dictation box for unsupported applications” checkbox. Use Caster text manipulation instead.

## Python

1. Download and install [Python v2.7.18 32-bit](https://www.python.org/downloads/release/python-2718/) listed as `Windows x86 MSI installer` not Python 3 or the Python 2.7 64-bit.

    - These dependencies will change when Natlink utilizes Python 3.

2. Make sure to select `Add python to path`.

    - This can be done manually by searching for "edit environment variables for your account" and adding your Python folder to the list of Path values

## NatLink

- Download and install [Natlink](https://sourceforge.net/projects/natlink/files/natlink/natlink4.2/). Use `Natlink-4.2` or newer.
  
  1. Verify (DPI / DNS) is not running.
  
  2. Open the start menu and search for `Configure NatLink` and click `Configure NatLink via GUI`.
    ![Configure start](https://mathfly.org/images/configure_start.png)

  3. Register Natlink and Restart your computer.
    ![Natlink-Setup1.jpg](https://i.postimg.cc/3wdKsJFS/Natlink-Setup1.jpg)

  4. Relaunch `Configure NatLink via GUI`. Then disable Natlink. Done with Natlink setup.
      ![Natlink-Setup2.jpg](https://i.postimg.cc/j20TGHMv/Natlink-Setup2.jpg)

### Caster

  1. Download Caster from the [master branch](https://github.com/dictation-toolbox/Caster/archive/master.zip).
  2. Open up the zip file downloaded
  3. Copy the contents of `Caster-master` folder. You can put it anywhere but it is common to use `%USERPROFILE%\Documents\Caster`.
  4. Install dependencies and set up Natlink by running `Caster/Install_Caster_DNS-WSR.bat`. 
    - *Note: For this to work correctly, Python must be installed to `C:/Python27` **
    - **Optional Step** for Caster's `Legion` MouseGrid- Legion Feature available on Windows 8 and above.
  5. The Legion MouseGrid requires [Microsoft Visual C++ Redistributable Packages for Visual Studio 2015, 2017 and 2019 (x86).](https://support.microsoft.com/en-nz/help/2977003/the-latest-supported-visual-c-downloads) Note: Should not be needed if Windows 10 is up-to-date.

### **Setup and launch DNS for Classic Install.**

> 1. Start or restart Dragon. `Click Run_Caster_DNS.bat` Status Window appear and load Caster.  Once loaded Caster commands should be available to dictate.
> 2. To test this, open Window's Notepad and try saying `arch brov char delta` producing `abcd` text.

### Update Caster

> 1. Backup `%USERPROFILE%\Documents\Caster`
> 2. Delete `%USERPROFILE%\Documents\Caster`
> 3. Repeat Steps `1.- 4.` within the Caster install section

------

### -Alternative- Natlink Configuration

An alternative to the instructions above for configuring Natlink. Automatically launches Caster when DNS starts. The disadvantage of this method is when Caser restarts so does DNS. Open the start menu and search for `natlink` and click the file called `Configure NatLink via GUI`.

1. Open Configure Natlink
    - ![Configure start](https://mathfly.org/images/configure_start.png)
> Ensure that the details of your DNS setup are correct in the “info” tab.

2. In the "configure" tab Register Natlink and Restart your computer.

  ![Caster-Natlink.jpg](https://i.postimg.cc/d1jN4xcw/Caster-Natlink.jpg)
3. Relaunch the GUI. In the “configure” tab- under “NatLink” and “UserDirectory”- click enable. When you are prompted for a folder, give it the folder
 - `C:\Users\<YourUsername>\Documents\Caster`

### Natlink Troubleshooting FAQ

1. Visual C++ Runtime Error R6034 on Dragon launch. This is related to Natlink. You can safely ignore it.
    - A Fix: "Core directory of NatLink (...\NatLink\MacroSystem\core) there is a directory msvcr100fix. Please consult the NatLink README.txt file.
        - See if copying the dll file (msvcr100.dll) to the Core directory (one step up) solves your problem."  
        - Note: Not recommended for Windows 10.
    - A dated discussion [VoiceCoder](https://groups.yahoo.com/neo/groups/VoiceCoder/conversations/topics/7925) on the issue.
2. When using `start_configurenatlink.py` gives  `ImportError: No module named six"` or `ImportError: No module named future"`
    - To fix pip Install  `pip install six` or `pip install dragonfly2` in CMD
3. Cannot load compatibility module support `(GUID = {dd990001-bb89-1d2-b031-0060088dc929}))`
  
    - [Detailed Instructions](https://qh.antenna.nl/unimacro/installation/problemswithinstallation.html) Typically fixed by installing Microsoft Visual C++ 2010 Service Pack 1 Redistributable Package
    - May need to unRegister and then reRegister Natlink from the GUI

4. Running "Configure NatLink via GUI" does not bring up the settings window- try running the program as an administrator: 
      1. A Fix: Open an administrator command prompt by searching for "cmd" in start and right click run as administrator.
      2. Change directory to the folder where start_configurenatlink.py was installed. See command below:
      3. `cd C:\NatLink\NatLink\confignatlinkvocolaunimacro`.
      4. Run `python start_configurenatlink.py`.

See [qh.antenna troubleshooting guide](https://qh.antenna.nl/unimacro/installation/problemswithinstallation.html) has further solutions for NatLink Issues.
