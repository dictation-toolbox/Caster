# Windows Speech Recognition - Classic Install

Caster currently supports Windows Speech Recognition (WSR) on Microsoft Windows 7 through Windows 10.

### 1. Python

- **First** Download and install [Python v2.7.17 64-bit](https://www.python.org/downloads/release/python-2717/) listed as `Windows x86-64 MSI installer` not Python 3.

Make sure to select `Add python to path`. This can be done manually by searching for "edit environment variables for your account" and adding your Python27 folder to the list of Path values.

### 2. Caster

1. Download Caster from the [master branch](https://github.com/dictation-toolbox/Caster/archive/master.zip).
2. Open up the zip file downloaded
3. Copy the contents of `Caster-master` folder, you can put it anywhere but it is common to use `%USERPROFILE%\Documents\Caster`.
4. *Optional Step* for Caster's`Legion` MouseGrid - Legion Feature available on Windows 8 and above
   - The Legion MouseGrid requires [Microsoft Visual C++ Redistributable Packages for Visual Studio 2015, 2017 and 2019 (x86).](https://support.microsoft.com/en-nz/help/2977003/the-latest-supported-visual-c-downloads) Note: Should not be needed if Windows 10 is up-to-date.
5. Click `Install_Caster_DNS-WSR.bat` to install prerequisite Caster dependencies.  **Note** that for this to work correctly Python must be installed to `C:/Python27`

### 4. Launch  Caster for Classic Install.

1. Go to  `%USERPROFILE%\Documents\Caster`

2. Start caster by double clicking on `Start_Caster_WSR.py`. 

3. To test open Window's Notepad and try saying `arch brov char delta` producing `abcd` text. Set up complete!


### Update Caster
  1. Backup `%USERPROFILE%\Documents\Caster`
  2. Delete `%USERPROFILE%\Documents\Caster`
  3. Repeat Steps 1. - 4. in `2. Caster`
------

   **Troubleshooting Windows Speech Recognition**

- For WRS double clicking on `Start_Caster_WSR.py` opens the file and does not launch Caster. 
  **Note** Depending on your file associations it may launch an editor instead of running the file. Run the file using CMD. Detailed instructions below.
  1. Change the directory to ` Caster` install location in CMD.
     Example `cd C:\Users\<YourUsername>\Documents\Caster`
  2. To start `python Start_Caster_WSR.py`

