import numbers
import os
import sys
import threading

from xmlrpc.server import SimpleXMLRPCServer

try:  # Style C -- may be imported into Caster, or externally
    BASE_PATH = os.path.realpath(__file__).rsplit(os.path.sep + "castervoice", 1)[0]
    if BASE_PATH not in sys.path:
        sys.path.append(BASE_PATH)
finally:
    from castervoice.lib import printer
    from castervoice.lib import settings
    from castervoice.lib.merge.communication import Communicator

from PySide2 import QtCore
from PySide2.QtGui import QPalette
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QDialogButtonBox
from PySide2.QtWidgets import QCheckBox
from PySide2.QtWidgets import QDialog
from PySide2.QtWidgets import QFormLayout
from PySide2.QtWidgets import QGroupBox
from PySide2.QtWidgets import QLabel
from PySide2.QtWidgets import QLineEdit
from PySide2.QtWidgets import QScrollArea
from PySide2.QtWidgets import QTabWidget
from PySide2.QtWidgets import QVBoxLayout
from PySide2.QtWidgets import QWidget



settings.initialize()
DICT_SETTING = 1
STRING_SETTING = 2
STRING_LIST_SETTING = 4
NUMBER_LIST_SETTING = 8
NUMBER_SETTING = 16
BOOLEAN_SETTING = 32

CONTROL_KEY = QtCore.Qt.Key_Meta if sys.platform == "darwin" else QtCore.Qt.Key_Control
SHIFT_TAB_KEY = int(QtCore.Qt.Key_Tab) + 1

RPC_COMPLETE_EVENT = QtCore.QEvent.Type(QtCore.QEvent.registerEventType(-1))


class Field:
    def __init__(self, widget, original, text_type=None):
        self.children = []
        self.widget = widget
        self.original = original
        self.text_type = text_type

    def add_child(self, field):
        self.children.append(field)


