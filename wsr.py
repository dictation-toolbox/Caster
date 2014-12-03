import time
import pythoncom
import __init__
import _main


while True:
    pythoncom.PumpWaitingMessages()
    time.sleep(.1)