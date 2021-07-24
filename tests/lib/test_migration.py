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

_INIT_PY = "__init__.py"


class TestMigrator(TestCase):

    def setUp(self):
        Path(TEST_USER_DIR).mkdir(exist_ok=True)
        self.migrator = UserDirUpdater(TEST_USER_DIR)

    def tearDown(self):
        shutil.rmtree(TEST_USER_DIR)

    def test_legacy_upgrade(self):
        # setup 1.0.0 user dir structure
        self.migrator.create_user_dir_directories()
        TestMigrator._setup_legacy_user_content_structure()

        # run migration
        self.migrator.update_user_dir_packages_to_v1_7_0()

        # assert paths
        expected_paths = self._get_first_time_expected_paths()
        expected_paths.update(self._get_test_migration_content_expected_paths())
        self.assertSetEqual(expected_paths, self._get_actual_paths())

    def test_first_time_use(self):
        # setup 1.0.0 user dir structure and 1.7.0+ user dir content packages
        self.migrator.create_user_dir_directories()
        self.migrator.update_user_dir_packages_to_v1_7_0()

        # assert paths
        expected_paths = self._get_first_time_expected_paths()
        self.assertSetEqual(expected_paths, self._get_actual_paths())

    def _get_first_time_expected_paths(self):
        expected = []
        content_root = Path(TEST_USER_DIR).joinpath(ContentRoot.USER_DIR)
        expected.extend([content_root, content_root.joinpath(_INIT_PY)])
        for directory in ["rules", "hooks", "transformers"]:
            pkg = content_root.joinpath(directory)
            expected.extend([pkg, pkg.joinpath(_INIT_PY)])
        expected.extend([Path(TEST_USER_DIR).joinpath(directory) for directory in ["data", "sikuli", "settings"]])
        return set([str(d) for d in expected])

    def _get_test_migration_content_expected_paths(self):
        expected = []
        content_root = Path(TEST_USER_DIR).joinpath(ContentRoot.USER_DIR)
        for directory in ["rules", "hooks", "transformers"]:
            for pkg_dir in ["pkg1", "pkg2"]:
                pkg = content_root.joinpath(directory).joinpath(pkg_dir)
                expected.append(pkg)
                expected.extend([pkg.joinpath(pf) for pf in ["__init__.py", pkg_dir + ".py", pkg_dir + "_support.py"]])
        return set([str(p) for p in expected])

    def _get_actual_paths(self):
        return set([str(f) for f in Path(TEST_USER_DIR).glob("**/*")])

    @staticmethod
    def _setup_legacy_user_content_structure():
        for directory in ["rules", "hooks", "transformers"]:
            for pkg in ["pkg1", "pkg2"]:
                pkg_path = Path(TEST_USER_DIR).joinpath(directory).joinpath(pkg)
                pkg_path.mkdir(parents=True)  # not using exist_ok=True b/c tests shouldn't leave junk behind
                for python_file in ["__init__.py", pkg + ".py", pkg + "_support.py"]:
                    pkg_path.joinpath(python_file).touch()
