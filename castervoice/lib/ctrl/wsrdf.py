import logging
from threading import Timer
import time


class RecognitionHistoryForWSR(list):
    '''
    Copied verbatim from Dragonfly, but doesn't require Natlink
    '''

    def __init__(self, length=10):
        list.__init__(self)

        usable_length = isinstance(length, int) and length >= 1
        if length is None or usable_length:
            self._length = length
        else:
            raise ValueError("length must be a positive int or None,"
                             " received %r." % length)

    def on_recognition(self, words):
        self._complete = True
        self.append(self._recognition_to_item(words))
        if self._length:
            while len(self) > self._length:
                self.pop(0)

    def _recognition_to_item(self, words):
        return tuple(words)


class TimerForWSR(object):
    '''
    Copied verbatim from Dragonfly, but doesn't require
    Natlink and has been those parts reimplemented    
    '''

    class Callback(object):
        def __init__(self, function, interval):
            self.function = function
            self.interval = interval
            self.next_time = time.clock() + self.interval

        def call(self):
            self.next_time += self.interval
            try:
                self.function()
            except Exception, e:
                logging.getLogger("timer").exception("Exception during timer callback")
                print("Exception during timer callback: %s (%r)" % (e, e))

    def __init__(self, interval):
        self.interval = interval
        self.callbacks = []
        self._continue = {"_continue": False}

    def add_callback(self, function, interval):
        self.callbacks.append(self.Callback(function, interval))
        if len(self.callbacks) == 1:
            self.setTimerCallback(self.callback)

    def remove_callback(self, function):
        for c in self.callbacks:
            if c.function == function: self.callbacks.remove(c)
        if len(self.callbacks) == 0:
            self.setTimerCallback(None)

    def callback(self):
        now = time.clock()
        for c in self.callbacks:
            if c.next_time < now: c.call()

    def setTimerCallback(self, callback):
        _continue = self._continue
        if callback is None:
            _continue["_continue"] = False
        else:
            _continue["_continue"] = True
            _interval = self.interval

            def call():
                if _continue["_continue"]:
                    callback()
                    Timer(_interval, call).start()

            Timer(_interval, call).start()
