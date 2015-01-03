import getopt
import sys
import time

import psutil
from subprocess import Popen


def run(arguments):
    Popen(arguments, shell=False, stdin=None, stdout=None, stderr=None, close_fds=True)

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
            print "Relaunch!"
            run([r"C:\Program Files (x86)\Nuance\NaturallySpeaking12\Program\natspeak.exe"])
                        

if __name__ == "__main__":
    main(sys.argv[1:])