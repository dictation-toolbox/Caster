'''
Sends signal of some sort to registered listeners
that a file or directory needs reloading.
'''

class BaseReloadObservable(object):
    def __init__(self):
        self._file_hashes = {}
        self._listeners = []
        
    def register_listener(self, listener):
        self._listeners.append(listener)
        
    def _notify_listeners(self, paths_changed):
        for listener in self._listeners:
            listener.receive(paths_changed)
    
    def register_watched_file(self, path):
        '''
        TODO: 
        1. plug into dragonfly timer system
        2. get hashes of files at (A) registry and (B) timer events
        3. notify listeners when hash changes
        '''
    
    '''TODO this -- check all the hashes and notify if changed'''
    def update(self):
        pass