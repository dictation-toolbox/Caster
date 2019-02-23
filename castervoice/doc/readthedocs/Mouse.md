# Alternate Mouse Modes

Demonstration [here](https://youtu.be/UISjQBMmQ-I).

## Basic mouse commands

### Clicking

- Left click: `kick`
- Right click: `psychic`

### Moving

- Move around: `curse <direction> [[E] <direction>] <distance_in_pixel>`  
  _direction_ can be _sauce_ (up), _dunce_ (down), _lease_ (left) and _ross_ (right).

**Example**:

- _curse sauce ten_
- _curse lease sauce ten_
- _curse lease-e-sauce ten_ - Easier to speak than the example above.

## Advanced mouse commands

### Mousegrid

**Description**:

- Approach the desired position by recursively selecting tiles on the screen. Provided by Dragon Naturally Speaking.

**Usage**:

- Evoke: `mousegrid`
- Select tile: `<tile_number>`  
  _tile_number_ can be anything from 1 to 9.

### Douglas

**Description**:

- Creates a grid on the screen with horizontal and vertical numbers at the borders. Squares are directly selectable by calling out the respective numbers.

**Usage**:

- Evoke: `douglas`
- Select square: `<horizontal_number> by <vertical_number>`

**Example**:

- _5 by 20_

### Rainbow

**Description**:

- Creates a colored grid on the screen. Squares are directly selectable by calling out the respective color and number.

**Usage**:

- Evoke: `rainbow`
- Select square: `[<number_of_color_palette] <color> <number>`  
  _number_of_color_palette_ refers to the fact that colors loop when filling the screen.  
  _color_ can be replaced by the following colors: _red_, _orange_, _yellow_, _green_, _blue_, _purple_.

**Example**:

- _red 86_: - References the according square within the first color palette.
- _two red 86_ - References the according square within the second color palette.

### Legion

**Description**:

- Finds text on the screen and gives each a number which you can call out.

**Usage**:

- Evoke: `legion`
- Select text area: `<number>`