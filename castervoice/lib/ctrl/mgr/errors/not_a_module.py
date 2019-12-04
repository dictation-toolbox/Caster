class NotAModuleError(Exception):
    def __init__(self, file_path):
        super(NotAModuleError, self).__init__(file_path + " is not a module.")