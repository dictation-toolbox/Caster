'''
Common filter functions library
'''


def make_filter(change_fn, targeting_fn=None, time=None, type=None):
    def _(mp):
        if time and mp.time != time:
            return
        if type and mp.type != type:
            return
        if targeting_fn and not targeting_fn(mp):
            return
        change_fn(mp)

    return _


def there_is_spec_overlap(mp):
    '''determines if there is incompatibility between two rules'''
    if mp.rule1 is None:
        return False
    for spec in mp.rule1.mapping_actual().keys():
        if spec in mp.rule2.mapping_actual().keys():
            return True
    return False


def incoming_gets_priority(mp):
    '''blindly deletes conflicting specs out of the base rule, 
    enables blind merge by disabling compatibility check'''
    for spec in mp.rule1.mapping_actual().keys():
        if spec in mp.rule2.mapping_actual().keys():
            del mp.rule1.mapping_actual()[spec]
    mp.check_compatibility = False
