from dragonfly import get_engine, get_current_engine, FuncContext, Function, MappingRule, Grammar, Choice, Dictation
from castervoice.lib import printer

engine = get_current_engine().name
if engine == 'natlink':
    import natlink


class EngineModesManager(object):
    """
    Manages engine modes and microphone states using backend engine API and through dragonfly grammar exclusivity.
    """
    engine_modes = {"normal": 0,  "command": 2,
                    "dictation": 1, "numbers": 3, "spell": 4}
    mic_modes = {"on": 5, "sleeping": 6, "off": 7}
    engine_state = None
    previous_engine_state = None
    mic_state = None

    @classmethod
    def initialize(cls):
        # Remove "normal" and "off" from 'states' for non-DNS based engines.
        if engine != 'natlink':
            cls.engine_modes.pop("normal", 0)
            cls.mic_modes.pop("off", 7)
        # Sets 1st index key ("normal" or "command") depending on engine type as default mode
        cls.engine_state = cls.previous_engine_state = next(
            iter(cls.engine_modes.keys()))

    @classmethod
    def set_mic_mode(cls, mode):
        """
        Changes the engine microphone mode
        :param mode: str
            'on': mic is on
            'sleeping': mic from the sleeping and can be woken up by command
            'off': mic off and cannot be turned back on by voice. (DPI Only)
        """
        if mode in cls.mic_modes:
            cls.mic_state = mode
            if engine == 'natlink':
                natlink.setMicState(mode)
            # Overrides DNS/DPI is built in sleep grammar
            ExclusiveManager(mode, modetype="mic_mode")
        else:
            printer.out(
                "Caster: '{}' is not valid. set_mic_state modes are: 'off' - DPI Only, 'on', 'sleeping'".format(mode))

    @classmethod
    def get_mic_mode(cls):
        """
        Returns mic state.
            mode: str
        """
        return cls.mic_state

    @classmethod
    def set_engine_mode(cls, mode=None, state=True):
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
            cls.previous_engine_state = cls.engine_state
        else:
            if not state:
                # Restore previous mode
                mode = cls.previous_engine_state
            else:
                printer.out(
                    "Caster: set_engine_mode: 'State' cannot be 'True' with a undefined a 'mode'")

        if mode in cls.engine_modes:
            if engine == 'natlink':
                try:
                    natlink.execScript("SetRecognitionMode {}".format(
                        cls.engine_modes[mode]))  # engine_modes[mode] is an integer
                    cls.engine_state = mode
                    ExclusiveManager(mode, modetype="engine_mode")
                except Exception as e:
                    printer.out("natlink.execScript failed \n {}".format(e))
            else:
                # TODO: Implement set_engine_mode exclusivity. This should override DPI is built mode but kept in sync automatically.
                if engine == 'text':
                    cls.engine_state = mode
                else:
                    printer.out(
                        "Caster: 'set_engine_mode' is not implemented for '{}'".format(engine))
        else:
            printer.out(
                "Caster: '{}' mode is not valid. set_engine_mode: Modes: 'normal'- DPI Only, 'dictation', 'command', 'numbers', 'spell'".format(mode))

    @classmethod
    def get_engine_mode(cls):
        """
        Returns engine mode.
            mode: str
        """
        return cls.engine_state

    @classmethod
    def _sync_mode(cls):
        """
        Synchronizes Caster exclusivity modes an with DNS/DPI GUI built-in modes state.
        """
        # TODO: Implement set_engine_mode logic with modes not just mic_state.
        caster_mic = cls.get_mic_mode()
        natlink_mic = natlink.getMicState()
        if caster_mic is None:
            cls.mic_state = natlink_mic
        else:
            if natlink_mic != caster_mic:
                cls.set_mic_mode(natlink_mic)

class ExclusiveManager:
    """
    Loads and switches exclusivity for caster modes
    :param mode: str
    :param modetype: 'mic_mode' or 'engine_mode' str
    """
    # TODO: Implement set_engine_mode exclusivity with mode rules.
    # TODO: Implement hotkey for microphone on-off
    sleep_grammar = None
    sleeping = False

    sleep_rule = MappingRule(
        name="sleep_rule",
        mapping={
            "caster <mic_mode>": Function(lambda mic_mode: EngineModesManager.set_mic_mode(mode=mic_mode)),
            "<text>": Function(lambda text: False)
        },
        extras=[Choice("mic_mode", {
            "off": "off",
            "on": "on",
            "sleep": "sleeping",
        }),
            Dictation("text")],
        context=FuncContext(lambda: ExclusiveManager.sleeping),
    )

    def __init__(self, mode, modetype):
        if modetype == "mic_mode":
            if not isinstance(ExclusiveManager.sleep_grammar, Grammar):
                grammar = ExclusiveManager.sleep_grammar = Grammar("sleeping")
                grammar.add_rule(self.sleep_rule)
                grammar.load()
            if mode == "sleeping":
                self.set_exclusive(state=True)
                printer.out("Caster: Microphone is sleeping")
            if mode == "on":
                self.set_exclusive(state=False)
                printer.out("Caster: Microphone is on")
            if mode == "off":
                printer.out("Caster: Microphone is off")
        else:
            printer.out("{}, {} not implemented".format(mode, modetype))

    def set_exclusive(self, state):
        grammar = ExclusiveManager.sleep_grammar
        ExclusiveManager.sleeping = state
        grammar.set_exclusive(state)
        get_engine().process_grammars_context()