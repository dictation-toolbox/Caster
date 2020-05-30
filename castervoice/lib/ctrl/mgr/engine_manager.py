from dragonfly import get_engine, get_current_engine
from castervoice.lib import settings, printer

# TODO: Implement a grammar exclusivity for non-DNS engines in a separate class

class EngineModesManager(object):
    """
    Manages engine modes and microphone states using backend engine API and through dragonfly grammar exclusivity.
    """
    engine = get_current_engine().name
    if engine == 'natlink':
        import natlink
    
    engine_modes =  {"normal":0,  "command":2, "dictation":1,"numbers":3, "spell":4}
    mic_modes = ["on", "sleeping", "off"]
    engine_state = None
    previous_engine_state = None
    mic_state = None

    def initialize(self):
        # Remove "normal" and "off" from 'states' for non-DNS based engines.
        if self.engine != 'natlink':
            self.engine_modes.pop("normal", 0)
            self.mic_modes.remove("off")
        # Sets 1st index key ("normal" or "command") depending on engine type as default mode
        self.engine_state = self.previous_engine_state = next(iter(self.engine_modes.keys()))


    def set_mic_mode(self, mode):
        """
        Changes the engine microphone mode
        'on': mic is on
        'sleeping': mic from the sleeping and can be woken up by command
        'off': mic off and cannot be turned back on by voice. (DNS Only)
        """
        if mode in self.mic_modes:
            self.mic_state = mode
            if self.engine == 'natlink':
                self.natlink.setMicState(mode)
            # From here other engines use grammar exclusivity to re-create the sleep mode
            #if mode != "off": # off does not need grammar exclusivity
                #pass
                # TODO: Implement mic mode sleep mode using grammar exclusivity. This should override DNS is built in sleep grammar but kept in sync automatically with natlink.setmic_state
            else:
                printer.out("Caster: 'set_mic_mode' is not implemented for '{}'".format(self.engine))
        else:
            printer.out("Caster: '{}' is not a valid. set_mic_state modes are: 'off' - DNS Only, 'on', 'sleeping'".format(mode))


    def get_mic_mode(self):
        """
        Returns mic state.
        mode: string
        """
        return self.mic_state


    def set_engine_mode(self, mode=None, state=True):
        """
        Sets the engine mode so that only certain types of commands/dictation are recognized.
        'state': Bool - enable/disable mode.
            'True': replaces current mode (Default)
            'False': restores previous mode
        'normal': dictation and command (Default: DNS only)
        'dictation': Dictation only 
        'command': Commands only (Default: Other engines)
        'numbers': Numbers only
        'spell': Spelling only
        """
        if state and mode is not None:
            # Track previous engine state
            # TODO: Timer to synchronize natlink.getMicState() with mengine_state in case of changed by end-user via DNS GUI.
            self.previous_engine_state = self.engine_state
        else:
            if not state:
                # Restore previous mode
                mode = self.previous_engine_state
            else:
                printer.out("Caster: set_engine_mode: 'State' cannot be 'True' with a undefined a 'mode'")
            
        if mode in self.engine_modes:
            if self.engine == 'natlink':
                try:
                    self.natlink.execScript("SetRecognitionMode {}".format(self.engine_modes[mode])) # engine_modes[mode] is an integer
                    self.engine_state = mode
                except Exception as e:
                    printer.out("natlink.execScript failed \n {}".format(e))
            else:
                # TODO: Implement mode exclusivity. This should override DNS is built in sleep grammar but kept in sync automatically with natlinks SetRecognitionMode
                # Once DNS enters its native mode exclusivity will override the any native DNS mode except for normal/command mode.
                if self.engine == 'text':
                    self.engine_state = mode
                else:
                    printer.out("Caster: 'set_engine_mode' is not implemented for '{}'".format(self.engine))
        else:
            printer.out("Caster: '{}' mode is not a valid. set_engine_mode: Modes: 'normal'- DNS Only, 'dictation', 'command', 'numbers', 'spell'".format(mode))


    def get_engine_mode(self):
        """
        Returns engine mode.
        mode: str
        """
        return self.engine_state
