import time
from dragonfly import Function, Choice, MappingRule, Mouse
from castervoice.lib import control, navigation
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.state.short import R
from castervoice.rules.ccr.standard import SymbolSpecs


def kill():
    control.nexus().comm.get_com("grids").kill()


def send_input(n, action):
    s = control.nexus().comm.get_com("grids")

    int_a = int(action)
    response = None

    if int_a != 2:
        s.go(str(n))
    elif int_a == 2:
        response = s.retrieve_data_for_highlight(str(int(n)))

    s.kill()
    navigation.wait_for_grid_exit()

    if int_a == 0:
        Mouse("left").execute()
    elif int_a == 1:
        Mouse("right").execute()
    elif int_a == 2:
        x1 = response["l"] + 2
        x2 = response["r"]
        y = response["y"]
        Mouse("[{}, {}]".format(x1, y)).execute()
        time.sleep(0.1)
        Mouse("left:down").execute()
        Mouse("[{}, {}]".format(x2, y)).execute()
        time.sleep(0.1)
        Mouse("left:up").execute()


def drag_highlight(n1, n2):
    s = control.nexus().comm.get_com("grids")
    response1 = s.retrieve_data_for_highlight(str(int(n1)))
    response2 = s.retrieve_data_for_highlight(str(int(n2)))
    s.kill()
    navigation.wait_for_grid_exit()
    x11 = response1["l"] + 2
    y1 = response1["y"]
    x22 = response2["r"]
    y2 = response2["y"]
    Mouse("[{}, {}]".format(x11, y1)).execute()
    time.sleep(0.1)
    Mouse("left:down").execute()
    Mouse("[{}, {}]".format(x22, y2)).execute()
    time.sleep(0.1)
    Mouse("left:up").execute()


class LegionGridRule(MappingRule):

    mapping = {
        "<n> [<action>]":
            R(Function(send_input)),
        "refresh":
            R(Function(navigation.mouse_alternates, mode="legion")),
        SymbolSpecs.CANCEL + " {weight=2}":
            R(Function(kill)),
        "<n1> (select | light) <n2>":
            R(Function(drag_highlight)),
    }
    extras = [
        Choice("action", {
            "kick": 0,
            "psychic": 1,
            "select | light": 2,
        }),
        IntegerRefST("n", 0, 1000),
        IntegerRefST("n1", 0, 1000),
        IntegerRefST("n2", 0, 1000),
    ]
    defaults = {
        "action": -1,
    }


def get_rule():
    return LegionGridRule, RuleDetails(name="legion grid rule", title="legiongrid")
