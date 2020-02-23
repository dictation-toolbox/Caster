## User Directory

This provides a brief overview caster user directory. The main function of the user directory is to store Caster settings and user made content. 

1. `data` - Caster stores it's data files that are not meant to be editedby the end user explicitly in the data directory. 
    Most data toml files are for SelfModifying rules starting with `sm_`. Files include:

  ​	`sm_aliases.toml` # alias command
  ​	`sm_chain_aliases.toml` # chain alias command
  ​	`sm_css_tree.toml`  # noderule css grammar data
  ​	`sm_history.toml` # record from history feature
  ​	`sm_bringme.toml` # bring me feature
  ​	`clipboard.json` #  multi clipboard data

2. `hooks` - User made hooks are placed
     Empty by default
3. `rules` - User made rules and caster rule starter rules overrides
    Empty by default
4. `settings` - All Caster related settings file
    See details
5. `sikuli` - User made sikuli Scripts
    Empty by default
6. `transformers` - Used for simplified transformers i.e words.txt
    Empty by default

### Backup Procedures

It's good to back up this directory as it contains user content.
The backup scheme can be simple as a zip file, Cloud backup service i.e. Dropbox, or even a private GitHub repository.

- You can utilize `hard links`. Hardlinks provide the ability to keep a single copy of a file yet have it appear in multiple folders (directories).
  - There is a helpful utility that makes these Hardlinks easy to use Windows OS. [Hard Link Shell Extension](https://schinagl.priv.at/nt/hardlinkshellext/linkshellextension.html) 

