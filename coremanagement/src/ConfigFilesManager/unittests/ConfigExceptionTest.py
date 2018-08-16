import unittest
import os
import json


class TestConfigFileManager(unittest.TestCase):
    def setUp(self):
        self.cwd = os.getcwd()
        self.inputs_folder = os.path.join(self.cwd, "inputs")
        self._name_config_squema = "config_squema.json"

        with open(os.path.join(self.inputs_folder,
                               self._name_config_squema)) as f:
            self.config_squema = json.loads(f.read())

    def test__correct_read(self):
        a = {'CONFIG': {'IP': {'type': 'str', 'required': True},
                        'TIMEOUT_DB_MS': {'type': 'int', 'required': True},
                        'PORT': {'type': 'int', 'required': True},
                        'BD_NAME': {'type': 'str', 'required': True},
                        'INSTALL_PATH': {'required': True}}}
        self.assertEqual(a, self.config_squema)

