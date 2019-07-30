import os


class AutoMagicalModulePathResolver(object):
    def __init__(self, settings_paths):
        self._base_path = settings_paths["BASE_PATH"]
        self._user_dir = settings_paths["USER_DIR"]
        self._paths_to_inspect = [

        ]

    def resolve(self, module_name):
        for dirpath, dirnames, filenames in os.walk(content_path):


