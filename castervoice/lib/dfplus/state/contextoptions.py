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

    def __init__(self,
                 specTriggers,
                 f,
                 parameters=None,
                 consume=True,
                 use_spoken=False,
                 use_rspec=False):
        assert len(specTriggers) > 0, "ContextSet must have at least one spec trigger"
        self.specTriggers = specTriggers
        self.f = f
        self.parameters = parameters
        self.consume = consume
        self.use_spoken = use_spoken
        self.use_rspec = use_rspec


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
        self.result = None  # selected ContextSet
        self.dragonfly_data = None
        self.index = -1  # used to determine which eat() results to use

    def copy(self):
        return ContextLevel(*self.sets)

    def number(self, index):  # used for assigning indices
        self.index = index
