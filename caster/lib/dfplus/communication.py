import xmlrpclib


class Communicator:
    LOCALHOST = "127.0.0.1"
    def __init__(self):
        self.coms = {}
        self.com_registry = {"sticky_list":     1337, 
                             "hmc":             1338, 
                             "grids":           1339, 
                             "status":          1340,
                             "sikuli":          8000
                             }
    def get_com(self, name):
        try:# try a ping
            return self.coms[name]
        except Exception:
            com = xmlrpclib.ServerProxy("http://"+Communicator.LOCALHOST+":" + str(self.com_registry[name]))
            self.coms[name] = com
            return com
