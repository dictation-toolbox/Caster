class PrinterSpy(object):
    def __init__(self):
        self.printed = []

    def get_first(self):
        return self.printed[0]


def printer_spy():
    spy = PrinterSpy()
    from castervoice.lib import printer

    def _spy(*args):
        spy.printed.extend(args)

    printer.out = _spy

    return spy
