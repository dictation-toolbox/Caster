class ContentResult(object):
    def __init__(self, content_type, content_item):
        """
        :param content_type: a string indicating the type
        :param content_item: a rule, transformer, or hook
        """
        self.content_type = content_type
        self.content_item = content_item
