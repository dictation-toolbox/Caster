_NEXUS = None


def nexus():
    global _NEXUS
    if _NEXUS is None:
        from castervoice.lib.ctrl.nexus import Nexus
        _NEXUS = Nexus()
    return _NEXUS
