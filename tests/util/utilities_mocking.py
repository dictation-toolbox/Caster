from castervoice.lib import utilities


_TOML_FILE = None


def _save_toml_file(data, path):
    global _TOML_FILE
    _TOML_FILE = data.copy()


def _load_toml_file(path):
    return _TOML_FILE.copy()


def mock_toml_files():
    global _TOML_FILE
    _TOML_FILE = {}
    utilities.save_toml_file = _save_toml_file
    utilities.load_toml_file = _load_toml_file
