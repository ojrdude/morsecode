"""
The Morse code application
"""
from _io import TextIOWrapper, BytesIO
from configparser import ConfigParser
import os
from queue import Queue
import sys

import RPi.GPIO as GPIO
from morsecode.filewriter.filewriter import FileWriter
from morsecode.inputreader.inputreader import InputReader


class Application(object):
    
    def __init__(self, configFile, stanza):
        """
        Constructor
        :param:configFile: The location of a config file for the application.
        :param:stanza: The stanza of the config file to use.
        """
        config = ConfigParser()
        config.read(configFile)
        self._config = {}
        for item in config.items(stanza):
            self._config[item[0]] = item[1]
    
    def main(self):
        """
        Starts the application.
        """
        outputFilePath = self._config['output file']
        directory = '/'.join((outputFilePath).split('/')[:-1])
        os.makedirs(directory, exist_ok=True)
        outFile = open(outputFilePath, 'a')
        msgQueue = Queue()
        codeToLetterDict = self._readCodeToLetterDict()        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        def morseKey():
            return GPIO.input(7)

        
        inputReader = InputReader(morseKey, codeToLetterDict, msgQueue)
        outputWriter = FileWriter(msgQueue, outFile)
        
        try:
            inputReader.start()
            outputWriter.start()
            outputWriter.performAction = True
            while True:
                pass
        except KeyboardInterrupt:
            outFile.close()
            exit(0)
            
            
    def _readCodeToLetterDict(self):
        """
        Read the code to letter map from file and return as dictionary
        """
        result = {}
        with open('config/codetoletterdict', 'r') as ctlFile:
            for line in ctlFile:
                parts = line.split("|")
                result[parts[0]] = parts[1]
        return result
                
    
    def _readLetterToCodeDict(self):
        """
        Read the letter to code map from file and return as dictionary.
        """
        result = {}
        with open('config/lettertocodedict', 'r') as ctlFile:
            for line in ctlFile:
                parts = line.split("|")
                result[parts[0]] = parts[1]
        return result
    
    
if __name__ == '__main__':
    try:
        configFile = sys.argv[1]
        stanza = sys.argv[2]
    except IndexError:
        print('Not enough parameters given. Usage: python application.py configFileLocation stanza')
        print('E.g. python application.py /home/raspberrypi/config raspberrypi') 
        sys.exit(1)
    sys.exit(Application(configFile, stanza).main())