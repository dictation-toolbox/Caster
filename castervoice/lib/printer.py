import logging


_log = logging.getLogger("caster")


def out(*args):
    """
    Use this as a printing interface to send messages to places other than the console.
    DO NOT import anything in this class. Use *args.
    """
    _log.debug("\n".join([str(o) for o in args]))
