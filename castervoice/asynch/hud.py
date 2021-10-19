#! python
'''
Caster HUD Window module
'''
# pylint: disable=import-error,no-name-in-module
import html
import json
import os
import signal
import sys
import threading
import PySide2.QtCore
import PySide2.QtGui
import dragonfly
from xmlrpc.server import SimpleXMLRPCServer
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QMainWindow
from PySide2.QtWidgets import QTextEdit
from PySide2.QtWidgets import QTreeView
from PySide2.QtWidgets import QVBoxLayout
from PySide2.QtWidgets import QWidget
try:  # Style C -- may be imported into Caster, or externally
    BASE_PATH = os.path.realpath(__file__).rsplit(os.path.sep + "castervoice", 1)[0]
    if BASE_PATH not in sys.path:
        sys.path.append(BASE_PATH)
finally:
    from castervoice.lib.merge.communication import Communicator
    from castervoice.lib import settings

CLEAR_HUD_EVENT = PySide2.QtCore.QEvent.Type(PySide2.QtCore.QEvent.registerEventType(-1))
HIDE_HUD_EVENT = PySide2.QtCore.QEvent.Type(PySide2.QtCore.QEvent.registerEventType(-1))
SHOW_HUD_EVENT = PySide2.QtCore.QEvent.Type(PySide2.QtCore.QEvent.registerEventType(-1))
HIDE_RULES_EVENT = PySide2.QtCore.QEvent.Type(PySide2.QtCore.QEvent.registerEventType(-1))
SHOW_RULES_EVENT = PySide2.QtCore.QEvent.Type(PySide2.QtCore.QEvent.registerEventType(-1))
SEND_COMMAND_EVENT = PySide2.QtCore.QEvent.Type(PySide2.QtCore.QEvent.registerEventType(-1))


class RPCEvent(PySide2.QtCore.QEvent):

    def __init__(self, type, text):
        PySide2.QtCore.QEvent.__init__(self, type)
        self._text = text

    @property
    def text(self):
        return self._text


class RulesWindow(QWidget):

    _WIDTH = 600
    _MARGIN = 30

    def __init__(self, text):
        QWidget.__init__(self, f=(PySide2.QtCore.Qt.WindowStaysOnTopHint))
        x = dragonfly.monitors[0].rectangle.dx - (RulesWindow._WIDTH + RulesWindow._MARGIN)
        y = 300
        dx = RulesWindow._WIDTH
        dy = dragonfly.monitors[0].rectangle.dy - (y + 2 * RulesWindow._MARGIN)
        self.setGeometry(x, y, dx, dy)
        self.setWindowTitle("Active Rules")
        rules_tree = PySide2.QtGui.QStandardItemModel()
        rules_tree.setColumnCount(2)
        rules_tree.setHorizontalHeaderLabels(['phrase', 'action'])
        rules_dict = json.loads(text)
        rules = rules_tree.invisibleRootItem()
        for g in rules_dict:
            gram = PySide2.QtGui.QStandardItem(g["name"]) if len(g["rules"]) > 1 else None
            for r in g["rules"]:
                rule = PySide2.QtGui.QStandardItem(r["name"])
                rule.setRowCount(len(r["specs"]))
                rule.setColumnCount(2)
                row = 0
                for s in r["specs"]:
                    phrase, _, action = s.partition('::')
                    rule.setChild(row, 0, PySide2.QtGui.QStandardItem(phrase))
                    rule.setChild(row, 1, PySide2.QtGui.QStandardItem(action))
                    row += 1
                if gram is None:
                    rules.appendRow(rule)
                else:
                    gram.appendRow(rule)
            if gram:
                rules.appendRow(gram)
        tree_view = QTreeView(self)
        tree_view.setModel(rules_tree)
        tree_view.setColumnWidth(0, RulesWindow._WIDTH / 2)
        layout = QVBoxLayout()
        layout.addWidget(tree_view)
        self.setLayout(layout)


