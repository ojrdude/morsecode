"""
Config file reader
"""
from configparser import ConfigParser

class ConfigReader(object):
    """
    Class that reads a config file containing timing values and
    returns a dict with these values.
    """

    _REQUIRED_FIELDS = ['DashLength', 'MessageEnd', 'SpaceLength', 'LetterSpace']
    
    def __init__(self, config_file):
        """
        Constructor
        :param:config_file The location of the config file to read.
        """
        self._config_file = config_file
        
    def read(self, section=None):
        """
        Read the config file and return a dict with of 
        timings.
        :param:section The name of the section to read. If not 
        provided, DEFAULT is read.
        """
        if section is None:
            section = 'DEFAULT'
        config = ConfigParser()
        config.read(self._config_file)
        config_section = config[section]
        
        missing_values = [x for x in self._REQUIRED_FIELDS if x not in config_section]
        
        if missing_values:
            raise ValueError('Values missing from config: {}'.format(missing_values))
        
        config_dict = {k : float(config_section[k]) for k in config_section}
        return config_dict