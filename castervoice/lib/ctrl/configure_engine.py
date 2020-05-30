# TODO: Create and utilize base class. These classes should be initialized only once.
# TODO: Add a function for end-user user to overload in EngineConfigEarly and EngineConfigLate

class EngineConfigEarly():
    """
    Initializes engine specific customizations before Nexus initializes.
    Grammars are not loaded
    """
    from castervoice.lib import settings
    from dragonfly import get_engine
    engine = get_engine().name  # get_engine used as a workaround for running Natlink inprocess

    def __init__(self):
        self.set_cancel_word()

    def set_cancel_word(self):
        """
        Defines SymbolSpecs cancel word as "escape" for windows speech recognition (WSR)
        """
        if self.engine in ["sapi5shared", "sapi5", "sapi5inproc"]:
            self.settings.WSR = True
            from castervoice.rules.ccr.standard import SymbolSpecs
            SymbolSpecs.set_cancel_word("escape")


class EngineConfigLate():
    """
    Initializes engine specific customizations after Nexus has initialized.
    Grammars are loaded into engine.
    """
    from castervoice.lib import settings
    from castervoice.lib import printer
    from dragonfly import get_current_engine
    engine = get_current_engine().name

    def __init__(self):
        from castervoice.lib import control # Access to Nexus instance
        self.instannce = control.nexus()._engine_modes_manager
        if self.engine != "text":
            self.set_default_mic_mode()
            self.set_engine_default_mode()


    def set_default_mic_mode(self):
        """
        Sets the microphone state on Caster startup.
        """
        # Only DNS supports mic_state 'off'. Substituts `sleep` mode on other engines"
        if self.settings.SETTINGS["engine"]["default_mic"]: # Default is `False`
            default_mic_state = self.settings.SETTINGS["engine"]["mic_mode"] # Default is `on`
            if self.engine != "natlink" and default_mic_state == "off": 
                default_mic_state == "sleep" 
            self.instannce.set_mic_mode(default_mic_state)


    def set_engine_default_mode(self):
        """
        Sets the engine mode on Caster startup.
        """
        # Only DNS supports 'normal'. Substituts `command` mode on other engines"
        if self.settings.SETTINGS["engine"]["default_engine_mode"]: # Default is `False`
            default_mode = self.settings.SETTINGS["engine"]["engine_mode"]  # Default is `normal`
            if self.engine != "natlink" and default_mode == "normal":
                default_mode == "command"
            self.instannce.set_engine_mode(mode=default_mode, state=True)