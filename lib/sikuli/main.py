'''
Created on Jan 3, 2015

@author: dave
'''

import SimpleXMLRPCServer
import time
import xmlrpclib


t1=time.time()
server = xmlrpclib.ServerProxy('http://localhost:8000')
server.fclick()
# print 'Ping:', server.add(4, 4)
t2=time.time()

print t2-t1

if __name__ == '__main__':
    pass