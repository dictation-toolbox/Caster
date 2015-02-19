import sys
try:
    # this section only necessary if called externally to Dragon
    BASE_PATH = sys.argv[0].split("MacroSystem")[0] + "MacroSystem"
    if BASE_PATH not in sys.path:
        sys.path.append(BASE_PATH)
except Exception:
    pass
from asynch.hmc.hmc_recording import Homunculus_Recording
from asynch.hmc.hmc_vocabulary import Homunculus_Vocabulary
from asynch.hmc.homunculus import Homunculus
from lib import settings, utilities
from lib.dragonfree import launch as ll




def launch(htype=None, info=None):
    instructions=["pythonw", settings.SETTINGS["paths"]["HOMUNCULUS_PATH"]]
    if htype!=None:
        instructions.append(htype)
        if info!=None:
            instructions.append(info)
    else:
        instructions.append(settings.QTYPE_DEFAULT)
    ll.run(instructions)

def clean_homunculi():
    while utilities.window_exists(None, settings.HOMUNCULUS_VERSION):
        ll.kill_process("pythonw.exe")
    while utilities.window_exists(None, settings.HOMUNCULUS_VERSION+settings.HMC_TITLE_VOCABULARY):
        ll.kill_process("pythonw.exe")
    while utilities.window_exists(None, settings.HOMUNCULUS_VERSION+settings.HMC_TITLE_RECORDING):
        ll.kill_process("pythonw.exe")

if __name__ == '__main__':
    found_word=None
    if len(sys.argv)>2:
        found_word=sys.argv[2]
    if sys.argv[1]==settings.QTYPE_DEFAULT:
        app = Homunculus(sys.argv[1])
    elif sys.argv[1]==settings.QTYPE_SET:
        app = Homunculus_Vocabulary([settings.QTYPE_SET, found_word])
    elif sys.argv[1]==settings.QTYPE_REM:
        app = Homunculus_Vocabulary([settings.QTYPE_REM, found_word])
    elif sys.argv[1]==settings.QTYPE_RECORDING:
        app = Homunculus_Recording([settings.QTYPE_RECORDING, found_word])
    elif sys.argv[1]==settings.QTYPE_INSTRUCTIONS:
        app = Homunculus(sys.argv[1], sys.argv[2])
            