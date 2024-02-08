import os
import subprocess
import sys

from xmlrpc.server import SimpleXMLRPCServer

try:  # Style C -- may be imported into Caster, or externally
    BASE_PATH = os.path.realpath(__file__).rsplit(os.path.sep + "castervoice", 1)[0]
    if BASE_PATH not in sys.path:
        sys.path.append(BASE_PATH)
finally:
    from castervoice.lib import settings


def launch(hmc_type, data=None):
    from dragonfly import (WaitWindow, FocusWindow, Key)
    instructions = _get_instructions(hmc_type)
    if data is not None:
        instructions.append(data)
    subprocess.Popen(instructions)
    hmc_title = _get_title(hmc_type)
    WaitWindow(title=hmc_title, timeout=5).execute()
    FocusWindow(title=hmc_title).execute()


def _get_instructions(hmc_type):
    if hmc_type == settings.QTTYPE_SETTINGS:
        return [
            settings.SETTINGS["paths"]["PYTHONW"],
            settings.SETTINGS["paths"]["SETTINGS_WINDOW_PATH"]
        ]
    else:
        return [
            settings.SETTINGS["paths"]["PYTHONW"],
            settings.SETTINGS["paths"]["HOMUNCULUS_PATH"], hmc_type
        ]


def _get_title(hmc_type):
    default = settings.HOMUNCULUS_VERSION
    if hmc_type == settings.QTYPE_DEFAULT or hmc_type == settings.QTYPE_INSTRUCTIONS:
        return default
    elif hmc_type == settings.QTYPE_RECORDING:
        return default + settings.HMC_TITLE_RECORDING
    elif hmc_type == settings.QTYPE_DIRECTORY:
        return default + settings.HMC_TITLE_DIRECTORY
    elif hmc_type == settings.QTYPE_CONFIRM:
        return default + settings.HMC_TITLE_CONFIRM
    elif hmc_type == settings.QTTYPE_SETTINGS:
        return settings.SETTINGS_WINDOW_TITLE + settings.SOFTWARE_VERSION_NUMBER
    return default


def main():
    import PySide2.QtWidgets
    from castervoice.asynch.hmc.homunculus import Homunculus
    from castervoice.lib.merge.communication import Communicator
    server_address = (Communicator.LOCALHOST, Communicator().com_registry["hmc"])
    # Enabled by default logging causes RPC to malfunction when the GUI runs on
    # pythonw.  Explicitly disable logging for the XML server.
    server = SimpleXMLRPCServer(server_address, logRequests=False, allow_none=True)
    app = PySide2.QtWidgets.QApplication(sys.argv)
    window = Homunculus(server, sys.argv)
    window.show()
    exit_code = app.exec_()
    server.shutdown()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
