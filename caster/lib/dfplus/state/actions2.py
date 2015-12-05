from dragonfly import Function, Key
from dragonfly.actions.action_startapp import BringApp
from dragonfly.windows.window import Window

from caster.asynch.hmc import h_launch
from caster.lib import settings, utilities, navigation
from caster.lib.dfplus.state.actions import AsynchronousAction, ContextSeeker, \
    RegisteredAction
from caster.lib.dfplus.state.short import L, S
from caster.lib.dfplus.state.stackitems import StackItemConfirm, StackItemSeeker,\
    StackItemAsynchronous


#win32gui.SystemParametersInfo(win32con.SPI_SETFOREGROUNDLOCKTIMEOUT, 0, 1)
class BoxAction(AsynchronousAction):
    '''
    Similar to AsynchronousAction, but the repeated action is always
    checking on the Homunculus response.
    '''
    def __init__(self, receiver, rspec="default", rdescript="unnamed command (BA)", repetitions=60,
                 box_type=settings.QTYPE_DEFAULT, box_settings={}, log_failure=False):
        _ = {"tries": 0}
        self._ = _ # signals to the stack to cease waiting, return True terminates
        def check_for_response():
            try:
                _data = self.nexus().comm.get_com("hmc").get_message()
            except Exception:
                if log_failure: utilities.simple_log()
                _["tries"]+=1
                if _["tries"]>9: return True # try 10 times max if there's no Homonculus response
                else: return False
            if _data is None: return False
            try:
                _data.append(_["dragonfly_data"]) # pass dragonfly data into receiver function
                _["dragonfly_data"] = None
                receiver(_data)
            except Exception:
                if log_failure: utilities.simple_log()
            return True
            
        AsynchronousAction.__init__(self, # cannot block, if it does, it'll block its own confirm command
                                    [L(S(["cancel"], check_for_response, None))], 
                                    1, repetitions, rdescript, False)
        self.rspec = rspec
        self.box_type = box_type
        self.box_settings = box_settings # custom instructions for setting up the tk window ("Homunculus")
        self.log_failure = log_failure
    def _execute(self, data=None):
        self._["tries"] = 0       # reset
        self._["dragonfly_data"] = data
        h_launch.launch(self.box_type, data = self.encode_box_settings())
        self.nexus().state.add(StackItemAsynchronous(self, data))
    
    def encode_box_settings(self):
        result=""
        instructions_first = False
        if self.box_type==settings.QTYPE_INSTRUCTIONS and "instructions" in self.box_settings:
            result+=settings.HMC_SEPARATOR.join(self.box_settings["instructions"].split(" "))+"|"
            instructions_first = True
        for key in self.box_settings.keys():
            if instructions_first and key=="instructions":
                continue
            result += settings.HMC_SEPARATOR.join(self.box_settings[key].split(" ")) + "|"
        return result
            
        

