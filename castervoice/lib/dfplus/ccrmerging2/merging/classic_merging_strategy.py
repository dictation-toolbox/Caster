from castervoice.lib.dfplus.ccrmerging2.merging.base_merging_strategy import BaseMergingStrategy

'''
This strategy KOs any incompatible rules.
'''
class ClassicMergingStrategy(BaseMergingStrategy):
    
    def merge(self, ordered_rules, compat_result):
        
        return None