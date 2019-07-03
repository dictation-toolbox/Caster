'''
Transformers are the successor to legacy Caster's
"filter functions". The main differences between
them are that:
1. transformers operate on single rules instead of rule pairs
2. transformers assume that the rules passed to them are non-null
3. transformers enforce immutability
4. transformers have no concept of "time" or "order"
'''
class BaseRuleTransformer(object):
    
    '''do not override'''
    def get_transformed_rule(self, mergerule):
        if self._is_applicable(mergerule):
            return self._transform(mergerule.copy())
        return mergerule
    
    '''override this'''
    def _transform(self, mergerule):
        return mergerule
    
    '''override this'''
    def _is_applicable(self, mergerule):
        return False 