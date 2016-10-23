"""
Unit tests for configreader
"""
import unittest

from morsecode.configreader.configreader import ConfigReader


class ConfigReaderTest(unittest.TestCase):
    """
    Tests for the ConfigReader class.
    """

    def test_read_config_default(self):
        config_reader = ConfigReader('testconfig.cfg')
        expected_dict = {'dashlength': 1.5,
                         'messageend': 13,
                         'spacelength': 6.5,
                         'letterspace': 2.7}
        actual_dict = config_reader.read()
        self.assertDictEqual(expected_dict, actual_dict)

    def test_read_config_non_default(self):
        config_reader = ConfigReader('testconfig.cfg')
        expected_dict = {'dashlength': 1.9,
                         'messageend': 2.0,
                         'spacelength': 6.6,
                         'letterspace': 2}
        actual_dict = config_reader.read('section2')
        self.assertDictEqual(expected_dict, actual_dict)
    
    def test_read_config_value_missing_no_default(self):
        config_reader = ConfigReader('testconfig_value_missing.cfg')
        with self.assertRaises(ValueError):
            config_reader.read('section')

    def test_read_config_missing_default_provided(self):
        config_reader = ConfigReader('testconfig.cfg')
        expected_dict = {'dashlength': 1.9,
                         'messageend': 2.0,
                         'spacelength': 6.5,
                         'letterspace': 2}
        actual_dict = config_reader.read('missing_value')
        self.assertDictEqual(expected_dict, actual_dict)
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()