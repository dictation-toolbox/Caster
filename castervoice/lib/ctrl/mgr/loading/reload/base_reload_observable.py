import hashlib
import os

from castervoice.lib import printer


class BaseReloadObservable(object):
    """
    Sends signal of some sort to registered listeners
    that a file or directory needs reloading.
    """

    def __init__(self):
        self._file_hashes = {}
        self._listeners = []
        self._deleted = set()

    def register_listener(self, listener):
        self._listeners.append(listener)

    def register_watched_file(self, file_path):
        self._file_hashes[file_path] = BaseReloadObservable._get_hash_of_file(file_path)

    def _update(self):
        file_paths = set(self._file_hashes.keys())
        for file_path in file_paths:
            if not os.path.exists(file_path):
                self._print_not_found_message(file_path)
                continue

            known_file_hash = self._file_hashes[file_path]
            current_file_hash = BaseReloadObservable._get_hash_of_file(file_path)
            if known_file_hash != current_file_hash:
                self._file_hashes[file_path] = current_file_hash
                self._notify_listeners(file_path)
                printer.out("Reloaded {}".format(file_path))

    def _print_not_found_message(self, file_path):
        """
        Print the 'not found' error only once.
        """
        if file_path not in self._deleted:
            msg = "{} appears to have been deleted or renamed. Please reboot Caster to re-track."
            printer.out(msg.format(file_path))
            self._deleted.add(file_path)

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
