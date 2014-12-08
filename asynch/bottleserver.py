import httplib
import json
from threading import Timer
import threading

from bottle import run, request
import bottle

'''
        formatted_data={}
        listening_port=None
        if destination=="legion":
            from asynch import legion
            listening_port=legion.LEGION_LISTENING_PORT
            ''''''
            if dtype=="scan":
                formatted_data["data_tirg"]=data[0]
                formatted_data["data_rex"]=data[1]
                formatted_data["redraw"]=True
        elif destination=="antimouse":
            listening_port=legion.LEGION_LISTENING_PORT
            if dtype=="req_tirg_update":
                formatted_data["origin"]="legion"
                formatted_data["type"]="req_tirg_update"
'''
class Sender:
    def __init__(self, report=False):
        self.report=report
    def send(self, destination, data,dtype=None,  response_required=False):
        try:
            c = httplib.HTTPConnection('localhost', destination)
            c.request('POST', '/process', json.dumps(data))
            if response_required:
                r = json.loads(c.getresponse().read())
                return r
        except Exception:
            if self.report:
                from lib import utilities
                utilities.simple_log(False)
            
        return None

class BottleServer:
    class Message:
        def __init__(self, content="", destination=""):
            self.content = content
            self.destination = destination
            self.sender= Sender()
        
    def __init__(self, listening_port, lock=None):
        self.listening_port = listening_port
        self.lock = threading.Lock() if lock == None else lock
        self.incoming = []
        self.outgoing = []
        bottle.route('/process', method="POST")(self.receive_request)
        # make it nonblocking:
        Timer(0.1, self.start_run).start()
        
    def start_run(self):
        run(host='localhost', port=self.listening_port, debug=False, server='cherrypy')
    
    def receive_request(self):
        with self.lock: 
            self.incoming.append(json.loads(request.body.read()))
            # self.request_object = json.loads(request.body.read())
            # action_type = self.request_object["action_type"]
    
    def process_requests(self):
        '''override this'''

    def send(self, destination, data,dtype=None,  response_required=False):
        return self.sender.send(destination, data, dtype, response_required)








