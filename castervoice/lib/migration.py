from pathlib import Path
import shutil

from castervoice.lib import settings
from castervoice.lib.ctrl.mgr.loading.load.content_root import ContentRoot
from castervoice.lib.merge.selfmod.sm_config import SelfModStateSavingConfig



class UserDirUpdater(object):

    def __init__(self, user_dir):
        self.user_dir = user_dir
        self.root_user_content_package_name = ContentRoot.USER_DIR

    def create_user_dir_directories(self):
        for directory in ["data", "sikuli", "settings"]:
            Path(self.user_dir).joinpath(directory).mkdir(parents=True, exist_ok=True)

    def update_user_dir_packages_to_v1_7_0(self):
        """
        Migrates Caster user dir from v1.0.0 structure to v1.7.0+ structure.
        If used for first time, just sets up v1.7.0+ structure.
        """
        self._make_root_user_content_package()
        for directory in ["rules", "transformers", "hooks"]:
            self._move_legacy_package(directory)
            self._make_user_content_package(directory)

    def update_bringme_toml_to_v1_7_0(self):
        user_dir_path = settings.settings(["paths", "USER_DIR"])
        bringme_config_path = settings.settings(["paths", "SM_BRINGME_PATH"])
        bringme_config = SelfModStateSavingConfig(bringme_config_path)
        bringme_config.load()
        directory_dict = bringme_config.get("folder")

        if directory_dict is not None and ContentRoot.USER_DIR not in directory_dict["caster rules"]:
            # make a backup copy
            copy_destination = str(Path(bringme_config_path).with_name("sm_bringme.toml.bak"))
            shutil.copy2(str(Path(bringme_config_path)), copy_destination)

            # update the user content paths in the bringme config
            directory_dict["caster rules"] = \
                str(Path(user_dir_path).joinpath(ContentRoot.USER_DIR).joinpath("rules"))
            directory_dict["caster hooks"] = \
                str(Path(user_dir_path).joinpath(ContentRoot.USER_DIR).joinpath("hooks"))
            directory_dict["caster transformers"] = \
                str(Path(user_dir_path).joinpath(ContentRoot.USER_DIR).joinpath("transformers"))
            bringme_config.put("folder", directory_dict)
            bringme_config.save()

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
