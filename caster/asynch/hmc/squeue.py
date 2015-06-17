'''
Message queue
'''
from caster.lib import control, utilities


LAST_QUERY = None
TRIES=0

class Query:
    def __init__(self, data, callback):
        ''''''
        self.data = data
        self.callback = callback

def check_for_response():
    global LAST_QUERY, TRIES
    if LAST_QUERY != None:
        data = None
        try: 
            data = control.nexus().comm.get_com("hmc").get_message()
        except Exception:
            TRIES+=1
            if TRIES>9:
                TRIES=0
                control.nexus().timer.remove_callback(check_for_response)
                return
        
        if data == None:
            return
        
        try: 
            LAST_QUERY.callback(data)
        except Exception:
            utilities.simple_log(False)
        LAST_QUERY = None
                
                
    if LAST_QUERY == None:
        control.nexus().timer.remove_callback(check_for_response)

def add_query(callback, data=None):
    global LAST_QUERY
    second = 1
    LAST_QUERY = Query({}, callback)
    control.nexus().timer.add_callback(check_for_response, second)
    
    
    
    
