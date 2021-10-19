from dragonfly import get_engine, get_current_engine
from castervoice.lib import printer

if get_engine().name == 'natlink':
    import natlink


class EngineModesManager(object):
    """
    Manages engine modes and microphone states using backend engine API and through dragonfly grammar exclusivity.
    """
    def __init__(self, ExclusiveManager):
        self.engine_modes = {
            "normal": 0,
            "command": 2,
            "dictation": 1,
            "numbers": 3,
            "spell": 4
        }
        self.mic_modes = {"on": 5, "sleeping": 6, "off": 7}
        self.engine_state = None
        self.previous_engine_state = None
        self.mic_state = None
        self.engine = get_current_engine().name
        self._exclusive_manager = ExclusiveManager

        # Remove "normal" and "off" from 'states' for non-DNS based engines.
        if self.engine != 'natlink':
            self.engine_modes.pop("normal", 0)
            self.mic_modes.pop("off", 7)
        # Sets 1st index key ("normal" or "command") depending on engine type as default mode
        self.engine_state = self.previous_engine_state = next(
            iter(self.engine_modes.keys()))

    def set_mic_mode(self, mode):
        """
        Changes the engine microphone mode
        :param mode: str
            'on': mic is on
            'sleeping': mic from the sleeping and can be woken up by command
            'off': mic off and cannot be turned back on by voice. (DPI Only)
        """
        if mode in self.mic_modes:
            self.mic_state = mode
            if self.engine == 'natlink':
                natlink.setMicState(mode)
            # Overrides DNS/DPI is built in sleep grammar
            self._exclusive_manager.set_mode(mode, modetype="mic_mode")
        else:
            printer.out(
                "Caster: '{}' is not valid. set_mic_state modes are: 'off' - DPI Only, 'on', 'sleeping'"
                .format(mode))

    def get_mic_mode(self):
        """
        Returns mic state.
            mode: str
        """
        return self.mic_state

    def set_engine_mode(self, mode=None, state=True):
        """
        Sets the engine mode so that only certain types of commands/dictation are recognized.
        :param state: Bool - enable/disable mode.
            'True': replaces current mode (Default)
            'False': restores previous mode
        :param mode: str
            'normal': dictation and command (Default: DPI only)
            'dictation': Dictation only 
            'command': Commands only (Default: Other engines)
            'numbers': Numbers only
            'spell': Spelling only
        """
        if state and mode is not None:
            # Track previous engine state
            self.previous_engine_state = self.engine_state
        else:
            if not state:
                # Restore previous mode
                mode = self.previous_engine_state
            else:
                printer.out(
                    "Caster: set_engine_mode: 'State' cannot be 'True' with a undefined a 'mode'"
                )

        if mode in self.engine_modes:
            if self.engine == 'natlink':
                try:
                    natlink.execScript("SetRecognitionMode {}".format(
                        self.engine_modes[mode]))  # mode is an integer
                    self.engine_state = mode
                    self._exclusive_manager.set_mode(mode, modetype="engine_mode")
                except Exception as e:
                    printer.out("natlink.execScript failed \n {}".format(e))
            else:
                # TODO: Implement set_engine_mode exclusivity. This should override DPI is built mode but kept in sync automatically.
                if self.engine == 'text':
                    self.engine_state = mode
                else:
                    printer.out(
                        "Caster: 'set_engine_mode' is not implemented for '{}'".format(
                            self.engine))
        else:
            printer.out(
                "Caster: '{}' mode is not valid. set_engine_mode: Modes: 'normal'- DPI Only, 'dictation', 'command', 'numbers', 'spell'"
                .format(mode))

    def get_engine_mode(self):
        """
        Returns engine mode.
            mode: str
        """
        return self.engine_state

    def _sync_mode(self):
        """
        Synchronizes Caster exclusivity modes an with DNS/DPI GUI built-in modes state.
        """
        # TODO: Implement set_engine_mode logic with modes not just mic_state.
        caster_mic = self.get_mic_mode()
        natlink_mic = natlink.getMicState()
        if caster_mic is None:
            self.mic_state = natlink_mic
        else:
            if natlink_mic != caster_mic:
                self.set_mic_mode(natlink_mic)
