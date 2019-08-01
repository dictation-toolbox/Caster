import hashlib


class BaseReloadObservable(object):
    """
    Sends signal of some sort to registered listeners
    that a file or directory needs reloading.

    Is called either by a timer or by a Dragonfly command.
    """

    def __init__(self):
        self._file_hashes = {}
        self._listeners = []

    def register_listener(self, listener):
        self._listeners.append(listener)

    def register_watched_file(self, file_path):
        self._file_hashes[file_path] = BaseReloadObservable._get_hash_of_file(file_path)

    def _update(self):
        for file_path in self._file_hashes:
            '''TODO: check if file still exists, print if not'''

            known_file_hash = self._file_hashes[file_path]
            current_file_hash = BaseReloadObservable._get_hash_of_file(file_path)
            if known_file_hash != current_file_hash:
                self._file_hashes[file_path] = current_file_hash
                self._notify_listeners(file_path)

    def _notify_listeners(self, path_changed):
        for listener in self._listeners:
            listener.receive(path_changed)

    @staticmethod
    def _get_hash_of_file(file_path):
        """
        Gets the hash of a file.

        :param file_path:
        :return: hex string hash
        """
        md5_hasher = hashlib.md5()
        with open(file_path, 'rb') as module:
            buf = module.read()
            md5_hasher.update(buf)
        return md5_hasher.hexdigest()
