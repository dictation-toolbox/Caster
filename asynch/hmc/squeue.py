'''
Message queue
'''
from asynch.hmc import homunculus
from lib import control, utilities


LAST_QUERY = None

class Query:
    def __init__(self, data, callback):
        ''''''
        self.data = data
        self.callback = callback

def check_for_response():
    global LAST_QUERY
    if LAST_QUERY != None:
        data = homunculus.communicate().get_message()
        if data == None:
            return
        
        try: 
            LAST_QUERY.callback(data)
        except Exception:
            utilities.simple_log(False)
        LAST_QUERY = None
                
                
    if LAST_QUERY == None:
        control.TIMER_MANAGER.remove_callback(check_for_response)

def add_query(callback, data=None):
    global LAST_QUERY
    second = 1
    LAST_QUERY = Query({}, callback)
    control.TIMER_MANAGER.add_callback(check_for_response, second)
    
    
    
    
