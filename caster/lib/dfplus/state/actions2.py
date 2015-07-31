from caster.asynch.hmc import h_launch
from caster.lib import settings, control
from caster.lib.dfplus.state.actions import AsynchronousAction, ContextSeeker
from caster.lib.dfplus.state.short import L, S


class ConfirmAction(AsynchronousAction):
    '''
    Similar to AsynchronousAction, but the repeated action is always
    checking on the Homunculus response.
    -
    Homunculus response guide:
    0: no response yet
    1: True
    2: False
    '''
    def __init__(self, base, rspec="default", rdescript="unnamed command (RA)"):
        mutable_integer = {"value": 0}
        def check_response(): # signals to the stack to cease waiting, return True terminates
            return mutable_integer["value"]!=0
        self.mutable_integer = mutable_integer
        AsynchronousAction.__init__(self, 
                                    [L(S(["cancel"], check_response, None))], 
                                    1, 60, rdescript, False)# cannot block, if it does, it'll block its own confirm command
        self.base = base
        self.rspec = rspec
    def _execute(self, data=None):
        confirm_stack_item = self.state.generate_confirm_stack_item(self, data)
        self.mutable_integer["value"] = 0
        mutable_integer = self.mutable_integer
        def hmc_closure(data):
            '''
            receives response from homunculus, uses it to
            stop the stack and tell the ConfirmAction how
            to execute
            '''
            mutable_integer["value"] = data["confirm"]
            confirm_stack_item.receive_hmc_response(data["confirm"])
                    
        h_launch.launch(settings.QTYPE_CONFIRM, hmc_closure, "_".join(self.rdescript.split(" ")))
        self.state.add(confirm_stack_item)

class FuzzyMatchAction(ContextSeeker):
    '''
    list_function: provides a list of strings to filter
        ; takes no parameters, returns a list
    filter_function: reduces the size of the list from list_function
        ; can be null, takes dragonfly data and list from  list_function
    selection_function: what to do with the result that the user chooses
        ; takes a string, does something with it, returns nothing
    default_1: speaking a next command other than a number or cancel activates the first choice in the list
        ; 
    '''
    TEN = ["numb one", "numb two", "numb three", "numb four", "numb five", 
       "numb six", "numb seven", "numb eight", "numb nine", "numb ten"]
    def __init__(self, list_function, filter_function, selection_function, default_1=True, rspec="default", rdescript="unnamed command (FM)"):
        def get_choices(data):
            choices = list_function()
            if filter_function:
                choices = filter_function(data, choices) # the filter function is responsible for using the data to filter the choices
            while len(choices)<len(FuzzyMatchAction.TEN):
                choices.append("") # this is questionable
            return choices
        self.choice_generator = get_choices
        
        mutable_list = {"value": None} # only generate the choices once, and show them between the action and the stack item
        self.mutable_list = mutable_list
        
        def execute_choice(spoken_words=[]):
            n = -1
            while len(spoken_words)>2:# in the event the last words spoken were a command chain,
                spoken_words.pop()    # get only the number trigger
            j = ""
            if len(spoken_words)>0:
                j = " ".join(spoken_words)
            if j in FuzzyMatchAction.TEN:
                n = FuzzyMatchAction.TEN.index(j)
            if n == -1: n = 0
            selection_function(mutable_list["value"][n])
        def cancel_message(_):
            control.nexus().intermediary.text("Cancel ("+rdescript+")")
        forward = [L(S([""], execute_choice, consume=False),
                     S(["number"], execute_choice, use_spoken=True), 
                     S(["cancel", "clear"], cancel_message)
                    )
                  ]
        if not default_1: # make cancel the default
            context_level = forward[0]
            a = context_level.sets[0]
            context_level.sets[0] = context_level.sets[2]
            context_level.sets[2] = a
        ContextSeeker.__init__(self, None, forward, rspec, rdescript)
    
    def _execute(self, data=None):
        choices = self.choice_generator(data)
        display_string = ""
        for i in range(0, 10):
            display_string += str(i+1)+" - "+choices[i]
            if i+1<10: display_string += "\n"
        control.nexus().intermediary.hint(display_string)
        self.mutable_list["value"] = choices
        self.state.add(self.state.generate_context_seeker_stack_item(self, data))
        