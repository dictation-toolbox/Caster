import sys
import PySimpleGUI27 as sg
import queue
import socket
import threading

class ThreadedServer(object):
    def __init__(self, queue, window, host, port):
        self.queue = queue
        self.window = window
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.listening = False

    def listen(self):
        self.listening = True
        t = threading.Thread(target=self._listen)
        t.daemon = True
        t.start()

    def _listen(self):
        self.sock.listen(5)
        while self.listening:
            client, address = self.sock.accept()
            client.settimeout(None)
            self.listenToClient(client, address)

    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    # Set the response to echo back the recieved data 
                    self.queue.put(str(data))
                    # print('rec'+str(data))
                    # client.send(response)
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False

class MessageWindow():

    layout = [      
            [sg.Output(size=(88, 20))],      
            [sg.InputText(focus=True)]      
            ]      

    def __init__(self):
        self.window = sg.Window('Caster', self.layout)
        self.queue = queue.Queue()
        self.server = ThreadedServer(self.queue, self.window, 'localhost', 10011)
        self.server.listen()
        self.mainloop()

    def mainloop(self):
        while True:  # Event Loop
            event, values = self.window.Read(timeout=10)
            data = ''
            while not self.queue.empty():
                data += self.queue.get()
            if data:
                print(data)
            if event is None:
                self.window.Close()
                sys.exit(0)
            # if event == 'Show':
                # Update the "output" element to be the value of "input" element
                # window.Element('_OUTPUT_').Update(values['_IN_'])
if __name__ == '__main__': 
    MessageWindow()
