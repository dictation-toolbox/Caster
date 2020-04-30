# Mouse

A video demonstration of mouse commands is found [here](https://youtu.be/UISjQBMmQ-I). Note that this demonstration is a little old and doesn't show all features.

## Basic mouse commands

### Clicking

- Left click: `kick [<number>]`
    - Can use an optional `<number>` to double (_two_) or triple (_three_) click.
- Right click: `psychic`
- Hold down left mouse: `squat`
- Release left mouse: `bench`
- Hold down right mouse: `lean`
- Release right mouse: `hoist`
- Control left click: `colic`
- Middle click: `kick mid`
- Shift click: `shift click`
- Shift right click: `shift right click`

### Moving

- Move around: `curse <direction> [[E] <direction>] <distance_in_pixel>`  
    - `<direction>` can be _sauce_ (up), _dunce_ (down), _lease_ (left), or _ross_ (right).
- Scroll mouse wheel: `scree <direction> [number_of_scrolls]`
    - `<direction>` can be _sauce_ (up) or _dunce_ (down).

**Examples**:

- _curse sauce ten_
- _curse lease sauce ten_
- _curse lease-e-sauce ten_ 
    - Easier to speak than the previous example.

## Advanced mouse commands

### Mousegrid

**Description**:

Approach the desired position by sequentially selecting tiles on the screen. Provided by Dragon Naturally Speaking and only available for the main monitor.

**Usage**:

- Invoke: `mousegrid`
- Select tile: `<tile_number>`  
    - `<tile_number>` is an integer from 1 to 9.
- Click on left on screen: `left point`
- Click on center on screen: `center point`
- Click on right on screen: `right point`

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

### Sudoku

**Description**:

Creates a grid of numbered 3 x 3 squares over the whole screen. A number is called out to move directly to the center of the square. The position can be refined to one of the adjacent small squares. It supports both clicking and dragging.

**Usage**:

- Invoke: `sudoku` or `sudoku <monitor_number>`
- Move to square: `<number>`
- Select/drag to square: `drag <number>`
- Select/drag from square to square: `<number> drag <number>`
- Move to square with refinement (also for drag): `<number> grid <number>`

**Examples**:

- _159 grid 8_
- _95 kick double_
- _drag 201_
- _7 drag 13_
- _55 move, curse sauce lease 5, squat, 20 grid 7 move, curse dunce lease 10, bench_

### Legion

**Description**:

- Finds text on the screen and gives each a number which you can call out.

**Usage**:

- Invoke: `legion [<monitor_number>] [<rough_detailed>]`
    - `<rough_detailed>` (optional) can be one of "rough" (default) or "detailed". "rough" can run a little faster depending on the system. "detailed" can be more accurate. Control the degree of downscaling done by "rough" using the user setting: `legion_downscale_factor`. 
- Move to text area: `<number>`
- Highlight one text area: `<number> (select | light)`
- Highlight from one text area to another: `<number_1> (select | light | grab) <number_2>`

**Examples**:

- _legion 2_
    - Runs legion on screen 2.
- _legion detailed_
    - Runs legion on screen 1 scanning with full resolution.
- _76 select_
    - Selects from the left side to the right side of 76.
- _76 select 100_
    - Selects from the left side of 76 to the right side of 100.