class ConfirmAction(AsynchronousAction):
    '''
    Similar to AsynchronousAction, but the repeated action is always
    checking on the Homunculus response.
    -
    Homunculus response guide:
    0: no response yet
    1: True
    2: False
    -
    This is the only action which requires the nexus in the constructor;
    the rest of them can use the setter. This is because on_complete
    needs a nexus immediately.
    '''
    def __init__(self, base, rspec="default", rdescript="unnamed command (CA)", instructions="instructions missing", nexus=None):
        self.set_nexus(nexus)
        on_complete = AsynchronousAction.hmc_complete(lambda data: receive_response(data), self.nexus())
        AsynchronousAction.__init__(self, 
                                    [L(S(["cancel"], on_complete, None))], 
                                    1, 60, rdescript, False)# cannot block, if it does, it'll block its own confirm command
        
        self.base = base
        self.rspec = rspec
        self.instructions = instructions
        
        
        mutable_integer = {"value": 0}
        def receive_response(data): # signals to the stack to cease waiting, return True terminates
            '''
            receives response from homunculus, uses it to
            stop the stack and tell the ConfirmAction how
            to execute
            '''
            mutable_integer["value"] = data["confirm"]
        self.mutable_integer = mutable_integer
        
        
        
    def _execute(self, data=None):
        '''the factory (ConfirmAction) sharing data with the objects 
        it generates (StackItemConfirm) would be a problem if there 
        could ever be more than one of these at a time, but there can't'''
        self.mutable_integer["value"] = 0
        
        confirm_stack_item = StackItemConfirm(self, data)
        confirm_stack_item.shared_state(self.mutable_integer)
                            
        h_launch.launch(settings.QTYPE_CONFIRM, data=settings.HMC_SEPARATOR.join(self.instructions.split(" ")))
        self.nexus().state.add(confirm_stack_item)

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
    TEN = ["numb "+x for x in navigation.numbers_list_1_to_9()+["ten"]]
    def __init__(self, list_function, filter_function, selection_function, default_1=True, rspec="default", 
                 rdescript="unnamed command (FM)", log_file_path=None):
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
        self.filter_text = ""
        
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
            choices = mutable_list["value"]
            selection_function(choices[n])
            if log_file_path and settings.SETTINGS["miscellaneous"]["enable_match_logging"]:
                log_entry = [self.filter_text] + [choices[n]] + [s for s,i in zip(choices, range(len(choices))) if i != n]
                with open(log_file_path, "a") as log_file:
                    log_file.write(str(log_entry) + "\n")
        def cancel_message():
            self.nexus().intermediary.text("Cancel ("+rdescript+")")
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
        self.nexus().intermediary.hint(display_string)
        if data is not None and "text" in data:
            self.filter_text = data["text"].format()
        self.mutable_list["value"] = choices
        self.nexus().state.add(StackItemSeeker(self, data))

class NullAction(RegisteredAction):
    def __init__(self, rspec="default", rdescript="unnamed command (RA)", show=False):
        RegisteredAction.__init__(self, Function(lambda: None), rspec=rspec, rdescript=rdescript, rundo=None, show=show)

class SuperFocusWindow(AsynchronousAction):
    '''
    Workaround class for Dragonfly's FocusWindow, which only works on titles and 
    32-bit executables, and sometimes fails to work at all. 
    '''
    @staticmethod
    def focus_was_success(title, executable):
        w=Window.get_foreground()
        success=True
        if title!=None:
            success=title in w.title
        if success and executable!=None:
            success=executable in w.executable
        return success
    
    @staticmethod
    def path_from_executable(executable):
        for win in Window.get_all_windows():
            if executable in win.executable:
                return win.executable
    
    def __init__(self, executable=None, title=None, time_in_seconds=1, repetitions=15, 
        rdescript="unnamed command (SFW)", blocking=False):
        assert executable!=None or title!=None, "SuperFocusWindow needs executable or title"
        def attempt_focus():
            for win in Window.get_all_windows():
                w=win
                found_match=True
                if title!=None:
                    found_match=title in w.title
                if found_match and executable!=None:
                    found_match=executable in w.executable
                if found_match:
                    try:
                        BringApp(w.executable).execute()
                    except Exception:
                        print("Unable to set focus:\ntitle: "+w.title+"\nexe: "+w.executable)
                    break
             
            # do not assume that it worked
            success = SuperFocusWindow.focus_was_success(title, executable)
            if not success:
                if title!=None:
                    print("title failure: ", title, w.title)
                if executable!=None:
                    print("executable failure: ", executable, w.executable, executable in w.executable)
            return success
            
        forward=[L(S(["cancel"], attempt_focus))]
        AsynchronousAction.__init__(self, forward, time_in_seconds=time_in_seconds, repetitions=repetitions, 
                                    rdescript=rdescript, blocking=blocking, 
                                    finisher=Function(lambda message: self.nexus().intermediary.text(message), message="SuperFocus Complete")+Key("escape"))
        self.show = False
        
