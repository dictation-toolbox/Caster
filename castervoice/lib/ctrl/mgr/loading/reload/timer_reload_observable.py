from dragonfly import get_current_engine

from castervoice.lib.ctrl.mgr.loading.reload.base_reload_observable import BaseReloadObservable


class TimerReloadObservable(BaseReloadObservable):

    def __init__(self, time_in_seconds):
        """
        Timer-based file watcher. Checks for file changes every time_in_seconds.

        :param time_in_seconds: number, time between checking for updates
        """
        super(TimerReloadObservable, self).__init__()
        self._time_in_seconds = time_in_seconds

    def start(self):
        get_current_engine().create_timer(lambda: self._update(), self._time_in_seconds)
