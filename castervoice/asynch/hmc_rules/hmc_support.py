from castervoice.lib import control, settings


def kill():
    control.nexus().comm.get_com("hmc").kill()


if not settings.SETTINGS["miscellaneous"]["hmc"]:
    print("WARNING: Tk Window controls have been disabled -- this is not advised!")