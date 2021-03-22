# User Directory

This provides a brief overview of the Caster user directory. The main function of the user directory is to store Caster settings and user-made content. 

*Note for Dragon users*: The Caster User directory is managed by Caster, and should not be confused with Natlink's UserDirectory, which is set to the Caster source code directory if using the [Alternative Natlink Configuration](../Installation/Dragon_NaturallySpeaking.md/#-alternative-natlink-configuration).

## User Directory Location

The default locations are:

- Windows: `C:\Users\%USERNAME%\AppData\Local\caster`
- Linux and MacOS: `~/.local/share/caster`

Users can set the location of their Caster user directory using the environment variable `CASTER_USER_DIR`. For help on setting environment variables on your system, search for "setting environment variables <_your OS_>".

### Layout  Description

- `data` - Caster stores the files that are not intended to be edited by the user in the `data` directory. Most files here are for self-modifying rules, such as [Alias](../Caster_Commands/Alias.md), and start with `sm_`.
- `hooks` - For user-made [hooks](https://caster.readthedocs.io/en/latest/readthedocs/Caster_Settings/hooks/) (Empty by default).
- `rules` - For user-made [rules](https://caster.readthedocs.io/en/latest/readthedocs/Caster_Settings/rules/) and overrides of rules from Caster (Empty by default).
- `settings` - All Caster [settings](https://caster.readthedocs.io/en/latest/readthedocs/Caster_Settings/settings/) files.
- `sikuli` - For user-made [Sikuli](https://caster.readthedocs.io/en/latest/readthedocs/Third-party_Integrations/Sikuli/) scripts (Empty by default).
- `transformers` - For [simplified transformers](https://caster.readthedocs.io/en/latest/readthedocs/Customize_Caster/Customizing_Starter_Rules/#use-simplified-transformers) i.e words.txt (Empty by default).

### Backup Procedures

It's good to back up this directory as it contains user content. The backup scheme can be simple as a zip file, cloud-backup service (e.g. Dropbox), or even a private GitHub repository. The simplest solution for most users will be to use the environment variable `CASTER_USER_DIR` to place the user directory inside your cloud-backup folder. Note that on many Windows setups the full user directory is already backed up by default using OneDrive. 

Another alternative is to use hard links to a folder in your cloud-backup folder. Hard links provide the ability to keep a single copy of a file yet have it appear in multiple directories. There is a helpful utility that makes these hard links easy to use on Windows OS. See [Hard Link Shell Extension](https://schinagl.priv.at/nt/hardlinkshellext/linkshellextension.html).
