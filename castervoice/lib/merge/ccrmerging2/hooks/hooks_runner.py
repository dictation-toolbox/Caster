from castervoice.lib import printer


class HooksRunner(object):
    def __init__(self):
        self._hooks = []

    def add_hook(self, hook):
        self._hooks.append(hook)

    def execute(self, event):
        for hook in self._hooks:
            if hook.match(event.get_type()):
                try:
                    hook.run(event)
                except:
                    err = "Error while running hook {} with {} event."
                    printer.out(err.format(hook, event.get_type()))
