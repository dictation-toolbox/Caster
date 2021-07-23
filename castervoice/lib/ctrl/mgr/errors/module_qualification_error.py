class ModuleQualificationError(Exception):

    def __init__(self):
        super(ModuleQualificationError, self).__init__("Module cannot be qualified.")
