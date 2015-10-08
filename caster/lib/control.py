from caster.lib.ctrl.nexus import Nexus


_NEXUS = None

def nexus():
    global _NEXUS
    if _NEXUS==None:
        _NEXUS = Nexus()
    return _NEXUS
