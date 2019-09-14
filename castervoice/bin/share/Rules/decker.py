# A global continuous command recognition(CCR) grammar
# Global means it works everywhere not just one application
# CCR means you can say commands say them without pause and they will execute in order of dictation.
# Enable the "Decker" rule by saying 'enable decker' or 'disable decker'

# Uncomment the 'get_rule()' function and place this file in your '.caster\rules' folder to activate filter.

from castervoice.lib.imports import *


class Decker(MergeRule):
    pronunciation = "decker"

    mapping = {
        "hit the deck": R(Text("shipwrecked")), 
        "explosion": R(Text("cannonball"))
    }


# def get_rule():
#    return Decker()
