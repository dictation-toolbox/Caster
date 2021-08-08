'''
This module lives in a subprocess and communicates with the main caster process
over a multiprocessing pipe.

It's primary purpose is to show and hide the window with a list of corrections
and ensure that it contains the correct list of corrections depending on
instructions sent from the manager module.

the list of similar sounding words comes from an index that I created
and curate in the similar_sounding_words python package.
'''
from PySide2 import QtWidgets, QtCore
import similar_sounding_words
from functools import partial

try:
    # Tip: because this module runs in the subprocess its logging output gets eaten
    # `pip install q`
    # then `tail -f /c/Users/<you>/AppData/Local/Temp/q` in `git-bash`
    # See https://github.com/zestyping/q for more useful stuff
    import q

    print = q
except ImportError:
    pass

def window_manager(pipe):
    '''
    Entry-point for the subprocess. Initializes a Qt application, but does not
    show the window. This function is called at program startup.
    '''
    qtapp = QtWidgets.QApplication()
    app = App(pipe, qtapp)
    qtapp.exec_()



class App(QtCore.QObject):
    '''
    Main QT application that sets up the window and the thread that listens
    for instructions from the multiprocessing pipe.
    '''
    def __init__(self, pipe, parent=None):
        super().__init__(parent)

        self.window = Window()
        self.pipe_loop = PipeLoop(pipe)
        self.window.cancelClicked.connect(self.pipe_loop.cancel)
        self.window.clickChoice.connect(self.pipe_loop.setChoice)
        self.pipe_loop.setChoices.connect(self.window.setChoices)
        self.pipe_loop.showWindow.connect(self.window.show)
        self.pipe_loop.hideWindow.connect(self.window.hide)
        self.parent().aboutToQuit.connect(self.forceLoopQuit)

        self.pipe_loop.start()

    def forceLoopQuit(self):
        '''
        Make sure we don't keep any threads hanging around if we unexpectedly quit.
        '''
        if self.pipe_loop.isRunning():
            self.pipe_loop.terminate()
            self.pipe_loop.wait()


class PipeLoop(QtCore.QThread):
    '''
    QT worker thread that just listens for instructions from the pipe and emits
    QT signals to the window when it receives them.
    '''
    setChoices = QtCore.Signal(list)
    showWindow = QtCore.Signal()
    hideWindow = QtCore.Signal()

    def __init__(self, pipe, parent=None):
        super().__init__(parent)
        self.pipe = pipe

    def run(self):
        choices = []
        while True:
            (message_type, message) = self.pipe.recv()
            print(
                f"Received corrections window message {message_type}, {message}"
            )
            if message_type == "SELECT CHOICE":
                choice_index = message - 1
                if choice_index < len(choices):
                    self.pipe.send(("CHOICE", choices[choice_index]))
                    choices = []
                    self.hideWindow.emit()
            elif message_type == "SHOW WINDOW":
                choices = get_choices(message)
                self.setChoices.emit(choices)
                self.showWindow.emit()
            elif message_type == "CANCEL":
                self.hideWindow.emit()
                choices = []

    @QtCore.Slot()
    def cancel(self):
        self.pipe.send(("CANCEL", ""))

    @QtCore.Slot()
    def setChoice(self, text):
        print("got choice", text)
        self.pipe.send(("CHOICE", text))
        self.hideWindow.emit()


class Window(QtWidgets.QDialog):
    '''
    The correction window is instantiated on program startup, but it does not
    get displayed until the user has requested a correction.
    '''
    cancelClicked = QtCore.Signal()
    clickChoice = QtCore.Signal(str)

    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setWindowTitle("Remedy")
        self.setAttribute(QtCore.Qt.WA_QuitOnClose, False)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)

    @QtCore.Slot(str, list)
    def setChoices(self, choices):
        '''
        When the user has requested a correction, we need to display the choices
        in a window. It each word that can be displayed comes in three flavours
        based on desired capitalization. We use QTs rich text formatting
        to display the first of each group in bold and insert a newline
        after the third member of the group so it's easier to visually scan
        for the desired correction.

        This lot is connected to the `setChoices` signal on the PipeLoop.
        '''
        clearLayout(self.layout)
        for i, choice in enumerate(choices):
            label = QtWidgets.QPushButton(f"{i+1}. {choice}")
            if i % 3 == 0:
                label.setStyleSheet("font:bold;border-style:none")
            elif i % 3 == 2:
                label.setStyleSheet("padding-bottom:5ex;border-style:none")
            else:
                label.setStyleSheet("border-style:none")
            label.clicked.connect(partial(self.clickChoice.emit, choice))
            self.layout.addWidget(label, i % 9, i // 9, 1, 1)

    def reject(self):
        '''
        Called when the user manually closes the window using the X button.
        '''
        print("Dialogue closed")
        self.hide()
        self.cancelClicked.emit()


def clearLayout(layout):
    '''
    Helper function to remove all of the children from the window
    before displaying the new choices. It is astonishing that QT does not have
    built-in support for this.
    '''
    child = layout.takeAt(0)
    while child:
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())
        child = layout.takeAt(0)


def get_choices(selection):
    '''
    Look up related words in the similar sounding words index and create a
    group of choices based on these words. Each word gets three options
    for the three different capitalization levels (lower, UPPER, and Title).
    '''
    selection = selection.lower()
    alternates = [selection] + similar_sounding_words.index.get(selection, [])
    capitalizations = (
        (word.lower(), word.title(), word.upper()) for word in alternates
    )
    return [word for capitalization in capitalizations for word in capitalization]



# super dirty test sequence so I don't have to restart caster for every bug
if __name__ == "__main__":
    import multiprocessing, time

    (PIPE, SUB_PIPE) = multiprocessing.Pipe()
    process = multiprocessing.Process(
        target=window_manager, args=(SUB_PIPE,), daemon=True
    )
    process.start()
    print("Process is running")
    print("Process is running")
    PIPE.send(("SHOW WINDOW", "or"))
    time.sleep(10)
    print("Sending select choice")
    PIPE.send(("SELECT CHOICE", 2))
    time.sleep(2)
    print("waiting for something")
    print(PIPE.recv())
    print(" trying to send show window again")
    PIPE.send(("SHOW WINDOW", "other"))
    time.sleep(2)
    print("sending a cancel")
    PIPE.send(("CANCEL", ""))
    time.sleep(2)
