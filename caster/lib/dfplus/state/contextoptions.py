'''
Created on Jun 7, 2015

@author: dave
'''
class ContextSet:  # ContextSet
    '''
    The context has composed one or more trigger words. These trigger words
    will be the spec of another command. That other command will be consumed
    by the ContextSeeker and will not be executed.
    '''
    def __init__(self, specTriggers, f, parameters=None):
        assert len(specTriggers) > 0, "ContextSet must have at least one spec trigger"
        assert f != None, "Function parameter can't be null"
        self.specTriggers = specTriggers
        self.f = f
        self.parameters = parameters

class ContextLevel:  # ContextLevel
    '''
    A ContextLevel is composed of one or more ContextSets.
    Once one of the ContextSets is chosen, the ContextLevel is marked as satisfied
    and the result, either an ActionBase or a function object is
    determined and parameters set.
    '''
    def __init__(self, *args):
        self.sets = args
        self.satisfied = False
        self.result = None
        self.parameters = None
        self.dragonfly_data = None
    def copy(self):
        return ContextLevel(*self.sets)