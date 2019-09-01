import hashlib
import os
from threading import Lock

from castervoice.lib import printer


class BaseReloadObservable(object):
    """
    Sends signal of some sort to registered listeners
    that a file or directory needs reloading.

    Is called either by a timer or by a Dragonfly command.
    In the timer case, the lock is needed to ensure that scanning for
    updates doesn't happen while rules are being registered.
    A less flexible alternative to this would be to not allow
    the '_update' method to do anything until the GrammarManager
    has registered all the rules. However, if rules are allowed to
    be registered post-boot in the future, we'd be back to the
    same problem of needing the lock.
    """

    def __init__(self):
        self._file_hashes = {}
        self._listeners = []
        self._lock = Lock()

    def register_listener(self, listener):
        self._listeners.append(listener)

    def register_watched_file(self, file_path):
        self._lock.acquire()
        self._file_hashes[file_path] = BaseReloadObservable._get_hash_of_file(file_path)
        self._lock.release()

    def _update(self):
        self._lock.acquire()
        for file_path in self._file_hashes:
            if not os.path.exists(file_path):
                printer.out(
                    "{} appears to have been deleted or renamed. Please reboot Caster to re-track.".format(file_path))
                continue

            known_file_hash = self._file_hashes[file_path]
            current_file_hash = BaseReloadObservable._get_hash_of_file(file_path)
            if known_file_hash != current_file_hash:
                self._file_hashes[file_path] = current_file_hash
                self._notify_listeners(file_path)
        self._lock.release()

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
