from dragonfly import (ActionBase, Text, Key, Function, Mimic, MappingRule)

class CasterState:
    def __init__(self):
        ''''''


class ContextDeck:
    def __init__(self):
        self.list=[]
    
    def add(self, action):
        is_seeker=isinstance(action, ContextSeeker)
        is_continuer=isinstance(action, Continuer)
        if is_seeker and not is_continuer:
            if action.back!=None:
                deck_size=len(self.list)
                seekback_size=len(action.back)
                all_satisfied=False
                for i in range(0, seekback_size):
                    index=deck_size-1-i
                    this_level_satisfied=index>=0
                    all_satisfied=this_level_satisfied
                    if this_level_satisfied:
                        action.satisfy_level(i, True, self.list[index])
                    else:
                        # back looking seekers have nothing else to wait for
                        action.satisfy_level(i, True, None)
                    
        
        # the other cases that need to be handled here:
        # an unsatisfied continuer exists
        # an unsatisfied forward-looking context seeker exists
        # neither exist

DECK=ContextDeck()

class RText(Text):
    def __init__(self, spec=None, static=False, pause=0.02,
                 autofmt=False, rspec="default", rdescript=None,
                 rbreakable=False):
        self.rspec = rspec
        self.rdescript = rdescript
        self.breakable = rbreakable
    
    def _execute(self, data=None):
        global DECK
        DECK.add(self)# should take care of execution if it's supposed to be executed

class RKey(Key):
    ''''''

class CS:#ContextSet
    '''
    The context has composed one or more trigger words. These trigger words
    will be the spec of another command. That other command will be consumed
    by the ContextSeeker and will not be executed.
    '''
    def __init__(self, specTriggers, f, parameters=None):
        if len(specTriggers)==0:
            raise Exception("ContextSet must have at least one spec trigger")
        if f==None:
            raise Exception("Function parameter can't be null")
        self.specTriggers=specTriggers
        self.f=f
        self.parameters=parameters

class CL:#ContextLevel
    '''
    A context level is composed of two or more context sets.
    Once one of the sets is chosen, the level is marked as satisfied
    and the result, either an ActionBase or a function object is
    determined and parameters set.
    '''
    def __init__(self, *args):
        if len(args)<2:
            raise Exception("Cannot create ContextLevel with <2 ContextSets")
        self.sets=args
        self.satisfied=False
        self.result=None
        self.parameters=None

class ContextSeeker(ActionBase):
    def __init__(self, back, forward):
        ActionBase.__init__(self)
        self.back=back
        self.forward=forward
        if self.back==None and self.forward==None:
            raise Exception("Cannot create ContextSeeker with no levels")
    
    def satisfy_level(self, level_index, is_back, action):
        dir=self.back if is_back else self.forward
        cl=dir[level_index]
        if not cl.satisfied:
            if action==None:
                cl.satisfied=True
                cl.result=cl.sets[0].f
                cl.parameters=cl.sets[0].parameters
                return
            for cs in cl.sets:
                #action must have a spec
                if action.spec in cs.specTriggers:
                    cl.satisfied=True
                    cl.result=cs.f
                    cl.parameters=cs.parameters
    
    def _execute(self, data=None):
        global DECK
        DECK.add(self)
        
    def execute_later(self):
        for cl in self.back+self.forward:
            action=cl.f
            if not isinstance(action, ActionBase):
                # it's a function object
                if cl.parameters==None:
                    action()
                else:
                    action(cl.parameters)
            else:
                # 
                action(cl.parameters).execute()
                    
        
        
        

class Continuer(ContextSeeker):
    ''''''
