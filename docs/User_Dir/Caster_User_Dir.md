# User Directory

This provides a brief overview of the Caster user directory. The main function of the user directory is to store Caster settings and user-made content. 


## User Directory Location

The default locations are:

- Windows: `C:\Users\%USERNAME%\AppData\Local\caster`
- Linux and MacOS: `~/.local/share/caster`

Users can set the location of their Caster user directory using the environment variable `CASTER_USER_DIR`. For help on setting environment variables on your system, search for "setting environment variables <_your OS_>".

### Layout  Description

- `data` - Caster stores the files that are not intended to be edited by the user in the `data` directory. Most files here are for self-modifying rules, such as [Alias](https://dictation-toolbox.github.io/Caster/#/Caster_Commands/Alias), and start with `sm_`.
- `caster_user_content\hooks` - For user-made [hooks](https://dictation-toolbox.github.io/Caster/#/Caster_Settings/hooks) (Empty by default).
- `caster_user_content\rules` - For user-made [rules](https://dictation-toolbox.github.io/Caster/#/Caster_Settings/rules) and overrides of rules from Caster (Empty by default).
- `settings` - All Caster [settings](https://dictation-toolbox.github.io/Caster/#/Caster_Settings/settings) files.
- `sikuli` - For user-made [Sikuli](https://dictation-toolbox.github.io/Caster/#/Third-party_Integrations/Sikuli) scripts (Empty by default).
- `caster_user_content\transformers` - For [simplified transformers](https://dictation-toolbox.github.io/Caster/#/Customize_Caster/Customizing_Starter_Rules?id=use-simplified-transformers) i.e words.txt (Empty by default).

### Backup Procedures

It's good to back up this directory as it contains user content. The backup scheme can be simple as a zip file, cloud-backup service (e.g. Dropbox), or even a private GitHub repository. The simplest solution for most users will be to use the environment variable `CASTER_USER_DIR` to place the user directory inside your cloud-backup folder. Note that on many Windows setups the full user directory is already backed up by default using OneDrive. 

Another alternative is to use hard links to a folder in your cloud-backup folder. Hard links provide the ability to keep a single copy of a file yet have it appear in multiple directories. There is a helpful utility that makes these hard links easy to use on Windows OS. See [Hard Link Shell Extension](https://schinagl.priv.at/nt/hardlinkshellext/linkshellextension.html).
