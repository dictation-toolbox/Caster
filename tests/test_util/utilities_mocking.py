from castervoice.lib import utilities


_TOML_FILE = None
_original_save_toml_file = utilities.save_toml_file
_original_load_toml_file = utilities.load_toml_file
_original_save_json_file = utilities.save_json_file
_original_load_json_file = utilities.load_json_file


def _save_toml_file(data, path):
    global _TOML_FILE
    _TOML_FILE[path] = data.copy()


def _load_toml_file(path):
    if path in _TOML_FILE:
        return _TOML_FILE[path].copy()
    return {}


def enable_mock_toml_files():
    global _TOML_FILE
    _TOML_FILE = {}
    utilities.save_toml_file = _save_toml_file
    utilities.load_toml_file = _load_toml_file
    utilities.save_json_file = _save_toml_file
    utilities.load_json_file = _load_toml_file


def disable_mock_toml_files():
    utilities.save_toml_file = _original_save_toml_file
    utilities.load_toml_file = _original_load_toml_file
    utilities.save_json_file = _original_save_json_file
    utilities.load_json_file = _original_load_json_file

