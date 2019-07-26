# Mouse

A video demonstration [here](https://youtu.be/UISjQBMmQ-I). Note that this demonstration is a little old and doesn't show all features.

## Basic mouse commands

### Clicking

- Left click: `kick [<number>]`
    - Can use an optional `<number>` to double (_two_) or triple (_three_) click.
- Right click: `psychic`

### Moving

- Move around: `curse <direction> [[E] <direction>] <distance_in_pixel>`  
    - `<direction>` can be _sauce_ (up), _dunce_ (down), _lease_ (left), or _ross_ (right).

**Examples**:

- _curse sauce ten_
- _curse lease sauce ten_
- _curse lease-e-sauce ten_ 
    - Easier to speak than the previous example.

## Advanced mouse commands

### Mousegrid

**Description**:

Approach the desired position by sequentially selecting tiles on the screen. Provided by Dragon Naturally Speaking.

**Usage**:

- Invoke: `mousegrid`
- Select tile: `<tile_number>`  
    - `<tile_number>` is an integer from 1 to 9. This function is currently only supported by Dragon for a single monitor.

### Douglas

**Description**:

Creates a grid on the screen with horizontal (top/bottom of screen) and vertical (left/right of screen) numbers at the borders. Squares are directly selectable by calling out the respective numbers.

Selecting from one point to another is available including fine adjustment of the start and end points.

**Usage**:

- Invoke: `douglas` or `douglas <monitor_number>`
- Move to square: `<horizontal_number> by <vertical_number>`
- Select: `<horizontal_number_1> by <vertical_number_1> (select | grab) <horizontal_number_2> by <vertical_number_2>`
- Select horizontally: `<horizontal_number_1> by <vertical_number_1> (select | grab) <horizontal_number_2>`
- Fine selection: `<horizontal_number_1> by <vertical_number_1> move` &rightarrow; `curse ...` &rightarrow; `squat` &rightarrow; `<horizontal_number_2> by <vertical_number_2> move` &rightarrow; `curse ...` &rightarrow; `bench`

**Examples**:

- _5 by 20_
- _5 by 20 kick_
- _5 by 20 select 10 by 30_
- _5 by 20 select 10_
- _5 by 20 move, curse sauce lease 5, squat, 10 by 30 move, curse dunce lease 10, bench_

### Rainbow

**Description**:

- Creates a colored grid on the screen. Squares are directly selectable by calling out the respective color then number.

**Usage**:

- Invoke: `rainbow` or `rainbow <monitor_number>` 
- Move to square: `[<number_of_color_palette>] <color> <number>`  
    - `<number_of_color_palette>` is an integer that refers to which chunk of that color you want as colors loop when filling the screen.
    - `<color>` can be the following: _red_, _orange_, _yellow_, _green_, _blue_, or _purple_.
- Select: `[<number_of_color_palette_1>] <color_1> <number_1> (select | grab) [<number_of_color_palette_2>] <color_2> <number_2>`
- Fine selection: `[<number_of_color_palette_1>] <color_1> <number_1> move` &rightarrow; `curse ...` &rightarrow; `squat` &rightarrow; `[<number_of_color_palette_2>] <color_2> <number_2> move` &rightarrow; `curse ...` &rightarrow; `bench`

**Examples**:

- _red 86_
    - References square within the first red palette.
- _red 86 kick_
    - Clicks at this location.
- _two red 86_
    - References square within the second red palette.
- _red 86 select 2 green 10_
    - Selects from the first red 86 to the second green 10.
- _red 86 move, curse sauce lease 5, squat, 2 green 10 move, curse dunce lease 10, bench_
    - Selects from the first red 86 to the second green 10 with fine adjustment.

### Legion

**Description**:

- Finds text on the screen and gives each a number which you can call out.

**Usage**:

- Invoke: `legion or legion [monitor_number]`
- Move to text area: `<number>`
- Highlight one text area: `<number> (select | light)`
- Highlight from one text area to another: `<number_1> (select | light | grab) <number_2>`

**Examples**:

- _76 select_
    - Selects from the left side to the right side of 76.
- _76 select 100_
    - Selects from the left side of 76 to the right side of 100.
