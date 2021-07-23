import shutil
from unittest import TestCase

import six

from castervoice.lib.ctrl.mgr.loading.load.content_root import ContentRoot
from castervoice.lib.migration import UserDirUpdater
from tests.test_consts import TEST_USER_DIR

if six.PY2:
    from castervoice.lib.util.pathlib import Path
else:
    from pathlib import Path  # pylint: disable=import-error


class TestMigrator(TestCase):

    def setUp(self):
        Path(TEST_USER_DIR).mkdir(exist_ok=True)
        self.migrator = UserDirUpdater(TEST_USER_DIR)

    def tearDown(self):
        shutil.rmtree(TEST_USER_DIR)

    def test_legacy_upgrade(self):
        TestMigrator._setup_legacy_user_content_structure()

        self.migrator.update_user_dir_packages_to_v1_7_0()

        self._assert_only_expected_paths_exist()

    def test_first_time_use(self):
        self.migrator.update_user_dir_packages_to_v1_7_0()

        self._assert_only_expected_paths_exist()

    def _assert_only_expected_paths_exist(self):
        expected_paths = {str(Path(TEST_USER_DIR)
                              .joinpath(ContentRoot.USER_DIR).joinpath("__init__.py"))}
        for directory in ["rules", "hooks", "transformers"]:
            expected_paths.add(str(Path(TEST_USER_DIR)
                                   .joinpath(ContentRoot.USER_DIR)
                                   .joinpath(directory)
                                   .joinpath("__init__.py")))
            for pkg in ["pkg1", "pkg2"]:
                for python_file in ["__init__.py", pkg + ".py", pkg + "_support.py"]:
                    expected_paths.add(str(Path(TEST_USER_DIR)
                                           .joinpath(ContentRoot.USER_DIR)
                                           .joinpath(directory)
                                           .joinpath(pkg)
                                           .joinpath(python_file)))
        for f in Path(TEST_USER_DIR).glob("**/*.py"):
            self.assertIn(str(f), expected_paths)

    @staticmethod
    def _setup_legacy_user_content_structure():
        for directory in ["rules", "hooks", "transformers"]:
            for pkg in ["pkg1", "pkg2"]:
                pkg_path = Path(TEST_USER_DIR).joinpath(directory).joinpath(pkg)
                pkg_path.mkdir(parents=True)  # not using exist_ok=True b/c tests shouldn't leave junk behind
                for python_file in ["__init__.py", pkg + ".py", pkg + "_support.py"]:
                    pkg_path.joinpath(python_file).touch()
