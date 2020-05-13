# Bring Me

_Bring me_ is a set of commands that allow the user to quickly invoke an item from a list of previously-saved items. Currently, these items are: programs, websites, folders, and files. The list of items is saved to the Caster [user directory](https://caster-lexiconcode.readthedocs.io/en/documentation/readthedocs/User_Dir/Caster_User_Dir/)  in the file `settings/sm_bringme.toml`. On first installation, if no list of items exists yet, a default list of commands is created with documentation websites, common computer folders, and Caster Settings files. Say "bring me caster bring me" to bring up the `bringme.toml` file.

## Commands

- Add current element: `<target> to bring me as <key>`
    - `<target>` may be _website_, _program_, _folder_, or _file_. `key` is the phrase you wish to use to invoke it later. You can usually omit `<target>` and it will be detected automatically based on the context. If in a browser, `<target>` defaults to _website_ if omitted. If in File/Windows Explorer or a Save/Open dialog, `<target>` defaults to _file_ or _folder_ if omitted depending on which item is selected in the file list. Otherwise, `<target>` defaults to _program_ if omitted.
- Bring up the item: `bring me <item>`
    - For websites, this launches the default browser and opens the desired site.
    - This launches programs.
    - Folders are either opened or navigated to depending on the context. If in a terminal, File/Windows Explorer, or a Save/Open dialog the program will navigate to the folder.
        - Use `bring me <item> in <terminal_explorer>` to open in a new window. `<terminal_explorer>` can be _terminal_ or _explorer_.
    - Files are opened using the system-default program for that file type.
- Refresh bring me after editing `bringme.toml` directly: `refresh bring me`
- Remove a key: `remove <key> from bring me`
- Restore default keys: `restore bring me defaults`

## Examples

- _to bring me as **caster github**_
    - Automatically detected as a website if in the browser.
- _bring me **caster github**_
    - Opens the caster GitHub web page in your default browser.
- _**program** to bring me as **my favorite browser**_
    - If in Google Chrome, this saves Google Chrome as a program.
- _bring me **my favorite browser**_
    - Opens Google Chrome (after the user runs the previous example).
- _bring me **caster bring me**_
    - Opens `bringme.toml` in your system default `.toml` editor.
- _bring me **my documents**_
    - If in a terminal, File/Windows Explorer, or a Save/Open dialog, this navigates to your Documents folder. If not, this opens a new Explorer window at that folder.
- _bring me **caster user** in **terminal**_
    - Opens a new terminal at the user's `.caster` folder.
