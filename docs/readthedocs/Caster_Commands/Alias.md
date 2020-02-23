# Alias Commands

## Creating Them

You can create commands on-the-fly by highlighting text on the screen and saying one of the following.

`"alias <something>"`

With the `alias` command, `<something>` is the spec of the new command you would like to create. For instance, if I highlight the word "create" in the previous sentence, then say `alias tiger`, then after that, if I say the word `tiger`, then the word "create" will be printed. If you don't speak the `alias <command>`  a box will pop up and ask command name.

`chain alias <something>`

There are two differences with the `chain` version of the `alias` command. The second is that commands created with the `chain` version will be incorporated into the active CCR set, meaning, they'll be chainable with the other active CCR commands.

## Deleting Them

You can delete alias commands either by editing your `sm_aliases.toml` or `sm_chain_aliases.toml `file manually, or by simply saying `delete aliases`. Doing the latter will wipe out both alias and chain aliases.

## Enabling Them

Aliases are not enabled by default. After creating your first alias command, you'll have to say `enable aliases` Aliases are a CCR module, and work like the rest of the CCR modules in this regard.