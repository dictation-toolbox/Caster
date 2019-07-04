class CompatibilityResult(object):
    def __init__(self, mergerule, compatible, incompatible_specs=None):
        self._mergerule = mergerule
        self._compatible = compatible
        self._incompatible_specs = incompatible_specs
    
    def rule(self):
        return self._mergerule
    
    def is_compatible(self):
        return self._compatible
    
    def incompatible_specs(self):
        if self._incompatible_specs is None: return []
        return list(self._incompatible_specs)