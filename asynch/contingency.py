'''
Created on Nov 15, 2014

@author: dave
'''
from collections import namedtuple
import json
import os
import signal
from threading import Timer
import time

from bottle import run, request
import bottle


        
class ContingencyServer:
    class Message:
        def __init__(self, content="", destination=0):
            self.content = content
            self.destination = destination
        
    def __init__(self, listening_port):
        self.listening_port = listening_port
        self.message_queue = []
        bottle.route('/process', method="POST")(self.process_request)
        run(host='localhost', port=self.listening_port, debug=False, server='cherrypy')        
    
    def process_request(self):
        request_object = json.loads(request.body.read())
        action_type = request_object["action_type"]
    
    

c = ContingencyServer(1338)
# TkTransparent("test", namedtuple("test", "width height x y")(width=400,height=300, x=0, y=0))
