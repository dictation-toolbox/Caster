from dragonfly import RecognitionHistory
from dragonfly.timer import _Timer


MULTI_CLIPBOARD={}

DICTATION_CACHE=RecognitionHistory(10)
DICTATION_CACHE.register()

TIMER_MANAGER=_Timer(1)


def print_startup_message():
    print "*- Starting Sorcery v.203 -*"







