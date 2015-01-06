import xmlrpclib

server = xmlrpclib.ServerProxy('http://localhost:8000')
server.fclick()

if __name__ == '__main__':
    pass