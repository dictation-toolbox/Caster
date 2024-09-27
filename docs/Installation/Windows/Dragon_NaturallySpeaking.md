# Dragon NaturallySpeaking Install

**Install Dragon NaturallySpeaking** (DPI / DNS)- Caster only supports Dragon NaturallySpeaking v13-v16 and Windows 10 or higher. Natlink v16 is beta in Natlink.

After installing Dragon, you can configure the DNS settings based on your preference.

- Disabling the DNS Browser plug-ins due to instability of Internet browsers and DNS is recommended.
- Disable all the checkboxes in the “Correction” menu, except for the “Automatically add words to the active vocabulary” option.
    - Under the “Commands” menu check the “Require click to select…” checkboxes.  Otherwise you will find yourself accidentally clicking buttons or menu items instead of inserting text into your editor. I’ve disabled the other checkboxes in that menu as well.
- Set the “speed versus accuracy” slider in the “Miscellaneous” menu to a fairly high value.
- Uncheck the “Use the dictation box for unsupported applications” checkbox.

### Preinstall Natlink requirements

- DPI 16, 15, 14, 13 or derivative of the same version
- Download and install  [**Python 3.10.X 32 bit**](https://www.python.org/downloads/release/python-31011/) as `Windows x86 MSI installer` and **Optionally** select **add Python to Path**.
- Make sure any previous versions of Natlink are unregistered and uninstalled. (Dragon must be close during that process)

### Caster

1. Download Caster from the [master branch](https://github.com/dictation-toolbox/Caster/archive/master.zip).
2. Extract the files. You can put it anywhere but it is common to use `%USERPROFILE%\Documents\Caster-master`. The `Caster-master` could be renamed to `Caster`.
3. Install dependencies and set up Natlink by running `Caster-master/Install_Caster_DNS-WSR.bat`.
4. *Optional Step* for Caster's`Legion` MouseGrid - Legion Feature available on Windows 10 and above
    - The Legion MouseGrid requires [Microsoft Visual C++ Redistributable Packages for Visual Studio 2015, 2017 and 2019 (x86).](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist) 

### Install Natlink

1. Download the latest [Natlink](https://github.com/dictation-toolbox/natlink/releases)
   
   - Python 3.10.X 32 bit is required but does not need to be on path.
   - Do not uncheck the default `Py Launcher`

2. Run the Natlink Installer and a GUI should pop up at the end.
   
   - Note: After install natlink can be reconfigured Using `Configure Natlink via CLI` Natlink start menu.
   - **Optionally** install other Python packages via commandline with Natlink's python interpreter utilizing `Natlink Python Environment` 

3. Configure the Natlink GUI
   
   ![natlink_gui](https://raw.githubusercontent.com/dictation-toolbox/Caster/refs/heads/master/docs/images/natlink_gui.png)
   
   - **Optionally** Check the relevant project Dragonfly or Unimacro to configure the file path to the grammars.

4. Start Dragon start Dragon, the `Messages from Natlink` window should show loading a dragonfly script.  In the picture blow is an example loading module`_caster` is `_caster.py`.

   ![natlink_running](https://raw.githubusercontent.com/dictation-toolbox/Caster/refs/heads/master/docs/images/natlink_running.png)

Scrips starting with an underscore and ending in .py `_*.py` will be imported in alphabetical order, except `__init__.py` will be loaded first if it exists. 

### Update Caster

1. Backup `%USERPROFILE%\Documents\Caster`
2. Delete `%USERPROFILE%\Documents\Caster`
3. Repeat Steps `1.- 4.` within the Caster install section

### Natlink FAQ

1. Cannot load compatibility module support `(GUID = {dd990001-bb89-1d2-b031-0060088dc929}))` aka  **natlink.pyd**
    - Natlink failed to load go to https://github.com/dictation-toolbox/natlink for support.

#### How do I reconfigure Natlink after installation?

- After install natlink can be reconfigured Using `Configure Natlink via GUI` or `Configure Natlink via CLI` Natlink start menu.

#### How can I install other Python packages with Natlink?

- Natlink requires a specific Python interpreter. You can access the Python environment via `Natlink Python Environment` from the natlink start menu

#### Where are natlink configuration files located?

- The natlinkconfig_gui or natlinkconfig_cli creates configuration files in`%UserProfile%\.natlink` as `natlink.ini`.