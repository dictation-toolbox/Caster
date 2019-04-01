# This is a test to see if contributors or maintainer can commit to others contributors pull requests.

# End-user at the office and IT guy
situation = ("The printer is jammed, cannot print statement") # End-user experience

# End-user thoughts
problem = True 
insurmountable = True

def enduser():
    if problem and insurmountable == True: # What is the user to do?
        call_IT() # Smart
    else:
        print ("End-user call IT anyway because they made it more worser")
        call_IT() # Dumb

def call_IT():
    print ("Press number 1 for printer support. " + situation)
    one = 1
    while True:
        if one == 1:
            print ("Slightly human but robotic voice: I'm sorry I did not recognize your entry") # Infinite loop

enduser() # End-user: Beginning a bad day



