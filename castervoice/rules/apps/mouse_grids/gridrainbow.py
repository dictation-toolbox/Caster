import time
from dragonfly import Function, Choice, MappingRule, ShortIntegerRef
from dragonfly.actions.mouse import get_cursor_position
from castervoice.lib import control
from castervoice.lib.navigation import Grid
from castervoice.lib.actions import Mouse
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R
from castervoice.rules.ccr.standard import SymbolSpecs


def send_input(pre, color, n, action):
    s = control.nexus().comm.get_com("grids")
    s.move_mouse(int(pre), int(color), int(n))
    int_a = int(action)
    if (int_a == 0) | (int_a == 1) | (int_a == 2) | (int_a == -1):
        s.kill()
        Grid.wait_for_grid_exit()
        time.sleep(0.1)
    if int_a == 0:
        Mouse("left").execute()
    if int_a == 1:
        Mouse("left:2").execute()
    elif int_a == 2:
        Mouse("right").execute()


def send_input_select(pre1, color1, n1, pre2, color2, n2):
    s = control.nexus().comm.get_com("grids")
    s.move_mouse(int(pre1), int(color1), int(n1))
    _x1, _y1 = get_cursor_position()
    s.move_mouse(int(pre2), int(color2), int(n2))
    _x2, _y2 = get_cursor_position()
    s.kill()
    Grid.wait_for_grid_exit()
    drag_from_to(_x1, _y1, _x2, _y2)


def send_input_select_short(pre1, color1, n1, n2):
    send_input_select(pre1, color1, n1, pre1, color1, n2)


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
    Grid.wait_for_grid_exit()
    drag_from_to(x1, y1, x2, y2)


class RainbowGridRule(MappingRule):

    mapping = {
        "[<pre>] <color> <n> [<action>]":
            R(Function(send_input)),
        "[<pre1>] <color1> <n1> (grab | select) [<pre2>] <color2> <n2>":
            R(Function(send_input_select)),
        "[<pre1>] <color1> <n1> (grab | select) <n2>":
            R(Function(send_input_select_short)),
        "squat {weight=2}":
            R(Function(store_first_point)),
        "bench {weight=2}":
            R(Function(select_text)),
        SymbolSpecs.CANCEL + " {weight=2}":
            R(Function(Grid.kill)),
    }
    extras = [
        ShortIntegerRef("pre", 0, 9),
        ShortIntegerRef("pre1", 0, 9),
        ShortIntegerRef("pre2", 0, 9),
        Choice(
            "color", {
                "(red | rot)": 0,
                "(orange | tan | brown | braun)": 1,
                "(yellow | gelb)": 2,
                "(green | gruen)": 3,
                "(blue | blau)": 4,
                "(purple | lila)": 5
            }),
        Choice(
            "color1", {
                "(red | rot)": 0,
                "(orange | tan | brown | braun)": 1,
                "(yellow | gelb)": 2,
                "(green | gruen)": 3,
                "(blue | blau)": 4,
                "(purple | lila)": 5
            }),
        Choice(
            "color2", {
                "(red | rot)": 0,
                "(orange | tan | brown | braun)": 1,
                "(yellow | gelb)": 2,
                "(green | gruen)": 3,
                "(blue | blau)": 4,
                "(purple | lila)": 5
            }),
        ShortIntegerRef("n", 0, 100),
        ShortIntegerRef("n1", 0, 100),
        ShortIntegerRef("n2", 0, 100),
        Choice("action", {
            "kick": 0,
            "kick (double | 2)": 1,
            "psychic": 2,
            "move": 3,
        }),
    ]
    defaults = {
        "pre": 0,
        "pre1": 0,
        "pre2": 0,
        "action": -1,
    }

def get_rule():
    return RainbowGridRule, RuleDetails(name="rainbow grid rule", function_context=lambda: Grid.is_grid_active("rainbow"))
