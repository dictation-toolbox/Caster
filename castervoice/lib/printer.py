from __future__ import print_function
from queue import Queue

_QUEUE = Queue()


def out(*args):
    """
    Queues up a message to be printed or otherwise handled.
    """
    _QUEUE.put(args)


def get_delegating_handler():
    return _DelegatingPrinterMessageHandler()


class _DelegatingPrinterMessageHandler(object):
    _ONE_SECOND = 1

    def __init__(self):
        self._queue = _QUEUE
        self._handlers = []
        self._timer = None
        self._default_handler = SimplePrintMessageHandler()

    def register_handler(self, handler):
        self._handlers.append(handler)

    def start(self):
        from dragonfly import get_engine
        self._timer = get_engine() \
            .create_timer(lambda: self._consume_queue(), _DelegatingPrinterMessageHandler._ONE_SECOND)

    def _consume_queue(self):
        """
        Dumps out the queue if it has any handlers and processes queued messages.
        """

        if len(self._handlers) > 0:
            messages = []
            while self._queue.qsize() > 0:
                messages.append(self._queue.get())

            for message in messages:
                for handler in self._handlers:
                    try:
                        handler.handle_message(message)
                    except:
                        self._default_handler.handle_message(message)


class BaseMessageHandler(object):

    def handle_message(self, items):
        """
        Child classes should implement this,
        doing something with the 'items' list.
        Each 'item' in the list is an object which
        was passed to printer.out as one of its *args.
        """
        from castervoice.lib.ctrl.mgr.errors.base_class_error import DontUseBaseClassError
        raise DontUseBaseClassError(self)


class SimplePrintMessageHandler(BaseMessageHandler):
    """
    A simple message handler which only prints messages to the console,
    newline-delimited.
    """

    def __init__(self):
        super(SimplePrintMessageHandler, self).__init__()
        self._print = print

    def handle_message(self, items):
        self._print("\n".join([str(m) for m in items]))
