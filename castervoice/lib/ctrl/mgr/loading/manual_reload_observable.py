from castervoice.lib.ctrl.mgr.loading.base_reload_observable import BaseReloadObservable

class ManualReloadObservable(BaseReloadObservable):
    
    '''TODO: set up a grammar which checks for reloads'''
    def __init__(self):
        BaseReloadObservable.__init__(self)