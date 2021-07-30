# Alias Commands

## Creating Them

You can create commands on-the-fly by highlighting text on the screen and saying one of the following:

`"alias <something>"`

With the `alias` command, `<something>` is the spec of the new command you would like to create. For instance, if I highlight the word "create" in the previous sentence, then say `alias tiger`, then after that, if I say the word `tiger`, then the word "create" will be printed as text.

`chain alias <something>`

The `chain` version of alias commands will be incorporated into the active CCR set, meaning, they'll be chainable with the other active CCR commands.

For both types of alias commands, if you don't spec, a GUI box will pop up and ask for the spec name.

## Deleting Them

You can delete alias commands either by editing your `sm_aliases.toml` or `sm_chain_aliases.toml` file manually in caster [data user directory](https://caster.readthedocs.io/en/latest/readthedocs/User_Dir/Caster_User_Dir/) or by simply saying `delete aliases`. Doing the latter will wipe out both alias and chain aliases.

## Enabling Them

Aliases are enabled by default. After creating your first alias command, you can say `enable/disable aliases` to toggle the feature on and off. Aliases are a CCR module and work like the rest of the CCR modules in this regard.
