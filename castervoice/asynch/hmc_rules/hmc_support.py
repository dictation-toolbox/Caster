from castervoice.lib import control, settings, printer


def kill():
    control.nexus().comm.get_com("hmc").kill()


if not settings.settings(["miscellaneous", "hmc"]):
    printer.out("WARNING: Tk Window controls have been disabled -- this is not advised!")