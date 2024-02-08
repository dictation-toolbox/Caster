# Hooks

This allows you to turn off certain Caster features.  Setting a hook to `true` or `False` in `hooks.toml` changes if the hook runs when Caster starts. Hooks can be temporarily `Disabled` and `Enabled`  by voice while Caster is running which does not altar settings in `hooks.toml`. Toggling typically uses the hook name unless noted otherwise.

Say `Enable <hook name>` activate a hook.

### Types of Hooks

1. Formatting Hook

   The Formatting Hook prints out to the status window when changes are made to Caster's formatting commands, such as the `set format  <Spacing> <Capitallization> bow` command.

   Example command

   `set format tie snake bow`

   Example Legend

   - snake - words_with_underscores
   - tie - TitleCase

2. Printer Hook (Enabled by Default)

   The Formatting Hook prints out to the status window when rules are enabled or disabled. `Enable  <Rule name>`

   Command example

   Say `Enable Firefox`

   `The rule FirefoxRule was set to active.`

3. Show Status Window On Error Hook

   Say `Enable show On Error Hook`

   When Caster encounters an error, the status window is brought to the forefront. This allows you to see the error message. 

   - Currently this is only implemented when rules reload with an error.

```toml
# hooks.toml example file
FormattingHook = false
PrinterHook = true
ShowStatusWindowOnErrorHook = false
```

------

Learn more about creating your own hooks and events in the **Customize Caster** documentation.
