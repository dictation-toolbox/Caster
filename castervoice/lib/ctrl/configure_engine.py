import time
from dragonfly import get_current_engine, register_recognition_callback, RecognitionObserver
from castervoice.lib import settings
from castervoice.lib import printer


class Observer(RecognitionObserver):
    def __init__(self):
        from castervoice.lib import control
        self.mic_mode = None
        self._engine_modes_manager = control.nexus().engine_modes_manager

    def on_begin(self):
        self.mic_mode = self._engine_modes_manager.get_mic_mode()

    def on_recognition(self, words):
        if not self.mic_mode == "sleeping":
            printer.out("$ {}".format(" ".join(words)))

    def on_failure(self):
        if not self.mic_mode == "sleeping":
            printer.out("?!")



class EngineConfigEarly:
    """
    Initializes engine customizations before Nexus initializes.
    Grammars are not loaded
    """
    # get_engine used as a workaround for running Natlink inprocess
    def __init__(self):
        self.engine = get_current_engine().name
        self._set_cancel_word()

    def _set_cancel_word(self):
        """
        Defines SymbolSpecs cancel word as "escape" for windows speech recognition (WSR)
        """
        if self.engine in ["sapi5shared", "sapi5", "sapi5inproc"]:
            settings.WSR = True
            from castervoice.rules.ccr.standard import SymbolSpecs
            SymbolSpecs.set_cancel_word("escape")


class EngineConfigLate:
    """
    Initializes engine specific customizations after Nexus has initialized.
    Grammars are loaded into engine.
    """
    def __init__(self):
        from castervoice.lib import control
        self._engine_modes_manager = control.nexus().engine_modes_manager
        self.engine = get_current_engine().name
        self.sync_timer = None
        self.sleep_timer = None
        Observer().register()


        if self.engine != 'natlink':
            # Other engines besides natlink needs a default mic state for sleep_timer
            self._engine_modes_manager.mic_state = "on"
        if self.engine != "text":
            self._engine_timers()
            self._set_default_mic_mode()
            self._set_engine_default_mode()

    def _engine_timers(self):
        # Timer to synchronize natlink.getMicState/SetRecognitionMode with mode_state in case of changed by end-user via DNS GUI.
        if self.engine == 'natlink' and self.sync_timer is None:
            sync_timer = get_current_engine().create_timer(
                callback=self._engine_modes_manager._sync_mode, interval=1)
            sync_timer.start()
        # A timer to change microphone state to "sleep" after X amount of seconds after last successful recognition
        if self.sleep_timer is None and settings.SETTINGS["engine"][
                "mic_sleep_timer_on"] == True:
            self.sleep_timer = get_current_engine().create_timer(
                callback=self._sleep_timer,
                interval=int(settings.SETTINGS["engine"]["mic_sleep_timer"]))
            self.sleep_timer.start()
            register_recognition_callback(function=self._reset_sleep_timer)

    def _sleep_timer(self):
        """
        Puts microphone to sleep if "on" via sleep_timer callback every x seconds
        """
        if self._engine_modes_manager.get_mic_mode() == "on":
            self._engine_modes_manager.set_mic_mode("sleeping")

    def _reset_sleep_timer(self, words=None):
        """
        A register_recognition_callback to reset the timer for sleep_timer based on last successful recognition
        """
        self.sleep_timer.stop()
        time.sleep(0.15)
        self.sleep_timer.start()

    def _set_default_mic_mode(self):
        """
        Sets the microphone state on Caster startup.
        """
        # Only DNS supports mic_state 'off'. Substituts `sleep` mode on other engines"
        if settings.SETTINGS["engine"]["default_mic"]:  # Default is `False`
            # Default is `on`
            default_mic_state = settings.SETTINGS["engine"]["mic_mode"]
            if self.engine != "natlink" and default_mic_state == "off":
                default_mic_state = "sleep"
            self._engine_modes_manager.set_mic_mode(default_mic_state)

    def _set_engine_default_mode(self):
        """
        Sets the engine mode on Caster startup.
        """
        # Only DNS supports 'normal'. Substituts `command` mode on other engines"
        # Default is `False`
        if settings.SETTINGS["engine"]["default_engine_mode"]:
            # Default is `normal`
            default_mode = settings.SETTINGS["engine"]["engine_mode"]
            if self.engine != "natlink" and default_mode == "normal":
                default_mode = "command"
            self._engine_modes_manager.set_engine_mode(mode=default_mode, state=True)
