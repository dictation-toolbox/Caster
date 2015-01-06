'''
Message queue
'''
from asynch.bottleserver import Sender
from lib import control, utilities, settings


LAST_QUERY=None
QUERY_CHECKER = Sender()



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
        response = QUERY_CHECKER.send(settings.HMC_LISTENING_PORT, {}, None, True)
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
    second = 1
    if data==None:
        data={"qtype": settings.QTYPE_DEFAULT}
    
        
    LAST_QUERY=Query(data, callback)
    control.TIMER_MANAGER.add_callback(check_for_response, second)