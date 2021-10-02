
class AvailableCommandsTracker(object):
    """
    This class should have NO dependencies.

    Do NOT make this more sophisticated. If you are considering doing so, you
    probably don't understand the problem as well as you think you do.

    This is nothing more than a container to set and get some formatted output.
    """

    def __init__(self):
        self._available_commands = "Available commands not set yet."

    def set_available_commands(self, commands):
        if not isinstance(commands, str):
            raise Exception("Do not set 'commands' to a non-string format.")
        self._available_commands = commands

    def get_available_commands(self):
        return self._available_commands


_INSTANCE = None


def get_instance():
    global _INSTANCE
    if _INSTANCE is None:
        _INSTANCE = AvailableCommandsTracker()
    return _INSTANCE
