import time
import unittest
import dragonfly.engines
from castervoice.lib import printer
from castervoice.lib.printer import SimplePrintMessageHandler, BaseMessageHandler, _DelegatingPrinterMessageHandler


class _PrinterArgsCapturer(object):

    def __init__(self):
        self.captured_args = []

    def _print(self, printed_line):
        self.captured_args.append(printed_line)


class TestPrinter(unittest.TestCase):

    def setUp(self):
        printer._DELEGATING_HANDLER = _DelegatingPrinterMessageHandler()
        self._delegating_handler = printer.get_delegating_handler()

    def test_handle_input_before_register(self):
        """
        Tests that printer.out will capture messages even before the delegating handler is created.
        """
        # queue up text before the handler is registered
        printer.out("some", "text")

        # create a handler with a monkey patched capturing print function
        handler = SimplePrintMessageHandler()

        args_capturer = _PrinterArgsCapturer()
        handler._print = args_capturer._print

        # register the handler
        self._delegating_handler.register_handler(handler)

        # force first message
        printer.out([])

        # assert that the handler handled the queued message
        self.assertEqual(2, len(args_capturer.captured_args))
        self.assertEqual("some\ntext", args_capturer.captured_args[0])

    def test_multiple_handlers(self):
        """
        Tests that the delegating handler can use multiple handlers.
        """
        # create several handlers with capturing print functions and register them
        handlers = []
        args_capturers = []
        for i in range(0, 2):
            handler = SimplePrintMessageHandler()
            handlers.append(handler)
            # handler._print = Mock()
            args_capturer = _PrinterArgsCapturer()
            args_capturers.append(args_capturer)

            handler._print = args_capturer._print
            self._delegating_handler.register_handler(handler)

        # queue up messages
        printer.out("some", 1)

        for i in range(0, 2):
            # assert that the handlers each handled the queued message
            self.assertEqual(1, len(args_capturers[i].captured_args))
            self.assertEqual("some\n1", args_capturers[i].captured_args[0])

    def test_broken_handler(self):
        """
        Tests that messages passed to a broken handler will still be printed to the console.
        """
        # set up arg capture on default handler
        args_capturer = _PrinterArgsCapturer()
        self._delegating_handler._error_handler._print = args_capturer._print

        # create and register a broken handler
        class BrokenHandler(BaseMessageHandler):
            def __init__(self):
                super(BrokenHandler, self).__init__()

            def handle_message(self, items):
                raise Exception("something unexpected happened")

        self._delegating_handler.register_handler(BrokenHandler())

        # queue up messages
        printer.out("asdf")

        # wait for the timer on the other thread
        time.sleep(1.5)

        # assert that the default handler still printed the message despite the error
        self.assertEqual("asdf", args_capturer.captured_args[0])
