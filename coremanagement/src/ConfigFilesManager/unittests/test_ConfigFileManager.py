import unittest
import os
import json
import sys

PACKAGE_PARENT = '../..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(
    os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from ConfigFilesManager import *


class TestConfigFileManager(unittest.TestCase):
    def setUp(self):
        self.cwd = os.getcwd()
        self.inputs_folder = os.path.join(self.cwd, "inputs")
        self.name_config = "config.ini"
        self._name_config_squema = "config_squema.json"
        self._name_config_output_waiting = "config_output_waiting.json"

        with open(os.path.join(self.inputs_folder,
                               self._name_config_output_waiting)) as f:
            self.config_output_waiting = json.loads(f.read())

        with open(os.path.join(self.inputs_folder,
                               self._name_config_squema)) as f:
            self.config_squema = json.loads(f.read())

        self.configfilemanager = configFilesManager.configFilesManager(
            os.path.join(self.inputs_folder, self.name_config),
            self.config_squema)

    def test_correct_read(self):
        a = {'CONFIG': {'IP': {'type': 'str', 'required': True},
                        'TIMEOUT_DB_MS': {'type': 'int', 'required': True},
                        'PORT': {'type': 'int', 'required': True},
                        'DB_NAME': {'type': 'str', 'required': True},
                        'INSTALL_PATH': {'type': 'str', 'required': True}}}
        self.assertEqual(a, self.config_squema)
        self.assertEqual(self.configfilemanager.dict_config_allows,
                         self.config_squema)

    def test_correct_type(self):
        self.assertIsInstance(self.config_squema, dict)
        self.assertIsInstance(self.config_output_waiting, dict)

    def test_parser_config(self):
        self.configfilemanager.run_check()
        self.assertEqual(self.config_output_waiting,
                         self.configfilemanager.parser_config_dict)

    def test_NotValidValueConfig(self):
        config_squema2 = 'config_squema2.json'
        config_squema2_value = None
        with open(os.path.join(self.inputs_folder,
                               config_squema2)) as f:
            config_squema2_value = json.loads(f.read())

        self.configfilemanager = configFilesManager.configFilesManager(
            os.path.join(self.inputs_folder, self.name_config),
            config_squema2_value)

        self.assertRaises(NotValidValueConfig,
                          self.configfilemanager.run_check)

    def test_RequiredNotExiste(self):
        config_squema3 = 'config_squema3.json'
        name_config2 = 'config2.ini'
        config_squema3_value = None
        with open(os.path.join(self.inputs_folder,
                               config_squema3)) as f:
            config_squema3_value = json.loads(f.read())

        self.configfilemanager = None
        self.configfilemanager = configFilesManager.configFilesManager(
            os.path.join(self.inputs_folder, name_config2),
            config_squema3_value)
        self.assertRaises(RequiredNotExiste,
                          self.configfilemanager.run_check)


if __name__ == '__main__':
    unittest.main()
