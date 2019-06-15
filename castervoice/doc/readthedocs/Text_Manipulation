# Text Manipulation and Navigation

Caster provides powerful text manipulation and navigation features. These functions are brand new, experimental, and subject to change (perhaps based on your feedback!).

## Common elements

- `direction` _sauce_ (up), _dunce_ (down), _lease_ (left) and _ross_ (right) and _must_ be included for all commands.
- `before_after` can be _before_ or _after_ and indicates whether the cursor should stop to the left (_before_) or the right (_after_) of the target object.
- `occurrence_number` can be _first_ through _ninth_ and indicates which occurrence of the target object you want, counting from the initial position of the cursor in the direction you specify.
- `target_object` can be a caster alphabet element (_arch, brov_ etc.), a caster punctuation element (_left prekris, deckle_ etc.), or arbitrary dictation (e.g. "punctuation element" spoken).

### Commands

- Move the cursor: `(go | move) <direction> [<number_of_lines_to_search>] [<before_after>] [<occurrence_number>] <target_object>` 
- Selecting a single element: `grab <direction> [<number_of_lines_to_search>] [<occurrence_number>] <dictation>`
- Selecting from the cursor to a target: `grab <direction> [<number_of_lines_to_search>] until [<before_after>] [<occurrence_number>] <dictation>`
- Selecting a single element: `grab <direction> [<number_of_lines_to_search>] [<occurrence_number>] <dictation>`
- Selecting from the cursor to a target: `grab <direction> [<number_of_lines_to_search>] until [<before_after>] [<occurrence_number>] <dictation>`
- Left click: `kick`
- Right click: `psychic`

### Moving

- Move around: `curse <direction> [[E] <direction>] <distance_in_pixel>`  
  _direction_ can be _sauce_ (up), _dunce_ (down), _lease_ (left) and _ross_ (right).

**Examples**:

- _curse sauce ten_
- _curse lease sauce ten_
- _curse lease-e-sauce ten_ - Easier to speak than the example above.

## Advanced mouse commands

### Mousegrid

**Description**:

Approach the desired position by recursively selecting tiles on the screen. Provided by Dragon Naturally Speaking.

**Usage**:

- Evoke: `mousegrid`
- Select tile: `<tile_number>`  
  _tile_number_ can be anything from 1 to 9.

### Douglas

**Description**:

Creates a grid on the screen with horizontal (top of screen) and vertical (left of screen) numbers at the borders. Squares are directly selectable by calling out the respective numbers. 

Selecting from one point to another is available including fine adjustment of the start and end points.

**Usage**:

- Evoke: `douglas` or `douglas <monitor_number>`
- Move to square: `<horizontal_number> by <vertical_number>`
- Select: `<horizontal_number_1> by <vertical_number_1> select <horizontal_number_2> by <vertical_number_2>`
- Select horizontally: `<horizontal_number_1> by <vertical_number_1> select <horizontal_number_2>`
- Fine selection: `<horizontal_number_1> by <vertical_number_1> move` &rightarrow; `curse ...` &rightarrow; `point one` &rightarrow; `<horizontal_number_2> by <vertical_number_2> move` &rightarrow; `curse ...` &rightarrow; `point two` &rightarrow; `select`

**Examples**:

- _5 by 20_
- _5 by 20 kick_
- _5 by 20 select 10 by 30_
- _5 by 20 select 10_
- _5 by 20 move, curse sauce lease 5, point one, 10 by 30 move, curse dunce lease 10, point two, select_

### Rainbow

**Description**:

- Creates a colored grid on the screen. Squares are directly selectable by calling out the respective color then number.

**Usage**:

- Evoke: `rainbow` or `rainbow <monitor_number>` 
- Move to square: `[<number_of_color_palette>] <color> <number>`  
  _number_of_color_palette_ refers to the fact that colors loop when filling the screen.  
  _color_ can be replaced by the following colors: _red_, _orange_, _yellow_, _green_, _blue_, _purple_.
- Select: `[<number_of_color_palette_1>] <color_1> <number_1>` select `[<number_of_color_palette_2>] <color_2> <number_2>`
- Fine selection: `[<number_of_color_palette_1>] <color_1> <number_1> move` &rightarrow; `curse ...` &rightarrow; `point one` &rightarrow; `[<number_of_color_palette_2>] <color_2> <number_2> move` &rightarrow; `curse ...` &rightarrow; `point two` &rightarrow; `select`

**Examples**:

- _red 86_: - References square within the first red palette.
- _red 86 kick_: - Clicks at this location.
- _two red 86_ - References square within the second red palette.
- _red 86 select 2 green 10_: - Selects from the first red 86 to the second green 10.
- _red 86, curse sauce lease 5, point one, select 2 green 10, curse dunce lease 10, point two, select_: - Selects from the first red 86 to the second green 10 with fine adjustment.

### Legion

**Description**:

- Finds text on the screen and gives each a number which you can call out.

**Usage**:

- Evoke: `legion or legion [monitor_number]`
- Move to text area: `<number>`
- Highlight one text area: `<number> (select | light)`
- Highlight from one text area to another: `<number_1> (select | light) <number_2>`

**Examples**:

- _76 select_: - Selects from the left side to the right side of 76.
- _76 select 100_: - Selects from the left side of 76 to the right side of 100.
