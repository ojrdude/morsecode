'''
The Morse code application
'''
import sys
from configparser import ConfigParser

class Application(object):
    
    def __init__(self, configFile, stanza):
        '''
        Constructor
        :param:configFile: The location of a config file for the application.
        :param:stanza: The stanza of the config file to use.
        '''
        self._config = ConfigParser().read(configFile)[stanza]
    
    def main(self):
        '''
        Starts the application.
        '''
        pass

if __name__ == '__main__':
    try:
        configFile = sys.argv[1]
        stanza = sys.argv[2]
    except IndexError:
        print('Not enough parameters given. Usage: python application.py configFileLocation stanza')
        print('E.g. python application.py /home/raspberrypi/config raspberrypi') 
        sys.exit(1)
    sys.exit(Application(configFile, stanza).main())