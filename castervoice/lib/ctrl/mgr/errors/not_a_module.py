class NotAModuleError(Exception):
    def __init__(self, file_path):
        super(file_path + " is not a module.")