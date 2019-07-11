from castervoice.lib.ctrl.mgr.loading.base_reload_observable import BaseReloadObservable


class FileWatcherObservable(BaseReloadObservable):
    '''TODO: set up a timer that calls update'''

    def __init__(self):
        BaseReloadObservable.__init__(self)
