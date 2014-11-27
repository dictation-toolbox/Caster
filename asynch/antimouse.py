'''
Created on Nov 15, 2014

@author: dave
'''
import json

from bottle import run, request
import bottle


        
class BottleServer:
    class Message:
        def __init__(self, content="", destination=0):
            self.content = content
            self.destination = destination
        
    def __init__(self, listening_port):
        self.listening_port = listening_port
        self.message_queue = []
        bottle.route('/process', method="POST")(self.process_request)
        run(host='localhost', port=self.listening_port, debug=False, server='cherrypy')        
    
    def receive_request(self):
        self.request_object = json.loads(request.body.read())
        #action_type = self.request_object["action_type"]
    
    def process_request(self):
        '''virtual method'''
    
    

#c = BottleServer(1338)
