'''
Created on Oct 7, 2015

@author: synkarius
'''
import socket
from time import sleep
import Queue

from caster.lib import settings, utilities


class StatusIntermediary:
    def __init__(self, c, t):
        self.communicator = c
        self.timer = t
        self.waiting_messages = Queue.LifoQueue()
        self.waiting_hints = Queue.LifoQueue()
    def send_entire_queue(self):
        result = ""
        is_message = False
        
        '''check for messages'''
        if not self.waiting_messages.empty():
            is_message = True
            while not self.waiting_messages.empty():
                message = self.waiting_messages.get(timeout=1)
                if self.waiting_messages.qsize() <= 5:
                    if result == "":
                        result = message
                    else:
                        result += "\n" + message 
            
        '''hints wipe out messages'''
        if not self.waiting_hints.empty():
            is_message = False
            while not self.waiting_hints.empty():
                result = self.waiting_hints.get(timeout=1)
        
        if result == "":
            self.timer.remove_callback(self.send_entire_queue)
            return
        
        if utilities.launch_status():
            sleep(2)
        
        send_function = self.communicator.get_com("status").text
        if not is_message:
            send_function = self.communicator.get_com("status").hint
        
        try:
            send_function(result)
        except Exception:
            print("problem communicating with status window:")
            utilities.simple_log()

    
    def hint(self, message):
        if settings.SETTINGS["miscellaneous"]["status_window_enabled"]:
            if self.waiting_hints.empty():
                self.timer.add_callback(self.send_entire_queue, 0.5)
            self.waiting_hints.put_nowait(message)
        else:
            print(message)
    def text(self, message):
        if settings.SETTINGS["miscellaneous"]["status_window_enabled"]:
            if self.waiting_messages.empty():
                self.timer.add_callback(self.send_entire_queue, 0.5)
            self.waiting_messages.put_nowait(message)
        else:
            print(message)
        
    def kill(self):
        if utilities.window_exists(None, settings.STATUS_WINDOW_TITLE):
            self.communicator.get_com("status").kill()
