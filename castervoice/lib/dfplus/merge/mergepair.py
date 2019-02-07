class MergeInf(object):
    '''TYPE'''
    GLOBAL = 0
    APP = 1
    SELFMOD = 2
    '''TIME'''
    BOOT = 3
    RUN = 4
    BOOT_NO_MERGE = 5


class MergePair(object):
    def __init__(self, time, type, rule1, rule2, check_compatibility, extras=None):
        self.time = time
        self.type = type
        self.rule1 = rule1
        self.rule2 = rule2
        self.changed = False  # presently unused
        self.check_compatibility = check_compatibility
        self.extras = extras
