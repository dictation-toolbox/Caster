import json
import os
import signal
import sys

from bottle import run, request
import bottle


class BottleServer:
    class Message:
        def __init__(self, content="", destination=""):
            self.content = content
            self.destination = destination
        
    def __init__(self, listening_port):
        self.listening_port = listening_port
        self.mpserver = None
        self.incoming = []
        self.outgoing = []
        bottle.route('/process', method="POST")(self.receive_request)
        run(host='localhost', port=self.listening_port, debug=False)#, server='cherrypy'
    
    def receive_request(self):
        self.incoming.append(json.loads(request.body.read()))
        #self.request_object = json.loads(request.body.read())
        #action_type = self.request_object["action_type"]
    
    def process_requests(self):
        '''virtual method'''
        
    def die(self):
        self.shutdown()
    
    

    def setup_monkey_patch_for_server_shutdown(self):
        """Setup globals to steal access to the server reference.                                                             
        This is required to initiate shutdown, unfortunately.                                                                 
        (Bottle could easily remedy that.)"""
    
        # Save the original function.                                                                                         
        from wsgiref.simple_server import make_server
    
        # Create a decorator that will save the server upon start.                                                            
        def stealing_make_server(*args, **kw):
            self.mpserver = make_server(*args, **kw)
            return self.mpserver
    
        # Patch up wsgiref itself with the decorated function.                                                                
        import wsgiref.simple_server
        wsgiref.simple_server.make_server = stealing_make_server



    def shutdown(self):
        """Request for the server to shutdown."""
        self.mpserver.shutdown()