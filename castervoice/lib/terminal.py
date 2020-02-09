from dragonfly import RunCommand, Function
from castervoice.lib.merge.state.actions2 import ConfirmAction

class TerminalCommand(RunCommand):
    '''
    TerminalCommand executes trusted or un-trusted RunCommands for terminal or CMD.
    Trusted commands not utilize Confirm Action to safeguard RunCommand execution.

    Example 1 - A trusted command
    class PingLocalHost(TerminalCommand):
        command = "ping localhost"
        trusted = True
    Ping().execute()

    Example 2 - A synchronous command
    "update caster test":
        R(TerminalCommand('python -m pip install --upgrade castervoice', synchronous=True),
          rdescript="Core: Update"),

    '''
    trusted = False
    def __init__(self, command=None, process_command=None,
                 synchronous=False, trusted=False):
        # Pass arguments to RunCommand.
        RunCommand.__init__(self, command, process_command, synchronous)

        # Allow setting 'trusted' at the class level.
        if trusted:
            self.trusted = trusted

    def execute(self, data=None):
        if self.trusted:
            return RunCommand.execute(self, data)
        else:
            return ConfirmAction(
                Function(lambda: RunCommand.execute(self, data)),
                rdescript="CasterTerminalCommand: Confirm Action '%s'?" % self.command,
                instructions="Run command '%s'?" % self.command
            ).execute(data)

