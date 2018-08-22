import unittest
import os
import json
import sys

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(
    os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from configFilesManager import configFilesManager


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

        self.configfilemanager = configFilesManager(
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
        self.configfilemanager.is_correct_information()
        self.assertEqual(self.config_output_waiting,
                         self.configfilemanager.parser_config_dict)


if __name__ == '__main__':
    unittest.main()
