class ContentRootValue(object):
    def __init__(self, detection_root, package_root):
        self.detection_root = detection_root
        self.package_root = package_root


class ContentRoot(object):
    STARTER = ContentRootValue("castervoice", "castervoice")
    USER_DIR = ContentRootValue("caster_user_content", "caster")
