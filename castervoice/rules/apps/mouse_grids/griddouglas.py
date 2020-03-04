import time
from dragonfly import Function, Choice, MappingRule
from dragonfly.actions.mouse import get_cursor_position
from castervoice.lib import control, navigation
from castervoice.lib.actions import Mouse
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.state.short import R
from castervoice.rules.ccr.standard import SymbolSpecs


def kill():
    control.nexus().comm.get_com("grids").kill()


def send_input(x, y, action):
    s = control.nexus().comm.get_com("grids")
    s.move_mouse(int(x), int(y))
    int_a = int(action)
    if (int_a == 0) | (int_a == 1) | (int_a == -1):
        s.kill()
        navigation.wait_for_grid_exit()
    if int_a == 0:
        Mouse("left").execute()
    elif int_a == 1:
        Mouse("right").execute()


def send_input_select(x1, y1, x2, y2):
    s = control.nexus().comm.get_com("grids")
    s.move_mouse(int(x1), int(y1))
    _x1, _y1 = get_cursor_position()
    s.move_mouse(int(x2), int(y2))
    _x2, _y2 = get_cursor_position()
    s.kill()
    navigation.wait_for_grid_exit()
    drag_from_to(_x1, _y1, _x2, _y2)


def send_input_select_short(x1, y1, x2):
    send_input_select(x1, y1, x2, y1)


def drag_from_to(x1, y1, x2, y2):
    Mouse("[{}, {}]".format(x1, y1)).execute()
    time.sleep(0.1)
    Mouse("left:down").execute()
    Mouse("[{}, {}]".format(x2, y2)).execute()
    time.sleep(0.1)
    Mouse("left:up").execute()


x1 = None
x2 = None
y1 = None
y2 = None


def store_first_point():
    global x1, y1
    x1, y1 = get_cursor_position()


def select_text():
    global x1, y1, x2, y2
    x2, y2 = get_cursor_position()
    s = control.nexus().comm.get_com("grids")
    s.kill()
    navigation.wait_for_grid_exit()
    drag_from_to(x1, y1, x2, y2)


class DouglasGridRule(MappingRule):
    mapping = {
        "<x> [by] <y> [<action>]":
            R(Function(send_input)),
        "<x1> [by] <y1> (grab | select) <x2> [by] <y2>":
            R(Function(send_input_select)),
        "<x1> [by] <y1> (grab | select) <x2>":
            R(Function(send_input_select_short)),
        "squat":
            R(Function(store_first_point)),
        "bench":
            R(Function(select_text)),
        SymbolSpecs.CANCEL:
            R(Function(kill)),
    }
    extras = [
        IntegerRefST("x", 0, 300),
        IntegerRefST("y", 0, 300),
        IntegerRefST("x1", 0, 300),
        IntegerRefST("y1", 0, 300),
        IntegerRefST("x2", 0, 300),
        IntegerRefST("y2", 0, 300),
        Choice("action", {
            "kick": 0,
            "psychic": 1,
            "move": 2,
        }),
        Choice("point", {
            "one": 1,
            "two": 2,
        }),
    ]
    defaults = {
        "action": -1,
    }


def get_rule():
    return DouglasGridRule, RuleDetails(name="douglas grid rule", title="douglasgrid")
