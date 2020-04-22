## User Directory

This provides a brief overview of the caster user directory. The main function of the user directory is to store Caster settings and user-made content. 

**User Directory Location**

Windows  OS `C:\Users\%USERNAME%\AppData\Local\caster`

At this point setup should be complete and engine agnostic.

*DNS/DPI*: The Caster User directory is managed by Caster, and should not be confused with Natlink's UserDirectory, which is set to the Caster source code directory if using the [Alternative Natlink Configuration](https://caster.readthedocs.io/en/latest/readthedocs/Installation/Dragon_NaturallySpeaking/#-alternative-natlink-configuration).

**Layout  Description**

1. `data` - Caster stores the data files that are not meant to be edited by the end user explicitly in the data directory. Most data toml files are for SelfModifying rules starting with `sm_`.
2. `hooks` - User-made hooks are placed (Empty by default)
3. `rules` - User-made rules and "Caster starter rules" overrides (Empty by default)
4. `settings` - All Caster related settings file
5. `sikuli` - User-made sikuli scripts (Empty by default)
6. `transformers` - Used for simplified transformers i.e words.txt (Empty by default)

### Backup Procedures

It's good to back up this directory as it contains user content. The backup scheme can be simple as a zip file, Cloud backup service i.e. Dropbox, or even a private GitHub repository.

- You can utilize hard links. Hardlinks provide the ability to keep a single copy of a file yet have it appear in multiple directories.
  - There is a helpful utility that makes these Hardlinks easy to use Windows OS. [Hard Link Shell Extension](https://schinagl.priv.at/nt/hardlinkshellext/linkshellextension.html) 

