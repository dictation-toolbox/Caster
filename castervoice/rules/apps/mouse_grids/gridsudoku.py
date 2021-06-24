import time
from dragonfly import Function, Choice, MappingRule, ShortIntegerRef
from dragonfly.actions.mouse import get_cursor_position
from castervoice.lib import control
from castervoice.lib.navigation import Grid
from castervoice.lib.actions import Mouse
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R
from castervoice.rules.ccr.standard import SymbolSpecs


# Perform an action based on the passed in action number
# action - optional mouse action after movement
def perform_mouse_action(action):
    if action == 0:
        Mouse("left").execute()
    if action == 1:
        Mouse("left:2").execute()
    elif action == 2:
        Mouse("right").execute()


# Command to move the mouse
# n - square to move to
# s - optional inner square to move to
# action - optional mouse action after movement
def move_mouse(n, s, action):
    sudoku = control.nexus().comm.get_com("grids")
    sudoku.move_mouse(int(n), int(s))
    int_a = int(action)
    if (int_a == 0) | (int_a == 1) | (int_a == 2) | (int_a == -1):
        sudoku.kill()
        Grid.wait_for_grid_exit()

    time.sleep(0.1)
    perform_mouse_action(int(action))

# Command to drag the mouse from the current position
# n0 - optional square to drag from
# s0 - optional inner square to drag from
# n  - square to drag to
# s  - optional inner square to drag to
# action - optional mouse action after movement
def drag_mouse(n0, s0, n, s, action):
    sudoku = control.nexus().comm.get_com("grids")
    # These numbers are internal to the monitor the screen is on
    x, y = sudoku.get_mouse_pos(int(n), int(s))
    
    # If dragging from a different location, move there first
    if int(n0) > 0:
        sudoku.move_mouse(int(n0), int(s0))
    sudoku.kill()
    Grid.wait_for_grid_exit()
    time.sleep(0.1)
    # Hold down click, move to drag destination, and release click
    Mouse("left:down/10").execute()
    Mouse("[{}, {}]".format(x, y)).execute()
    time.sleep(0.1)
    Mouse("left:up/30").execute()
    perform_mouse_action(int(action))

# This is used for the fine movement dragging
def drag_from_to(x1, y1, x2, y2):
    Mouse("[{}, {}]".format(x1, y1)).execute()
    time.sleep(0.5)
    Mouse("left:down").execute()
    time.sleep(0.5)
    Mouse("[{}, {}]".format(x2, y2)).execute()
    time.sleep(0.5)
    Mouse("left:up").execute()

def store_first_point():
    global x1, y1
    x1, y1 = get_cursor_position()
    
def select_text():
    global x1, y1, x2, y2
    x2, y2 = get_cursor_position()
    s = control.nexus().comm.get_com("grids")
    s.kill()
    Grid.wait_for_grid_exit()
    drag_from_to(x1, y1, x2, y2)

'''
Rules for sudoku grid. We can either move the mouse or drag it.
The number n is one of the numbered squares.
The grid portion is a number from 1-9 referencing an inner unnumbered square.
'''


class SudokuGridRule(MappingRule):
    pronunciation = "sudoku grid"

    mapping = {
        "<n> [grid <s>] [<action>]":
            R(Function(move_mouse)),
        "[<n0>] [grid <s0>] (grab | select | drag) <n> [grid <s>] [<action>]":
            R(Function(drag_mouse)),
        "squat {weight=2}":
            R(Function(store_first_point)),
        "bench {weight=2}":
            R(Function(select_text)),
        SymbolSpecs.CANCEL + "{weight=2}":
            R(Function(Grid.kill)),
    }
    extras = [
        ShortIntegerRef("n", -1, 1500),
        ShortIntegerRef("n0", -1, 1500),
        ShortIntegerRef("s", 0, 10),
        ShortIntegerRef("s0", 0, 10),
        Choice("action", {
            "kick": 0,
            "kick (double | 2)": 1,
            "psychic": 2,
            "move": 3,
        }),
    ]
    defaults = {
        "n": 0,
        "n0": 0,
        "s": 0,
        "s0": 0,
        "action": -1,
    }

def get_rule():
    Details = RuleDetails(name="Sudoku Grid", function_context=lambda: Grid.is_grid_active("sudoku"))
    return SudokuGridRule, Details
