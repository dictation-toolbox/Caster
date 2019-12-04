_NEXUS = None


def init_nexus(content_loader):
    global _NEXUS
    from castervoice.lib.ctrl.nexus import Nexus
    _NEXUS = Nexus(content_loader)


def nexus():
    return _NEXUS
