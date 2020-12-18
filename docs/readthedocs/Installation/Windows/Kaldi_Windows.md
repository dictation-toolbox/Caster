# Kaldi - Classic Install

Caster currently supports Kaldi on Microsoft Windows 7 through Windows 10. Consider supporting the author [daanzu](https://github.com/sponsors/daanzu) if you use his engine full-time.

## 1. Python

- First Download and install [Python v2.7.18 64-bit](https://www.python.org/downloads/release/python-2718/) or [Python 3](https://www.python.org/downloads/release/python-381/) listed as `Windows x86-64 MSI installer`.

    Make sure to select `Add python to path`. This can be done manually by searching for "edit environment variables for your account" and adding your Python27 or Python 3 folder to the list of Path values.

    Be sure the `wheel` package is installed. It can be installed with `pip install wheel` on a command line. You may need to update pip by running `pip install --upgrade pip` first.

## 2. Caster

1. Download Caster from the [master branch](https://github.com/dictation-toolbox/Caster/archive/master.zip).
2. Open up the zip file downloaded
3. Copy the contents of `Caster-master` folder. You can put it anywhere, but it is common to use `%USERPROFILE%\Documents\Caster`.
4. *Optional Step* for Caster's`Legion` MouseGrid - Legion Feature available on Windows 8 and above.
    - The Legion MouseGrid requires [Microsoft Visual C++ Redistributable Packages for Visual Studio 2015, 2017 and 2019 (x86).](https://support.microsoft.com/en-nz/help/2977003/the-latest-supported-visual-c-downloads) Note: Should not be needed if Windows 10 is up-to-date.
5. Click `Install_Caster_Kaldi.bat` to install prerequisite dependencies and set up Kaldi. 

## 3. Set up Kaldi Model

1. Download your preferred Kaldi model at [kaldi-active-grammar/releases](https://github.com/daanzu/kaldi-active-grammar/releases)
2. Extract `kaldi_model_< Model Type >.zip` to  `%USERPROFILE%\Documents\Caster`

## 4. Launch for Kaldi  for Classic Install.

1. Go to `%USERPROFILE%\Documents\Caster`
2. Double-click on `Run_Caster_Kaldi.bat`

**Note:**  Kaldi is flexible engine which can be configured via engine parameters to customize your experience. 

- You can modify the `Run_Caster_Kaldi.bat` file for  `python -m dragonfly load _*.py --engine kaldi --no-recobs-messages --engine-options "model_dir=kaldi_model, vad_padding_end_ms=300"`
- List of kaldi [engine parameters](https://dragonfly2.readthedocs.io/en/latest/kaldi_engine.html#engine-configuration). Scroll down for parameter explanations.

### Update Caster

1. Backup `%USERPROFILE%\Documents\Caster`
2. Delete `%USERPROFILE%\Documents\Caster`
3. Repeat Steps `1. - 5.` within the Caster install section

------

**Troubleshooting Kaldi**

- No commonly reported issues yet.

**Known Issues**

- None
