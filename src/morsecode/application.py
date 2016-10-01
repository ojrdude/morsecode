"""
The Morse code application
"""
import os
from queue import Queue
import sys

import RPi.GPIO as GPIO
from morsecode.filewriter.filewriter import FileWriter
from morsecode.inputreader.inputreader import InputReader


class Application(object):
    
    def __init__(self, output_file ):
        """
        Constructor
        :param:output_file: The file to output messages to.
        """
        self._output_file = output_file 

    
    def main(self):
        """
        Starts the application.
        """
        directory = '/'.join((self._output_file).split('/')[:-1])
        os.makedirs(directory, exist_ok=True)
        outFile = open(self._output_file, 'a')
        msg_queue = Queue()
        codeToLetterDict = self._read_code_to_letter_dict()        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        def morse_key():
            return GPIO.input(7)

        
        input_reader = InputReader(morseKey, codeToLetterDict, msg_queue)
        outputWriter = FileWriter(msg_queue, outFile)
        
        try:
            input_reader.start()
            outputWriter.start()
            outputWriter.perform_action = True
            while True:
                pass
        except KeyboardInterrupt:
            outFile.close()
            exit(0)
            
            
    def _read_code_to_letter_dict(self):
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
        output_file = sys.argv[1]
    except IndexError:
        print('Not enough parameters given. Usage: python application.py output_file')
        print('E.g. python application.py /home/raspberrypi/morsecodemessages') 
        sys.exit(1)
    sys.exit(Application(output_file).main())