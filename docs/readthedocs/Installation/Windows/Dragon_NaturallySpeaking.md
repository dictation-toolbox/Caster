# Dragon NaturallySpeaking Install

**Install Dragon NaturallySpeaking** (DPI / DNS)- Caster only supports Dragon NaturallySpeaking v13-v15 and Windows 7 or higher.

After installing Dragon, you can configure the DNS settings based on your preference.

- Disabling the DNS Browser plug-ins due to instability of Internet browsers and DNS is recommended.
- Disable all the checkboxes in the “Correction” menu, except for the “Automatically add words to the active vocabulary” option.
    - Under the “Commands” menu check the “Require click to select…” checkboxes.  Otherwise you will find yourself accidentally clicking buttons or menu items instead of inserting text into your editor. I’ve disabled the other checkboxes in that menu as well.
- Set the “speed versus accuracy” slider in the “Miscellaneous” menu to a fairly high value.
- Uncheck the “Use the dictation box for unsupported applications” checkbox.

### Python

1. Download and install  [**Python 3.8.X 32 bit**](https://www.python.org/downloads/release/python-3810/) as `Windows x86 MSI installer` and select **add Python to Path**.


### Caster

1. Download Caster from the [master branch](https://github.com/dictation-toolbox/Caster/archive/master.zip).
2. Open up the zip file downloaded
3. Copy the contents of `Caster-master` folder. You can put it anywhere but it is common to use `%USERPROFILE%\Documents\Caster`.
4. Install dependencies and set up Natlink by running `Caster/Install_Caster_DNS-WSR.bat`. 

   - Optional Step** for Caster's `Legion` MouseGrid- Legion Feature available on Windows 8 and above.

### **Setup and launch DNS for Classic Install.**

1. Close Dragon if open
2. Open Command Prompt/PowerShell **as administrator**
3. Upgrade pip: `pip install --upgrade pip`
4. `pip install natlink` from [PyPI](https://pypi.org/project/natlink/)
6. `natlinkconfig_cli` # should auto setup and register itself.
7. (Optional) type `u` to see all CLI options
8. Set Natlink UserDirectory to Caster: type `n C:\Users\Your-User-Name\Documents\Caster`
9. Restart Dragon and the "Messages from Natlink" window should start with Dragon.

### Update Caster

1. Backup `%USERPROFILE%\Documents\Caster`
2. Delete `%USERPROFILE%\Documents\Caster`
3. Repeat Steps `1.- 4.` within the Caster install section

### Natlink Troubleshooting FAQ

3. Cannot load compatibility module support `(GUID = {dd990001-bb89-1d2-b031-0060088dc929}))` aka  **natlink.pyd**
  
    - Verify **Python 3.8.X 32-bit** is installed and 32bit **python is on path**
    - Verify  Dragon NaturallySpeaking version is v13-v15
2. _On non-administrator accounts_:
      - You may need to manually delete **natlink.pyd** as administrator after closing the CLI
      - Running terminal as administrator changes the user account causing a mismatch between user directories between administrator/non-administrator. This impacts where your settings are stored for natlink.
        - Fix:- [Create an OS environment variable](https://phoenixnap.com/kb/windows-set-environment-variable) **DICTATIONTOOLBOXUSER** pointing to a directory to store `.natlink`. 

### -Alternative Install - Natlink via GUI

The program **natlinkconfig**,  being the GUI version, can be launched from a PowerShell running as in elevated mode (Admin Privileges). After the `natlink.pyd` file has been registered and Natlink is enabled, further configuration can be done. Note: unfortunately, Vocola and Unimacro cannot be enabled for the time being.