# Windows Speech Recognition - Classic Install

Caster currently supports Windows Speech Recognition (WSR) on Microsoft Windows 7 through Windows 10.

## 1. Python

- **First** Download and install [Python v2.7.18 64-bit](https://www.python.org/downloads/release/python-2718/) listed as `Windows x86-64 MSI installer` not Python 3.

      - Make sure to select `Add python to path`. This can be done manually by searching for "edit environment variables for your account" and adding your Python folder to the list of Path values.

## 2. Caster

   1. Download Caster from the [master branch](https://github.com/dictation-toolbox/Caster/archive/master.zip).
   2. Open up the zip file downloaded
   3. Copy the contents of `Caster-master` folder, you can put it anywhere but it is common to use `%USERPROFILE%\Documents\Caster`.
   4. *Optional Step* for Caster's`Legion` MouseGrid - Legion Feature available on Windows 8 and above
         - The Legion MouseGrid requires [Microsoft Visual C++ Redistributable Packages for Visual Studio 2015, 2017 and 2019 (x86).](https://support.microsoft.com/en-nz/help/2977003/the-latest-supported-visual-c-downloads) Note: Should not be needed if Windows 10 is up-to-date.
   5. Click `Install_Caster_DNS-WSR.bat` to install prerequisite Caster dependencies.  

## 4. Launch Caster for Classic Install

   1. Go to  `%USERPROFILE%\Documents\Caster`

   2. Start Caster by double clicking on `Start_Caster_WSR.py`.

   3. To test open Window's Notepad, try saying `arch brov char delta` producing `abcd` text. Set up complete!

## Update Caster

   1. Backup `%USERPROFILE%\Documents\Caster`
   2. Delete `%USERPROFILE%\Documents\Caster`
   3. Repeat Steps `1. - 4.` within the Caster install section

------

### Troubleshooting Windows Speech Recognition

Receive the `-2147352567` COM error when Caster starts. This is most likely related to the microphone being utilized by another program. See [issue #821](https://github.com/dictation-toolbox/Caster/issues/821) and [#68](https://github.com/dictation-toolbox/Caster/issues/68).  This can be mitigated by closing the program that's utilizing the microphone.

   > com_error: (-2147352567, 'Exception occurred.', (0, None, None, None, 0, -2004287480), None)`
  