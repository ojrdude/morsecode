"""
The Morse code application
"""
from argparse import ArgumentParser
import os
from queue import Queue
import sys

import RPi.GPIO as GPIO
from morsecode.filewriter.filewriter import FileWriter
from morsecode.inputreader.inputreader import InputReader
from morsecode.logging.logger import Logger


class Application(object):
    
    LOG_FILE = '/home/pi/morselog.log'
    
    def __init__(self, output_file, debug=False):
        """
        Constructor
        :param:output_file: The file to output messages to.
        """
        self._output_file = output_file
        self._debug_mode = debug
        self._logger = Logger(self.LOG_FILE, debug)
    
    def main(self):
        """
        Starts the application.
        """
        directory = '/'.join((self._output_file).split('/')[:-1])
        os.makedirs(directory, exist_ok=True)
        out_file = open(self._output_file, 'a')
        msg_queue = Queue()
        code_to_letter_dict = self._read_code_to_letter_dict()        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        def morse_key():
            return GPIO.input(7)

        
        input_reader = InputReader(morse_key, code_to_letter_dict, msg_queue,
                                   logger=self._logger)
        output_writer = FileWriter(msg_queue, out_file, logger=self._logger)
        
        try:
            input_reader.start()
            output_writer.start()
            output_writer.perform_action = True
            while True:
                pass
        finally:
            out_file.close()
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
        with open('config/lettertocodedict', 'r') as ctl_file:
            for line in ctl_file:
                parts = line.split("|")
                result[parts[0]] = parts[1]
        return result
    
    
if __name__ == '__main__':
    arg_parser = ArgumentParser(prog='Morse Code', description='Morse Code Reader')
    arg_parser.add_argument('-o', '--outputfile', default='/home/pi/morsecodemsgs/messages.txt',
                            dest='output_file')
    arg_parser.add_argument('-d', '--debug', default=False, dest='debug', type=bool)
    args = arg_parser.parse_args()
    sys.exit(Application(args.output_file, args.debug).main())