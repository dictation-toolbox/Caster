'''
Created on Feb 16, 2015

@author: dave
'''
# def speaking_decorator(f):
#     ''''''
from dragonfly.grammar.rule_compound import CompoundRule

class speaking_decorator(object):

    def __init__(self, f):
        self.f = f
        self.__name__ = f.__name__
        if hasattr(self, 'level'):
            self.level += 1
        else:
            self.level = 0

    def __call__(self, *args):
        print "Entering", self.f.__name__, "level", self.level
        print self.f(*args)
        print "Exited", self.f.__name__


@speaking_decorator
def add_a(text):
    return text + " a"

add_a("hello world")
