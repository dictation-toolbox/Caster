class ContentResult(object):
    def __init__(self, content_type, content_item):
        '''
        content_item is either a rule, transformer, or hook
        '''
        self.content_type = content_type
        self.content_item = content_item