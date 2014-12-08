'''
Message queue
'''
from asynch import homunculus
from asynch.bottleserver import Sender
from lib import control, utilities


LAST_QUERY=None
QUERY_CHECKER = Sender()
second = 1
DEFAULT_TYPE={}
DEFAULT_TYPE["qtype"]="-d"


class Query:
    def __init__(self, data, callback):
        ''''''
        self.qtype = data["qtype"]
        self.callback = callback

def check_for_response():
    global QUERY_CHECKER
    global LAST_QUERY
    if LAST_QUERY!=None:
        # response should have at least: qtype, data
        response = QUERY_CHECKER.send(homunculus.HMC_LISTENING_PORT, {}, None, True)
        if response != None and "qtype" in response:
            if LAST_QUERY.qtype == response["qtype"]:
                try: 
                    LAST_QUERY.callback(response)
                except Exception:
                    utilities.simple_log(False)
                LAST_QUERY=None
                
                
    if LAST_QUERY==None:
        control.TIMER_MANAGER.remove_callback(check_for_response)

def add_query(callback, data=None):
    global LAST_QUERY
    global DEFAULT_TYPE
    if data==None:
        data=DEFAULT_TYPE
    LAST_QUERY=Query(data, callback)
    control.TIMER_MANAGER.add_callback(check_for_response, second)