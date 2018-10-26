#Windows Speech Recognition

This page contains information about running Dragonfly and Caster with Windows Speech Recognition. (Not Cortana.)

##Running a Dragonfly Python file with WSR

In order to create a runnable Dragonfly .py file, you should create a Grammar object, add a Rule to it (as detailed in the Rule Construction page), and then add the following to the bottom of the file:

```
if __name__ == "__main__":
    import pythoncom, time
    # Ignore this if you're using Dragon
    while True:
        pythoncom.PumpWaitingMessages()  # @UndefinedVariable
        time.sleep(.1)
```

##Running Caster with WSR

Caster takes care of the above step for you and will detect whether you're using WSR or Dragon. No extra steps are required.
