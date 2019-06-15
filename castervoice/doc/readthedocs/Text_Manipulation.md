# Text Manipulation and Navigation

Caster provides powerful text manipulation and navigation features. These functions are brand new, experimental, and subject to change (perhaps based on your feedback!).

## Common elements

- `direction` _sauce_ (up), _dunce_ (down), _lease_ (left) or _ross_ (right). Direction _must_ be included for all commands.
- `number_of_lines_to_search` is an integer number of lines to search for the target object. _sauce/lease_ searches up and _dunce/ross_ searches down. _sauce/dunce_ defaults to 3 lines if omitted and _lease/ross_ searches only the current line if omitted.
- `before_after` can be _before_ or _after_ and indicates whether the cursor should stop to the left (_before_) or the right (_after_) of the target object.
- `occurrence_number` can be _first_ through _ninth_ and indicates which occurrence of the target object you want, counting from the initial position of the cursor in the direction you specify.
- `target_object` can be a caster alphabet element (_arch, brov_ etc.), a caster punctuation element (_left prekris, deckle_ etc.), or arbitrary dictation (e.g. "punctuation element" spoken). Caster numbers are not yet supported.

## Commands

- Move the cursor: `(go | move) <direction> [<number_of_lines_to_search>] [<before_after>] [<occurrence_number>] <target_object>` 
- Selecting a single element: `grab <direction> [<number_of_lines_to_search>] [<occurrence_number>] <dictation>`
- Selecting from the cursor to a target: `grab <direction> [<number_of_lines_to_search>] until [<before_after>] [<occurrence_number>] <dictation>`
- Deleting a single element: `remove <direction> [<number_of_lines_to_search>] [<occurrence_number>] <dictation>`
- Deleting from the cursor to a target: `remove <direction> [<number_of_lines_to_search>] until [<before_after>] [<occurrence_number>] <dictation>`
- Replacing a single element: `replace <direction>  [<number_of_lines_to_search>] [<occurrence_number>] <target_object> with <replacement_object>`
    - Note: `<replacement_object>` must match the type of the `<target_object>`.

**Examples**:

- _go ross before deckle_
- _go ross after second deckle_
- _grab sauce five examples_
    - Seacrhes five lines up and selects the first occurrence of the word "examples" above the cursor.
- _grab sauce five until examples_
    - Seacrhes five lines up and selects from the cursor to the first occurrence of the word "examples" above the cursor.
- _remove sauce five examples_
    - Seacrhes five lines up and deletes the first occurrence of the word "examples" above the cursor.
- _remove sauce five until examples_
    - Seacrhes five lines up and deletes from the cursor to the first occurrence of the word "examples" above the cursor.

## Possible future features
Please feel free to try and implement these and submit a pull request!
- Selecting from one element to another element rather than having to move the cursor first (e.g. "grab sauce twenty from third left prekris to second right prekris").
- Replacing with Caster-formatted text (e.g. replace lease caster with gum caster)
- Selecting with Caster-formatted text (e.g. replace lease tie caster with gum caster)
- Very powerful selection and replacement using Caster-style typing (e.g. replace lease tie caster minus gum style ace gum typing with tie caster minus laws formatted text)
