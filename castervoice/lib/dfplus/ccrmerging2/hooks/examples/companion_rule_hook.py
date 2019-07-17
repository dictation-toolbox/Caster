from castervoice.lib.dfplus.ccrmerging2.hooks.base_hook import BaseHook


class CompanionRuleHook(BaseHook):
    """
    Copying this into the .caster dir enables companion rules.
    """

    def __init__(self):
        super("activation")
        '''TODO: read in the [new] companion config file here
        
        
        '''

    def run(self, event):
        companion_names = self._get_companion_rules(event.rule_class_name, event.active)
        '''
        1. figure out how to map the rule class name to the pronunciation
        2. use Dragonfly actions to just "say" the enable/disable commands so you don't have to give special access
            to the GrammarManager
        '''


    def _get_companion_rules(self, class_name, active):
        "{}".format("")
        companion_rules = set()


        '''
        TODO: avoid circular companion rules by only traversing the map further if
        the next companion is not already in a SET of companions
        '''

        return []


def get_hook():
    return CompanionRuleHook()
