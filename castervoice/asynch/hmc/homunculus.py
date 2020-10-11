import os
import sys
import threading

import dragonfly

# TODO: Remove this try wrapper when CI server supports Qt
try:
    import PySide2.QtCore
    from PySide2.QtWidgets import QApplication
    from PySide2.QtWidgets import QCheckBox
    from PySide2.QtWidgets import QDialog
    from PySide2.QtWidgets import QFileDialog
    from PySide2.QtWidgets import QFormLayout
    from PySide2.QtWidgets import QLabel
    from PySide2.QtWidgets import QLineEdit
    from PySide2.QtWidgets import QScrollArea
    from PySide2.QtWidgets import QTextEdit
    from PySide2.QtWidgets import QVBoxLayout
    from PySide2.QtWidgets import QWidget
except ImportError:
    sys.exit(0)

try:  # Style C -- may be imported into Caster, or externally
    BASE_PATH = os.path.realpath(__file__).rsplit(os.path.sep + "castervoice", 1)[0]
    if BASE_PATH not in sys.path:
        sys.path.append(BASE_PATH)
finally:
    from castervoice.lib import settings

RPC_DIR_EVENT = PySide2.QtCore.QEvent.Type(PySide2.QtCore.QEvent.registerEventType(-1))


class Homunculus(QDialog):

    def __init__(self, server, args):
        QDialog.__init__(self, None)
        self.htype = args[1]
        self.completed = False
        self.server = server
        self.setup_xmlrpc_server()
        self.mainLayout = QVBoxLayout()
        found_word = None
        if len(args) > 2:
            found_word = args[2]
        if self.htype == settings.QTYPE_DEFAULT:
            self.setup_base_window()
        elif self.htype == settings.QTYPE_INSTRUCTIONS:
            self.setup_base_window(found_word)
        elif self.htype == settings.QTYPE_CONFIRM:
            self.setup_confirm_window(found_word)
        elif self.htype == settings.QTYPE_DIRECTORY:
            self.setup_directory_window()
        elif self.htype == settings.QTYPE_RECORDING:
            self.setup_recording_window(found_word)
        self.setLayout(self.mainLayout)
        self.expiration = threading.Timer(300, self.xmlrpc_kill)
        self.expiration.start()

    def setup_base_window(self, data=None):
        x = dragonfly.monitors[0].rectangle.dx / 2 - 150
        y = dragonfly.monitors[0].rectangle.dy / 2 - 100
        self.setGeometry(x, y, 300, 200)
        self.setWindowTitle(settings.HOMUNCULUS_VERSION)
        self.data = data.split("|") if data else [0, 0]
        label = QLabel(" ".join(self.data[0].split(settings.HMC_SEPARATOR))) if data else QLabel("Enter response then say 'complete'")  # pylint: disable=no-member
        label.setAlignment(PySide2.QtCore.Qt.AlignCenter)
        self.ext_box = QTextEdit()
        self.mainLayout.addWidget(label)
        self.mainLayout.addWidget(self.ext_box)
        self.setWindowTitle(settings.HOMUNCULUS_VERSION)

    def setup_confirm_window(self, params):
        x = dragonfly.monitors[0].rectangle.dx / 2 - 160
        y = dragonfly.monitors[0].rectangle.dy / 2 - 25
        self.setGeometry(x, y, 320, 50)
        self.setWindowTitle(settings.HOMUNCULUS_VERSION + settings.HMC_TITLE_CONFIRM)
        label1 = QLabel("Please confirm: " + " ".join(params.split(settings.HMC_SEPARATOR)))
        label2 = QLabel("(say \"confirm\" or \"disconfirm\")")
        self.mainLayout.addWidget(label1)
        self.mainLayout.addWidget(label2)

    def setup_directory_window(self):
        x = dragonfly.monitors[0].rectangle.dx / 2 - 320
        y = dragonfly.monitors[0].rectangle.dy / 2 - 25
        self.setGeometry(x, y, 640, 50)
        self.setWindowTitle(settings.HOMUNCULUS_VERSION + settings.HMC_TITLE_DIRECTORY)
        label = QLabel("Enter directory or say 'browse'")
        self.word_box = QLineEdit()
        label.setBuddy(self.word_box)
        self.mainLayout.addWidget(label)
        self.mainLayout.addWidget(self.word_box)

    def setup_recording_window(self, history):
        self.grid_row = 0
        x = dragonfly.monitors[0].rectangle.dx / 2 - 320
        y = dragonfly.monitors[0].rectangle.dy / 2 - 240
        self.setGeometry(x, y, 640, 480)
        self.setWindowTitle(settings.HOMUNCULUS_VERSION + settings.HMC_TITLE_RECORDING)
        label = QLabel("Macro Recording Options")
        label.setAlignment(PySide2.QtCore.Qt.AlignCenter)
        self.mainLayout.addWidget(label)
        label = QLabel("Command Words:")
        self.word_box = QLineEdit()
        label.setBuddy(self.word_box)
        self.mainLayout.addWidget(label)
        self.mainLayout.addWidget(self.word_box)
        self.repeatable = QCheckBox("Make Repeatable")
        self.mainLayout.addWidget(self.repeatable)
        label = QLabel("Dictation History")
        label.setAlignment(PySide2.QtCore.Qt.AlignCenter)
        self.mainLayout.addWidget(label)
        self.word_state = []
        cb_number = 1
        sentences = history.split("[s]")
        sentences.pop()
        form = QFormLayout()
        for sentence in sentences:
            sentence_words = sentence.split("[w]")
            sentence_words.pop()
            display_sentence = " ".join(sentence_words)
            cb = QCheckBox("(" + str(cb_number) + ")")
            form.addRow(QLabel(display_sentence), cb)
            self.word_state.append(cb)
            cb_number += 1
        self.word_state[0].setChecked(True)
        self.cb_max = cb_number
        area = QScrollArea(self)
        area.setWidgetResizable(True)
        group = QWidget(area)
        group.setLayout(form)
        area.setWidget(group)
        self.mainLayout.addWidget(area)

    def check_boxes(self, details):
        for box_index in details:
            if 0 < box_index and box_index < self.cb_max:
                self.word_state[box_index - 1].setChecked(True)

    def check_range_of_boxes(self, details):
        box_index_from = details[0] - 1
        box_index_to = details[1]
        for i in range(max(0, box_index_from), min(box_index_to, self.cb_max - 1)):
            self.word_state[i].setChecked(True)

    def ask_directory(self):
        result = QFileDialog.getExistingDirectory(self, "Please select directory", os.environ["HOME"], QFileDialog.ShowDirsOnly)
        self.word_box.setText(result)

    def event(self, event):
        if event.type() == RPC_DIR_EVENT:
            self.ask_directory()
            return True
        return QDialog.event(self, event)

    def reject(self):
        self.expiration.cancel()
        QApplication.quit()

    '''
    XMLRPC methods
    '''

    def setup_xmlrpc_server(self):
        self.server.register_function(self.xmlrpc_kill, "kill")
        self.server.register_function(self.xmlrpc_complete, "complete")
        if self.htype == settings.QTYPE_DEFAULT or self.htype == settings.QTYPE_INSTRUCTIONS:
            self.server.register_function(self.xmlrpc_do_action, "do_action")
            self.server.register_function(self.xmlrpc_get_message, "get_message")
        elif self.htype == settings.QTYPE_CONFIRM:
            self.server.register_function(self.xmlrpc_do_action_confirm, "do_action")
            self.server.register_function(self.xmlrpc_get_message_confirm, "get_message")
        elif self.htype == settings.QTYPE_DIRECTORY:
            self.server.register_function(self.xmlrpc_do_action_directory, "do_action")
            self.server.register_function(self.xmlrpc_get_message_directory, "get_message")
        elif self.htype == settings.QTYPE_RECORDING:
            self.server.register_function(self.xmlrpc_do_action_recording, "do_action")
            self.server.register_function(self.xmlrpc_get_message_recording, "get_message")
        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

    def xmlrpc_kill(self):
        self.expiration.cancel()
        QApplication.quit()

    def xmlrpc_complete(self):
        self.completed = True
        threading.Timer(10, self.xmlrpc_kill).start()

    def xmlrpc_do_action(self, action, details=None):
        pass

    def xmlrpc_get_message(self):
        response = None
        if self.completed:
            response = [self.ext_box.toPlainText(), self.data]
            threading.Timer(1, self.xmlrpc_kill).start()
        return response

    def xmlrpc_do_action_confirm(self, action, details=None):
        if isinstance(action, bool):
            self.completed = True
            '''1 is True, 2 is False'''
            self.value = 1 if action else 2

    def xmlrpc_get_message_confirm(self):
        response = None
        if self.completed:
            response = {"mode": "confirm"}
            response["confirm"] = self.value
            threading.Timer(1, self.xmlrpc_kill).start()
        return response

    def xmlrpc_do_action_directory(self, action, details=None):
        if action == "dir":
            PySide2.QtCore.QCoreApplication.postEvent(self, PySide2.QtCore.QEvent(RPC_DIR_EVENT))

    def xmlrpc_get_message_directory(self):
        response = None
        if self.completed:
            response = {"mode": "ask_dir"}
            response["path"] = self.word_box.text()
            threading.Timer(1, self.xmlrpc_kill).start()
        return response

    def xmlrpc_do_action_recording(self, action, details=None):
        '''acceptable keys are numbers and w and p'''
        if action == "check":
            self.check_boxes(details)
        elif action == "focus":
            if details == "word":
                self.word_box.setFocus()
        elif action == "check_range":
            self.check_range_of_boxes(details)
        elif action == "exclude":
            box_index = details
            if 0 < box_index and box_index < self.cb_max:
                self.word_state[box_index - 1].setChecked(False)
        elif action == "repeatable":
            self.repeatable.setChecked(not self.repeatable.isChecked())

    def xmlrpc_get_message_recording(self):
        response = None
        if self.completed:
            word = self.word_box.text()
            if len(word) > 0:
                response = {"mode": "recording"}
                response["word"] = word
                response["repeatable"] = self.repeatable.isChecked()
                selected_indices = []
                index = 0
                for ws in self.word_state:
                    if ws.isChecked():
                        selected_indices.append(index)
                    index += 1
                response["selected_indices"] = selected_indices
                if len(selected_indices) == 0:
                    response = None
            threading.Timer(1, self.xmlrpc_kill).start()
        return response
