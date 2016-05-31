# Alternate Mouse Modes
Demonstration [here](https://youtu.be/UISjQBMmQ-I).

## Basic mouse commands

### Clicking
- Left click: *kick*
- Right click: *psychic* 

### Moving 
- Move around: *mouse* *<direction>* *<distance_in_pixel>*  
    *<direction>* can be *up*, *down*, *right* and *left*. 

## Advanced mouse commands

### Mousegrid
**Description**:  
- Approach the desired position by recursively selecting tiles on the screen. Provided by Dragon Naturally Speaking. 

**Usage**:  
- Evoke: *mousegrid*
- Select tile: *<tile_number>*  
  *<tile_number>* can be anything from 1 to 9.  

### Douglas
**Description**:  
- Creates a grid on the screen with horizontal and vertical numbers at the borders. Squares are directly selectable by calling out the respective numbers.

**Usage**:  
- Evoke: *douglas*
- Select square: *<horizontal_number>* *by* *<vertical_number>*  

**Example**:  
- *5 by 20*

### Rainbow
**Description**:  
- Creates a colored grid on the screen. Squares are directly selectable by calling out the respective color and number.

**Usage**:  
- Evoke: *rainbow*
- Select square: *[<number_of_color_palette]* *<color>* *<number>*  
    *<number_of_color_palette>* refers to the fact that colors loop when filling the screen.  
    *<color>* can be replaced by the following colors: *red*, *orange*, *yellow*, *green*, *blue*, *purple*.

**Example**:  
- *red 86*: - References the according square within the first color palette.
- *two red 86*  - References the according square within the second color palette.

### Legion
**Description**:  
- Finds text on the screen and gives each a number which you can call out.

**Usage**:  
- Evoke: *legion*
- Select text area: *<number>*