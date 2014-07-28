import paths
import winsound, sys
from threading import Timer

CONTINUE = True
minutes=int(sys.argv[1])
remaining_minutes=minutes/60
original_remaining_minutes=remaining_minutes
INTERVAL=minutes

def set_alarm():
    global INTERVAL, CONTINUE, remaining_minutes
    winsound.PlaySound(paths.get_media_path() + '\\49685__ejfortin__nano-blade-loop.wav', winsound.SND_FILENAME)
    if CONTINUE:
        remaining_minutes=original_remaining_minutes
        Timer(INTERVAL, set_alarm).start()
        

def printer():
    global remaining_minutes
    print "minutes remaining: "+str(remaining_minutes)
    remaining_minutes-=1
    Timer( 60, printer).start()


print "Simple Alarm 0.1 by synkarius"
print "---"
printer()
set_alarm()