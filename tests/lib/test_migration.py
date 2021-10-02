import shutil

from pathlib import Path

from castervoice.lib.ctrl.mgr.loading.load.content_root import ContentRoot
from castervoice.lib.migration import UserDirUpdater
from tests.test_consts import TEST_USER_DIR
from castervoice.lib.merge.selfmod.sm_config import SelfModStateSavingConfig
from tests.test_util.settings_mocking import SettingsEnabledTestCase


_INIT_PY = "__init__.py"


class TestMigrator(SettingsEnabledTestCase):

    def setUp(self):
        self._enable_file_writing()
        Path(TEST_USER_DIR).mkdir(exist_ok=True)
        self.migrator = UserDirUpdater(TEST_USER_DIR)

    def tearDown(self):
        shutil.rmtree(TEST_USER_DIR)

    def test_bringme_toml_upgrade_correctness(self):
        """
        Tests that bringme toml config file is correct after 1.7.0 update.
        """
        # set up 1.0.0 bringme toml file
        bringme_toml_path = str(Path(TEST_USER_DIR).joinpath("settings/sm_bringme.toml"))
        self._setup_legacy_bringme_toml(bringme_toml_path)

        # run migration
        self.migrator.update_bringme_toml_to_v1_7_0()

        # assertions
        self._do_bringme_toml_assertions(bringme_toml_path)

    def test_bringme_toml_upgrade_check_works_with_first_time_run(self):
        """
        Tests that bringme toml upgrade doesn't crash out because of a blank bringme config
        file on first run.
        """
        # do 1.7.0+ first time setup
        self.migrator.create_user_dir_directories()
        self._set_setting(["paths", "USER_DIR"], TEST_USER_DIR)
        self._set_setting(["paths", "SM_BRINGME_PATH"], str(Path(TEST_USER_DIR).joinpath("settings/sm_bringme.toml")))

        # run migration
        self.migrator.update_bringme_toml_to_v1_7_0()

        # assertions
        self.assertFalse(Path(TEST_USER_DIR).joinpath("settings/sm_bringme.toml.bak").exists())

    def test_bringme_toml_upgrade_idempotency(self):
        """
        Tests that bringme toml config backup file is not overwritten after update runs 2nd time.
        """
        # set up 1.0.0 bringme toml file
        bringme_toml_path = str(Path(TEST_USER_DIR).joinpath("settings/sm_bringme.toml"))
        self._setup_legacy_bringme_toml(bringme_toml_path)

        # run migration 2x
        self.migrator.update_bringme_toml_to_v1_7_0()
        self.migrator.update_bringme_toml_to_v1_7_0()

        # assertions
        self._do_bringme_toml_assertions(bringme_toml_path)

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

    def _setup_legacy_bringme_toml(self, bringme_toml_path):
        self.migrator.create_user_dir_directories()
        self._set_setting(["paths", "USER_DIR"], TEST_USER_DIR)
        self._set_setting(["paths", "SM_BRINGME_PATH"], bringme_toml_path)
        TestMigrator._setup_legacy_bringme_toml_file(bringme_toml_path)

    def _do_bringme_toml_assertions(self, bringme_toml_path):
        # test that backup exists and is correct
        backup_path = Path(TEST_USER_DIR).joinpath("settings").joinpath("sm_bringme.toml.bak")
        backup_config = SelfModStateSavingConfig(str(backup_path))
        backup_config.load()
        expected_backup = {
            "caster rules": str(Path(TEST_USER_DIR).joinpath("rules")),
            "caster hooks": str(Path(TEST_USER_DIR).joinpath("hooks")),
            "caster transformers": str(Path(TEST_USER_DIR).joinpath("transformers")),
            "some other path": str(Path("asdf").joinpath("zxcv"))
        }
        self.assertDictEqual(expected_backup, backup_config.get("folder"))
        # test that new values are correct (including that other paths aren't wiped)
        updated_config = SelfModStateSavingConfig(bringme_toml_path)
        updated_config.load()
        expected_paths = {
            "caster rules": str(Path(TEST_USER_DIR).joinpath(ContentRoot.USER_DIR).joinpath("rules")),
            "caster hooks": str(Path(TEST_USER_DIR).joinpath(ContentRoot.USER_DIR).joinpath("hooks")),
            "caster transformers": str(Path(TEST_USER_DIR).joinpath(ContentRoot.USER_DIR).joinpath("transformers")),
            "some other path": str(Path("asdf").joinpath("zxcv"))
        }
        self.assertDictEqual(expected_paths, updated_config.get("folder"))

    @staticmethod
    def _setup_legacy_user_content_structure():
        for directory in ["rules", "hooks", "transformers"]:
            for pkg in ["pkg1", "pkg2"]:
                pkg_path = Path(TEST_USER_DIR).joinpath(directory).joinpath(pkg)
                pkg_path.mkdir(parents=True)  # not using exist_ok=True b/c tests shouldn't leave junk behind
                for python_file in ["__init__.py", pkg + ".py", pkg + "_support.py"]:
                    pkg_path.joinpath(python_file).touch()

    @staticmethod
    def _setup_legacy_bringme_toml_file(legacy_bringme_toml_path):
        bringme_config = SelfModStateSavingConfig(legacy_bringme_toml_path)
        bringme_config.load()
        bringme_config.put("folder", {
            "caster rules": str(Path(TEST_USER_DIR).joinpath("rules")),
            "caster hooks": str(Path(TEST_USER_DIR).joinpath("hooks")),
            "caster transformers": str(Path(TEST_USER_DIR).joinpath("transformers")),
            "some other path": str(Path("asdf").joinpath("zxcv"))
        })
        bringme_config.save()