class SettingsDialog(QDialog):

    def __init__(self, server):
        QDialog.__init__(self, None)
        self.modifier = 0
        self.server = server
        self.setup_xmlrpc_server()
        self.completed = False
        self.fields = []
        self.tabs = QTabWidget()
        for top in sorted(settings.SETTINGS.keys()):  # pylint: disable=no-member
            self.tabs.addTab(self.make_tab(top), top)
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButtons((int(QDialogButtonBox.StandardButton.Ok) |
                                              int(QDialogButtonBox.StandardButton.Cancel))))
        buttons.accepted.connect(self.accept)  # pylint: disable=no-member
        buttons.rejected.connect(self.reject)  # pylint: disable=no-member
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.tabs)
        mainLayout.addWidget(buttons)
        self.setLayout(mainLayout)
        self.setWindowTitle(settings.SETTINGS_WINDOW_TITLE +
                            settings.SOFTWARE_VERSION_NUMBER)
        self.expiration = threading.Timer(300, self.xmlrpc_kill)
        self.expiration.start()

    def event(self, event):
        if event.type() == QtCore.QEvent.KeyRelease:
            if self.modifier == 1:
                curr = self.tabs.currentIndex()
                tabs_count = self.tabs.count()
                if event.key() == QtCore.Qt.Key_Tab:
                    next = curr + 1
                    next = 0 if next == tabs_count else next
                    self.tabs.setCurrentIndex(next)
                    return True
                elif event.key() == SHIFT_TAB_KEY:
                    next = curr - 1
                    next = tabs_count - 1 if next == -1 else next
                    self.tabs.setCurrentIndex(next)
                    return True
        elif event.type() == RPC_COMPLETE_EVENT:
            self.completed = True
            self.hide()
            return True
        return QDialog.event(self, event)

    def keyPressEvent(self, event):
        if event.key() == CONTROL_KEY:
            self.modifier |= 1
        QDialog.keyPressEvent(self, event)

    def keyReleaseEvent(self, event):
        if event.key() == CONTROL_KEY:
            self.modifier &= ~1
        QDialog.keyReleaseEvent(self, event)

    def make_tab(self, title):
        area = QScrollArea()
        field = Field(area, title)
        area.setBackgroundRole(QPalette.Mid)
        area.setWidgetResizable(True)
        area.setWidget(self.add_fields(self, title, field))
        self.fields.append(field)
        return area

    def add_fields(self, parent, title, field):
        tab = QWidget(parent)
        form = QFormLayout()
        form.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        for label in sorted(settings.SETTINGS[title].keys()):
            value = settings.SETTINGS[title][label]
            subfield = Field(None, label)
            subfield.widget = self.field_from_value(tab, value, subfield)
            form.addRow(QLabel(label), subfield.widget)
            field.add_child(subfield)
        tab.setLayout(form)
        return tab

    def field_from_value(self, parent, value, field):
        if isinstance(value, bool):
            item = QCheckBox('')
            item.setChecked(value)
            return item
        if isinstance(value, str):
            field.text_type = STRING_SETTING
            return QLineEdit(value)
        if isinstance(value, numbers.Real):
            field.text_type = NUMBER_SETTING
            return QLineEdit(str(value))
        if isinstance(value, list):
            if isinstance(value[0], str):
                field.text_type = STRING_LIST_SETTING
                return QLineEdit(", ".join(value))
            elif isinstance(value[0], numbers.Real):
                field.text_type = NUMBER_LIST_SETTING
                return QLineEdit(", ".join((str(x) for x in value)))
        if isinstance(value, dict):
            subpage = QGroupBox(parent)
            form = QFormLayout()
            for label in sorted(value.keys()):
                subfield = Field(None, label)
                subfield.widget = self.field_from_value(subpage, value[label], subfield)
                field.add_child(subfield)
                form.addRow(QLabel(label), subfield.widget)
            subpage.setLayout(form)
            return subpage
        # This is left for bug reporting purposes.
        printer.out("{} was not assigned to {} because type {} is unknown.".format(value, parent, type(value)))
        return None

    def tree_to_dictionary(self, t=None):
        d = {}
        children = self.fields if t is None else t.children
        for field in children:
            value = None
            if isinstance(field.widget, QLineEdit):
                value = field.widget.text()
                if field.text_type == STRING_LIST_SETTING:
                    d[field.original] = [
                        x for x in value.replace(", ", ",").split(",") if x
                    ]  # don't count empty strings
                elif field.text_type == NUMBER_LIST_SETTING:
                    temp_list = (
                        float(x) for x in value.replace(", ", ",").split(",") if x
                    )  # don't count empty strings
                    d[field.original] = [int(x) if x.is_integer() else x for x in temp_list]
                elif field.text_type == NUMBER_SETTING:
                    value = float(value)
                    if value.is_integer():
                        value = int(value)
                    d[field.original] = float(value)
                else:
                    d[field.original] = value
            elif isinstance(field.widget, (QScrollArea, QGroupBox)):
                d[field.original] = self.tree_to_dictionary(field)
            elif isinstance(field.widget, QCheckBox):
                d[field.original] = field.widget.isChecked()
        return d

    def setup_xmlrpc_server(self):
        self.server.register_function(self.xmlrpc_get_message, "get_message")
        self.server.register_function(self.xmlrpc_complete, "complete")
        self.server.register_function(self.xmlrpc_kill, "kill")
        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

    def xmlrpc_kill(self):
        self.expiration.cancel()
        QApplication.quit()

    def xmlrpc_get_message(self):
        if self.completed:
            threading.Timer(1, self.xmlrpc_kill).start()
            return self.tree_to_dictionary()
        else:
            return None

    def xmlrpc_complete(self):
        QtCore.QCoreApplication.postEvent(self, QtCore.QEvent(RPC_COMPLETE_EVENT))

    def accept(self):
        self.xmlrpc_complete()

    def reject(self):
        self.xmlrpc_kill()


def main():
    server_address = (Communicator.LOCALHOST, Communicator().com_registry["hmc"])
    # Enabled by default logging causes RPC to malfunction when the GUI runs on
    # pythonw.  Explicitly disable logging for the XML server.
    server = SimpleXMLRPCServer(server_address, logRequests=False, allow_none=True)
    app = QApplication(sys.argv)
    window = SettingsDialog(server)
    window.show()
    exit_code = app.exec_()
    server.shutdown()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
