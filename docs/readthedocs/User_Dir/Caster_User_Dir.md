## User Directory

This provides a brief overview of the Caster user directory. The main function of the user directory is to store Caster settings and user-made content. 

**User Directory Location**

The default locations are:

Windows: `C:\Users\%USERNAME%\AppData\Local\caster`
Linux and MacOS: `~/.local/share/caster`

Users can set the location of their Caster user directory using the environment variable `CASTER_USER_DIR`. For help on setting environment variables on your system, search for "setting environment variables <_your OS_>".

*DNS/DPI*: The Caster User directory is managed by Caster, and should not be confused with Natlink's UserDirectory, which is set to the Caster source code directory if using the [Alternative Natlink Configuration](../Installation/Dragon_NaturallySpeaking/#alternative-natlink-configuration).

**Layout  Description**

1. `data` - Caster stores the files that are not intended to be edited by the user in the `data` directory. Most data `toml` files are for self-modifying rules, such as [Alias](Caster_Commands/Alias), and start with `sm_`.
2. `hooks` - For user-made [hooks](../Caster_Settings/hooks) (Empty by default)
3. `rules` - For user-made [rules](../Caster_Settings/rules) and overrides of rules from Caster (Empty by default)
4. `settings` - All Caster [settings](../Caster_Settings/settings) files
5. `sikuli` - For user-made [Sikuli](../Third-party_Integrations/Sikuli) scripts (Empty by default)
6. `transformers` - For [simplified transformers](../Customize_Caster/Customizing_Starter_Rules/#use-simplified-transformers) i.e words.txt (Empty by default)

### Backup Procedures

It's good to back up this directory as it contains user content. The backup scheme can be simple as a zip file, Cloud backup service i.e. Dropbox, or even a private GitHub repository.

- You can utilize hard links. Hardlinks provide the ability to keep a single copy of a file yet have it appear in multiple directories.
  - There is a helpful utility that makes these Hardlinks easy to use Windows OS. [Hard Link Shell Extension](https://schinagl.priv.at/nt/hardlinkshellext/linkshellextension.html) 

