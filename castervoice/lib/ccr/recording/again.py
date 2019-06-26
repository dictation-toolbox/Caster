'''
Created on Sep 6, 2015

@author: synkarius
'''
from castervoice.lib.imports import *

class Again(MergeRule):
    def __init__(self, nexus):
        self.nexus = nexus
        MergeRule.__init__(
            self,
            name="repeat that",
            extras=[IntegerRefST("n", 1, 50)],
            defaults={"n": 1},
            mapping={
                "again (<n> [(times|time)] | do)":
                    R(Function(lambda n: self._create_asynchronous(n)), show=False)
            })

    def _repeat(self, utterance):
        Playback([(utterance, 0.0)]).execute()
        return False

    def _create_asynchronous(self, n):
        if len(self.nexus.history) == 0:
            return

        last_utterance_index = 1
        if settings.WSR:  # ContextStack adds the word to history before executing it
            if len(self.nexus.history) == 1: return
            last_utterance_index = 2

        utterance = [
            str(x) for x in " ".join(self.nexus.history[len(self.nexus.history)
                                                        - last_utterance_index]).split()
        ]
        if utterance[0] == "again": return
        forward = [L(S(["cancel"], lambda: self._repeat(utterance)))]
        AsynchronousAction(
            forward,
            rdescript="Repeat Last Action",
            time_in_seconds=0.2,
            repetitions=int(n),
            blocking=False).execute()

_NEXUS = control.nexus()

if settings.SETTINGS["feature_rules"]["again"]:
    control.non_ccr_app_rule(Again(_NEXUS), context=None, rdp=False)
