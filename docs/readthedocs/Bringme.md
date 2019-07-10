# Bring me

_Bring me_ is a function that allows the user to quickly invoke an item from a list of previously saved items. Currently these items are: programs, websites, folders, and files. The list of items is saved to the Caster user directory to the file bringme.toml. On first installation, if no list of items exists yet, default list is created with some documentation websites, common computer folders and some Caster settings files.

`<launch> to bring me as <key>`: adds current element, which may be a website, program, folder, or file, to the list of items to be able to invoke it later by uttering `key`

`to bring me as <key>`: same as above, but the "launch" is detected automatically, based on if you are in a web browser, Windows Explorer, or the terminal

`bring me <item>` : brings up the `item` in a way dependent on the type of the item. It can be:

- a website: launches the default system browser opening the desired site
- a program: launches the program
- a folder: opens the desired folder; if `in terminal` or `in explorer` is appended, opens the folder explicitly in this. Default is opening in the Windows Explorer.
- a file: opens the file with its default associated program

`refresh bring me`: refreshes the bring me grammar and synchronizes it with its settings. This is useful if you edit the bringme.toml file directly.

`remove <key> from bring me`: removes the utterance `key` from the list of items to launch
            "restore bring me defaults": R(Function(self.bring_restore)),

`restore bring me defaults`: clears the list of items and restores its default values

## Example

When in Google Chrome, saying "program to bring me as my favorite browser" saves Google Chrome as a program, which can be launched by saying "bring me my favorite browser".

When in a browser (currently Google Chrome and Firefox are supported), saying "Website to bring me as my little pony" will save the current website so that it can be brought up later by saying "my little pony" in a new tab, if the default system browser is already running, or in a new browser window.