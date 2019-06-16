# Text Manipulation and Navigation

Caster provides powerful text manipulation and navigation features. These functions are brand new, experimental, and subject to change (perhaps based on your feedback!). We encourage contributions; please discuss your ideas [here](https://github.com/dictation-toolbox/Caster/issues/579). These commands are "CCR" so are able to be combined with other CCR commands. Enable these commands by saying "Enable text manipulation".

## Common elements

- `direction` _sauce_ (up), _dunce_ (down), _lease_ (left) or _ross_ (right). Direction _must_ be included for all commands.
- `number_of_lines_to_search` is an integer number of lines to search for the target object. _sauce/lease_ searches up and _dunce/ross_ searches down. _sauce/dunce_ defaults to 3 lines if omitted and _lease/ross_ defaults to searching only the current line.
- `before_after` can be _before_ or _after_ and indicates whether the cursor should stop to the left (_before_) or the right (_after_) of the target object. Defaults for `before_after` depend on which command is being used. For the "go" commands, `before_after` defaults to whichever one is closer to the cursor. More explicitly, for "go", _ross/dunce_ defaults to _before_ and _lease/sauce_ defaults to _after_.  By contrast, for the "grab until" and "remove until" commands it defaults to the one that is farther (i.e. it selects or removes all the way through the target object). More explicitly, for "grab/remove until", _ross/dunce_ defaults to _after_ and _lease/sauce_ defaults to _before_. 
- `occurrence_number` can be _first_ through _ninth_ and indicates which occurrence of the target object you want, counting from the initial position of the cursor in the direction you specify. Defaults to _first_.
- `target_object` can be a Caster alphabet element (_arch, brov_ etc.), a Caster punctuation element (_left prekris, deckle_ etc.), or arbitrary dictation (e.g. "punctuation element" spoken). Caster numbers are not yet supported.

## Commands

- Move the cursor: `(go | move) <direction> [<number_of_lines_to_search>] [<before_after>] [<occurrence_number>] <target_object>` 
- Selecting a single element: `grab <direction> [<number_of_lines_to_search>] [<occurrence_number>] <dictation>`
- Selecting from the cursor to a target: `grab <direction> [<number_of_lines_to_search>] until [<before_after>] [<occurrence_number>] <dictation>`
- Deleting a single element: `remove <direction> [<number_of_lines_to_search>] [<occurrence_number>] <dictation>`
- Deleting from the cursor to a target: `remove <direction> [<number_of_lines_to_search>] until [<before_after>] [<occurrence_number>] <dictation>`
- Replacing a single element: `replace <direction>  [<number_of_lines_to_search>] [<occurrence_number>] <target_object> with <replacement_object>`
    - Note: `<replacement_object>` must be dictation if `<target_object>` is dictation. As in, you can't yet replace dictation with a Caster alphabet element.

**Examples**:

- _go ross before deckle_
- _go ross after second deckle_
- _grab sauce five examples_
    - Searches five lines up and selects the first occurrence of the word "examples" above the cursor.
- _grab sauce five until examples_
    - Searches five lines up and selects from the cursor to the first occurrence of the word "examples" above the cursor.
- _grab ross hello hug quotes_
    - select the nearest occurrence of "hello" (to the right of the cursor on the current line) and surround it by quotes.
    - _hug quotes_ is actually a separate command not part of this module, but you can do this because these commands are CCR.
- _remove sauce five examples_
    - Searches five lines up and deletes the first occurrence of the word "examples" above the cursor.
- _remove sauce five until examples_
    - Searches five lines up and deletes from the cursor to the first occurrence of the word "examples" above the cursor.

## Possible future features
Please feel free to try and implement these and submit a pull request!

- Supporting Caster numbers as targets (e.g. _go lease before numb one_).
- Selecting from one element to another element rather than having to move the cursor first (e.g. _grab sauce twenty from third left prekris to second right prekris_).
- Replacing with Caster-formatted text (e.g. _replace lease caster with gum caster_).
- Selecting with Caster-formatted text (e.g. _grab lease tie caster_).
- Very powerful selection and replacement using Caster-style typing (e.g. _replace lease tie caster minus gum style ace gum typing with tie caster minus laws formatted text_).
- Quick format switching (e.g. _switch lease [format of] very powerful to snake_).
- Limit dictation recognition to only elements that are there. Currently, the voice recognition software provides its best guess at what you mean, rather than Caster limiting the options to what is in the selection.
- Use line numbers as location limiters (e.g. go line one fifty nine third right prekris).

## Known bugs/issues
- Report bugs and discuss solutions [here](https://github.com/dictation-toolbox/Caster/issues/579).
- In some applications, the keypress speed is slow such that the cursor takes a long time to move to the desired location (seems to be application dependent).
- Currently, using _sauce/dunce_ includes the current line in the search (it shouldn't) and _lease/ross_ allows the user to specify a number of lines to search over (it should only search the current line). To fix this, we would need to adjust the regex for the case when _sauce/dunce_ is specified so that it only matches when it sees a new line character before (for _dunce_) or after (for _sauce_) the target object. The regex is located in the function `select_text_and_return_it` in the file `text_manipulation_functions.py`.
- Words within a multiword camel case phrase will be ignored, the regex (see above) needs to be adjusted to fix this. 
- In some situations (possibly only when selecting towards the left), if you have two of the same word directly in a row, the regex not match the nearest occurrence but rather start by matching the second nearest one. The regex (see above) needs to be adjusted to fix this (I don't know how).
- Occasionally the command parameters (e.g. `occurrence_number` or `before_after`) are interpreted as dictation since the parameters are optional. For example, if you say "go ross after hello", once in a while it will think you are searching for the phrase "after hello" and so won't work in which case it would print in the Natlink window "'after hello' not found". I don't understand what determines when this happens and when it doesn't.
- There is some duplication in the code. It would be great if a python expert was able to help us tidy the code up a bit.
- These commands are unreliable in Microsoft Word. You will want to [disable smart selection](https://superuser.com/questions/962710/how-to-make-microsoft-word-selection-behave-like-it-would-in-a-plain-text-editor) and [cursor animation](https://www.404techsupport.com/2012/11/07/disable-cursor-animation-word-2013/) for use there. You can also try adjusting the pause times (see below). However, you are probably better off using Dragon's native commands in Microsoft Word. Those commands have some advantages and disadvantages relative to Caster's.
- In RStudio, the underlying Ace text editor automatically navigates through double spaces with a single arrow key press. This feature causes these functions to fail. An RStudio [issue](https://github.com/rstudio/rstudio/issues/4934) is open.
- Emacs is not supported yet. The reason is that Emacs has unusual cursor/selection behavior, see [here](https://www.gnu.org/software/emacs/manual/html_node/eintr/Point-and-mark.html) and [here](https://www.gnu.org/software/emacs/manual/html_node/emacs/Mark-Ring.html) . The functions in text_manipulation_functions.py take an `application` parameter , so one would just need to make an if statement `if application == emacs:` in some the functions such as `select_text_and_return_it` to account for Emacs cursor/selection behavior. Application parameters need to be added into the dictionary `contexts` at the top of the file.
- Although these commands do not affect what is on the first slot of the clipboard, they do sometimes affect what is on the second or third slot of the clipboard if you are using a clipboard with multiple slots. (The multi-clipboard on Windows 10 can be accessed by pressing Windows-V.) In particular, the text that the command selects will typically be added onto the second slot of the clipboard by the function `read_selected_without_altering_clipboard`. Sometimes the function `paste_string_without_altering_clipboard` causes a similar problem. It is possible that this issue could be solved by tweaking those functions (I don't totally understand how they work, though I know they use pyperclip). If not, it might be worth looking into a third-party clipboard manager such as CopyQ, which appears to be quite sophisticated and apparently supports python scripting.
- Sometimes these commands don't work properly in certain apps because those apps take a very long time for text to be added into the clipboard after pressing Ctrl-C. The current solution is to have a dictionary called `copy_pause_time_dict` that lets the user set different pause times (for after pressing Ctrl-C) for different apps. (`copy_pause_time_dict` and the other dictionaries described here are in `text_manipulation_functions.py` for now). In order to add a custom pause time for an application, the user must first add that application into the dictionary `contexts`.
    - In the future, a better solution might be the following:  if the text that is passed into the function is the same as what was on the clipboard before, then have the command try copying again (with an increased pause time afterwards). The tools for doing something like this alternative solution are already available in caster's `lib/context.py`, see for example the function `read_nmax_tries` and the parameter `same_is_okay` in the function `read_selected_without_altering_clipboard`. One problem with this solution seems to be that sometimes you might want to use the commands on the same text multiple times in a row (e.g. for moving the cursor) in which case what was on the first slot of the clipboard wouldn't change so the command would try to copy again unnecessarily. That problem could possibly be avoided by adjusting the function `read_selected_without_altering_clipboard`. 
    - In addition to the `copy_pause_time_dict`, there is also a dictionary called `paste_pause_time_dict` that adjusts the pause time between putting text onto the clipboard and pressing `Ctrl-V`, since this seems (but not totally sure) to be application dependent.
