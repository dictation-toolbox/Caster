class HooksRunner(object):
    def __init__(self):
        self._hooks = []

    def add_hook(self, hook):
        self._hooks.append(hook)

    def execute(self, event):
        for hook in self._hooks:
            if hook.match(event.get_type()):
                hook.run(event)
