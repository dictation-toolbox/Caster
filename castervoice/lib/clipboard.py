from castervoice.lib import settings, printer

Clipboard = None
try:
    from dragonfly import Clipboard as DragonflyClipboard
    # Use DragonflyClipboard as Clipboard.
    Clipboard = DragonflyClipboard
except:
    printer.out("dragonfly.Clipboard failed to import.")

def _is_aenea_available():
    try:
        import aenea
        return True
    except ImportError:
        print("Unable to import aenea, dragonfly.Clipboard will be used "
              "instead.")
        return False


# Use a subclass of dragonfly's clipboard class instead if the 'use_aenea'
# setting is set to true. This will allow commands like 'stoosh' to work
# properly server-side if the RPC functions are available.
if settings.settings(["miscellaneous", "use_aenea"]) and _is_aenea_available():
    # pylint: disable=import-error
    import aenea
    from jsonrpclib import ProtocolError

    class Clipboard(DragonflyClipboard): # pylint: disable=function-redefined

        @classmethod
        def get_system_text(cls):
            # Get the server's clipboard content if possible and update this
            # system's clipboard.
            try:
                server_text = aenea.communications.server.paste()
                DragonflyClipboard.set_system_text(server_text)
                return server_text
            except ProtocolError as e:
                print("ProtocolError caught when calling server.paste(): %s"
                      % e)
                print("Only getting local clipboard content.")
                return DragonflyClipboard.get_system_text()

        @classmethod
        def set_system_text(cls, content):
            # Set the server's clipboard content if possible.
            try:
                aenea.communications.server.copy(content)
            except ProtocolError as e:
                print("ProtocolError caught when calling server.copy(): %s"
                      % e)
                print("Only setting local clipboard content.")

            # Set this system's clipboard content.
            DragonflyClipboard.set_system_text(content)
