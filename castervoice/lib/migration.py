import six

from castervoice.lib.ctrl.mgr.loading.load.content_root import ContentRoot

if six.PY2:
    from castervoice.lib.util.pathlib import Path
else:
    from pathlib import Path  # pylint: disable=import-error


class UserDirUpdater(object):

    def __init__(self, user_dir):
        self.user_dir = user_dir
        self.root_user_content_package_name = ContentRoot.USER_DIR

    def update_user_dir_packages_to_v1_7_0(self):
        """
        Migrates Caster user dir from v1.0.0 structure to v1.7.0+ structure.
        If used for first time, just sets up v1.7.0+ structure.
        """
        self._make_root_user_content_package()
        for directory in ["rules", "transformers", "hooks"]:
            self._move_legacy_package(directory)
            self._make_user_content_package(directory)

    def _move_legacy_package(self, package_name):
        source_path = Path(self.user_dir).joinpath(package_name)
        dest_path_base = Path(self.user_dir).joinpath(self.root_user_content_package_name).joinpath(package_name)
        dest_path_base.mkdir(parents=True, exist_ok=True)
        if source_path.exists():
            for f in source_path.glob("*"):
                f.rename(dest_path_base.joinpath(f.stem))
            source_path.rmdir()

    def _make_user_content_package(self, package_name):
        """idempotent"""
        root_package_path = Path(self.user_dir).joinpath(self.root_user_content_package_name)
        package_path = root_package_path.joinpath(package_name)
        package_path.mkdir(parents=True, exist_ok=True)

        init_py_file = package_path.joinpath("__init__.py")
        init_py_file.touch(exist_ok=True)

    def _make_root_user_content_package(self):
        """idempotent"""
        root_user_content_package_path = Path(self.user_dir).joinpath(self.root_user_content_package_name)
        root_user_content_package_path.mkdir(parents=True, exist_ok=True)
        root_user_content_package_path.joinpath("__init__.py").touch(exist_ok=True)
