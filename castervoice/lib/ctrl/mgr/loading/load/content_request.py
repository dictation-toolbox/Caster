class ContentRequest(object):
    def __init__(self, content_type, directory, module_name):
        self.content_type = content_type
        self.directory = directory
        self.module_name = module_name
