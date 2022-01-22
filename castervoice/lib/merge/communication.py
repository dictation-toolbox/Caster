import xmlrpc.client as xmlrpclib

class Communicator:
    LOCALHOST = "127.0.0.1"

    def __init__(self):
        self.coms = {}
        self.com_registry = {
            "hmc": 8337,
            "hud": 8338,
            "grids": 8339,
            "sikuli": 8340
        }

    def get_com(self, name):
        try:  # try a ping
            return self.coms[name]
        except Exception:
            com = xmlrpclib.ServerProxy(
                "http://" + Communicator.LOCALHOST + ":" + str(self.com_registry[name]))
            self.coms[name] = com
            return com
