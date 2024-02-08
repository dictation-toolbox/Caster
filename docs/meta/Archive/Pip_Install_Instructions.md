# PIP Install  (Alpha)  -  Not fully implemented

If you're using DNS make sure you've installed and configured NatLink first! Open [command prompt](https://www.wikihow.com/Open-the-Command-Prompt-in-Windows) (CMD) and type the following then press enter.

`pip install castervoice`

At the end of the PIP install instructions a CMD window will guide you of what to expect for WSR or DNS. Setup complete. **Note** If a window does not appear please refer to the troubleshooting section.  

**PIP install Troubleshooting**

You have followed the PIP install `pip install castervoice` CMD window does not provide instructions during install. Caster does not start with DNS automatically or `start_caster.py` does not appear on the desktop for WSR.

- Look for `CasterInstall.log` on your desktop to check for error messages.
- The PIP install is in beta yet please report any issues or error messages that you experience github [issues](https://github.com/dictation-toolbox/Caster/issues) or [gitter chat](https://gitter.im/synkarius/Caster?utm_source=share-link&utm_medium=link&utm_campaign=share-link). 

**Launch Caster Troubleshooting - PIP install variant**

For WRS double clicking on `_caster.py` or `start_caster.py` opens the file and does not launch Caster. 
**Note** Depending on your file associations it may launch an editor instead of running the file. Run the file using CMD. Detailed instructions below.

1. Change the directory to  `Desktop` in CMD.
   Example PIP `cd C:\Users\<YourUsername>\Desktop` or Classic `cd C:\Users\<YourUsername>\Documents\Caster`
2. Then Classic:`python _caster.py` or PIP: `python start_caster.py`
