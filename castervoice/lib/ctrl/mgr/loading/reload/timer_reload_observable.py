from dragonfly import get_engine

from castervoice.lib.ctrl.mgr.loading.base_reload_observable import BaseReloadObservable


class TimerReloadObservable(BaseReloadObservable):

    def __init__(self, time_in_seconds):
        """
        Timer-based file watcher. Checks for file changes every time_in_seconds.

        :param time_in_seconds: number, time between checking for updates
        """
        BaseReloadObservable.__init__(self)
        get_engine().create_timer(lambda: self._update(), time_in_seconds)