class HUDWindow(QMainWindow):

    _WIDTH = 300
    _HEIGHT = 200
    _MARGIN = 30

    def __init__(self, server):
        QMainWindow.__init__(self, flags=(PySide2.QtCore.Qt.WindowStaysOnTopHint))
        x = dragonfly.monitors[0].rectangle.dx - (HUDWindow._WIDTH + HUDWindow._MARGIN)
        y = HUDWindow._MARGIN
        dx = HUDWindow._WIDTH
        dy = HUDWindow._HEIGHT
        self.server = server
        self.setup_xmlrpc_server()
        self.setGeometry(x, y, dx, dy)
        self.setWindowTitle(settings.HUD_TITLE)
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.setCentralWidget(self.output)
        self.rules_window = None
        self.commands_count = 0

    def event(self, event):
        if event.type() == SHOW_HUD_EVENT:
            self.show()
            return True
        if event.type() == HIDE_HUD_EVENT:
            self.hide()
            return True
        if event.type() == SHOW_RULES_EVENT:
            self.rules_window = RulesWindow(event.text)
            self.rules_window.show()
            return True
        if event.type() == HIDE_RULES_EVENT and self.rules_window:
            self.rules_window.close()
            self.rules_window = None
            return True
        if event.type() == SEND_COMMAND_EVENT:
            escaped_text = html.escape(event.text)
            if escaped_text.startswith('$'):
                formatted_text = '<font color="blue">&lt;</font><b>{}</b>'.format(escaped_text[1:])
                if self.commands_count == 0:
                    self.output.setHtml(formatted_text)
                else:
                    # self.output.append('<br>')
                    self.output.append(formatted_text)
                cursor = self.output.textCursor()
                cursor.movePosition(PySide2.QtGui.QTextCursor.End)
                self.output.setTextCursor(cursor)
                self.output.ensureCursorVisible()
                self.commands_count += 1
                if self.commands_count == 50:
                    self.commands_count = 0
                return True
            if escaped_text.startswith('@'):
                formatted_text = '<font color="purple">&gt;</font><b>{}</b>'.format(escaped_text[1:])
            elif escaped_text.startswith(''):
                formatted_text = '<font color="red">&gt;</font>{}'.format(escaped_text)
            else:
                formatted_text = escaped_text
            self.output.append(formatted_text)
            self.output.ensureCursorVisible()
            return True
        if event.type() == CLEAR_HUD_EVENT:
            self.commands_count = 0
            return True
        return QMainWindow.event(self, event)

    def closeEvent(self, event):
        event.accept()

    def setup_xmlrpc_server(self):
        self.server.register_function(self.xmlrpc_clear, "clear_hud")
        self.server.register_function(self.xmlrpc_ping, "ping")
        self.server.register_function(self.xmlrpc_hide_hud, "hide_hud")
        self.server.register_function(self.xmlrpc_hide_rules, "hide_rules")
        self.server.register_function(self.xmlrpc_kill, "kill")
        self.server.register_function(self.xmlrpc_send, "send")
        self.server.register_function(self.xmlrpc_show_hud, "show_hud")
        self.server.register_function(self.xmlrpc_show_rules, "show_rules")
        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.daemon = True
        server_thread.start()


    def xmlrpc_clear(self):
        PySide2.QtCore.QCoreApplication.postEvent(self, PySide2.QtCore.QEvent(CLEAR_HUD_EVENT))
        return 0

    def xmlrpc_ping(self):
        return 0

    def xmlrpc_hide_hud(self):
        PySide2.QtCore.QCoreApplication.postEvent(self, PySide2.QtCore.QEvent(HIDE_HUD_EVENT))
        return 0

    def xmlrpc_show_hud(self):
        PySide2.QtCore.QCoreApplication.postEvent(self, PySide2.QtCore.QEvent(SHOW_HUD_EVENT))
        return 0

    def xmlrpc_hide_rules(self):
        PySide2.QtCore.QCoreApplication.postEvent(self, PySide2.QtCore.QEvent(HIDE_RULES_EVENT))
        return 0

    def xmlrpc_kill(self):
        QApplication.quit()

    def xmlrpc_send(self, text):
        PySide2.QtCore.QCoreApplication.postEvent(self, RPCEvent(SEND_COMMAND_EVENT, text))
        return len(text)

    def xmlrpc_show_rules(self, text):
        PySide2.QtCore.QCoreApplication.postEvent(self, RPCEvent(SHOW_RULES_EVENT, text))
        return len(text)


def handler(signum, frame):
    """
    This handler doesn't stop the application when ^C is pressed,
    but it prevents exceptions being thrown when later
    the application is terminated from GUI.  Normally, HUD is started
    by the recognition process and can't be killed from shell prompt,
    in which case this handler is not needed.
    """
    pass


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    server_address = (Communicator.LOCALHOST, Communicator().com_registry["hud"])
    # allow_none=True means Python constant None will be translated into XML
    server = SimpleXMLRPCServer(server_address, logRequests=False, allow_none=True)
    app = QApplication(sys.argv)
    window = HUDWindow(server)
    window.show()
    exit_code = app.exec_()
    server.shutdown()
    sys.exit(exit_code)
