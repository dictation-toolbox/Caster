"""

The idea here is to create a thing which is not the nexus, but which has
the ability to re-register and reload rule classes via the GrammarManager.

This should be a TEMPORARY solution. The real solution is to do away with
SelfModifyingRule and create something like "RuleFactoryRule" to take its
place. This replacement thing would have a backing data structure, and have
the ability to both mutate the backing data structure and send new copies of
a rule to the GrammarManager when the backing data structure is mutated,
traversed, etc.

"""


class SelfModReloadingShim(object):

    def __init__(self):
        pass

    def signal_reload(self, rule_class):
        """
        TODO: this
        :return:
        """
        pass


_SINGLETON = None


def get_instance():
    global _SINGLETON
    if _SINGLETON is None:
        _SINGLETON = SelfModReloadingShim()
    return _SINGLETON
