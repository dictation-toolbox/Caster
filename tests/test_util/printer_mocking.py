class PrinterSpy(object):
    def __init__(self):
        self.printed = []

    def get_first(self):
        return self.printed[0]


def printer_spy():
    from castervoice.lib import printer

    # keep original method, for cleanup
    printer_out_orig = printer.out

    # set printer.out to a spy, so we can test the output
    spy = PrinterSpy()
    def _spy(*args):
        spy.printed.extend(args)
    printer.out = _spy

    # make cleanup function
    def cleanup():
        printer.out = printer_out_orig

    return spy, cleanup
