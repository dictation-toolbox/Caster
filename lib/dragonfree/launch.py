import getopt
from subprocess import Popen
import sys
import time

import psutil

try:
    # this section only necessary if called externally to Dragon
    BASE_PATH = "C:/NatLink/NatLink/MacroSystem"
    if BASE_PATH not in sys.path:
        sys.path.append(BASE_PATH)
except Exception:
    pass
from lib import settings

def run(arguments):
#     Popen(arguments, shell=False, stdin=None, stdout=None, stderr=None, close_fds=True)
    Popen(arguments)

def kill_process(executable):
    for proc in psutil.process_iter():
        try:
            if proc.name() == executable:
                proc.kill()
        except:
            pass

def main(argv):
    help_message = 'launch.py -r\nr\treboot dragon'
    try:
        opts, args = getopt.getopt(argv, "hr")
    except getopt.GetoptError:
        print help_message
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print help_message
            sys.exit()
        elif opt == '-r':
            print "\nDragon Reboot Sequence"
            time.sleep(0.3)
            print "kill: natspeak.exe"
            kill_process("natspeak.exe")
            time.sleep(0.3)
            print "kill: dgnuiasvr_x64.exe"
            kill_process("dgnuiasvr_x64.exe")
            time.sleep(0.3)
            print "kill: dnsspserver.exe"
            kill_process("dnsspserver.exe")
            time.sleep(0.3)
            print "kill: dragonbar.exe"
            kill_process("dragonbar.exe")
            time.sleep(0.3)
            print "Relaunch!"
            
            run([settings.SETTINGS["paths"]["ENGINE_PATH"]])
                        

if __name__ == "__main__":
    main(sys.argv[1:])