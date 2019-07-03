from castervoice.lib import settings, textformat

from castervoice.lib.dfplus.ccrmerging2.transformers.base_transformer import BaseRuleTransformer
from castervoice.lib.dfplus.merge.mergerule import MergeRule

'''
This is actually not a transformer. It changes the state for a global method.
It's more like a hook that gets called when you're merging, which executes
based on the name of the mergerule being merged. Should probably rework this,
but porting it as-is to preserve existing functionality for now.
'''

def _apply_format(rule_pronunciation):
    if rule_pronunciation in settings.SETTINGS["formats"]:
        if 'text_format' in settings.SETTINGS["formats"][rule_pronunciation]:
            cap, spacing = settings.SETTINGS["formats"][rule_pronunciation]['text_format']
            textformat.format.set_text_format(cap, spacing)
        else:
            textformat.format.clear_text_format()
        if 'secondary_format' in settings.SETTINGS["formats"][rule_pronunciation]:
            cap, spacing = settings.SETTINGS["formats"][rule_pronunciation]['secondary_format']
            textformat.secondary_format.set_text_format(cap, spacing)
        else:
            textformat.secondary_format.clear_text_format()
    else:
        textformat.format.clear_text_format()
        textformat.secondary_format.clear_text_format()

class NonTransformingGlobalFormatHook(BaseRuleTransformer):
    
    '''abuse the _transform method so can use this transformer
    as a "merge hook" for global state '''
    def _transform(self, mergerule):
        _apply_format(mergerule.get_pronunciation())
        return mergerule
    
    '''This used to only run on MergeRules in ccrmerger.merge'''
    def _is_applicable(self, rule):
        return isinstance(rule, MergeRule)