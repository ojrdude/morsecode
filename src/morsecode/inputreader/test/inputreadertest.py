"""
Unit tests for input reader.
"""
from queue import Queue, Empty
import time
import unittest
from unittest.mock import Mock

from morsecode.inputreader.inputreader import InputReader


class InputReaderTest(unittest.TestCase):
    """
    Unit tests for the Input Reader class
    """

    class _MockMorseKey(object):
        """
        A mock of the GPIO morse key. Provides the
        input method that returns True (On) or False
        (Off) depending on internal state.
        """
        
        
        def __init__(self, startingState=False):
            """
            Constructor.
            :param:startingState: Whether the mock starts On (True) or Off (False)
            """
            self.state = startingState
        
            
        def get_state(self):
            """
            Analogous to GPIO.input() allows the on/off to be polled
            """
            return self.state
    
    
    class _MockLogObject(object):
        """
        A Mock Logger.
        """
        
        def __init__(self):
            self.loggedMessages = ''
        
        def log(self, application, message):
            '''
            Mockup of Logger.write()
            '''
            self.loggedMessages += message
            
            
    def setUp(self):
        self.morse_key = self._MockMorseKey()
        self._logger = self._MockLogObject()
        self.message_queue = Queue()       
        self.input_reader = InputReader(self.morse_key.get_state, CODE_DICT, self.message_queue,
                                        logger=self._logger)
        self.input_reader.start()
        time.sleep(0.2) # So that the test definitely starts with Off detected

    def tearDown(self):
        self.input_reader.terminate()


    def test_owain(self):
        self._input_morse_code('OWAIN')
        
        time.sleep(1)
        expected_result = 'O W A I N  AR'
        actual_result = ''
        try:
            for _ in range(1000): # Safer than while True
                queue_item = self.message_queue.get(block=False)
                actual_result += queue_item
        except Empty:
            pass
        self.assertEqual(expected_result, actual_result)
        
    def test_logging_output(self):
        self.assertFalse(self._logger.loggedMessages)
        self._input_morse_code('HI')
        self.assertTrue(self._logger.loggedMessages,'Nothing written to log output')
        
    def _input_morse_code(self, message):
        for letter in message[:-1]:
            component = LETTER_DICT[letter]
            for dot_or_dash in component[:-1]:
                self.morse_key.state = True
                if dot_or_dash == DOT:
                    time.sleep(STANDARD_INTERVAL_SECONDS * DOT_DURATION)
                else:
                    time.sleep(STANDARD_INTERVAL_SECONDS * DASH_DURATION)
                self.morse_key.state = False
                time.sleep(STANDARD_INTERVAL_SECONDS * MID_LETTER_GAP)
                
            self.morse_key.state = True
            if component[-1] == DOT:
                time.sleep(STANDARD_INTERVAL_SECONDS * DOT_DURATION)
            else:
                time.sleep(STANDARD_INTERVAL_SECONDS * DASH_DURATION)
            self.morse_key.state = False
            time.sleep(STANDARD_INTERVAL_SECONDS * LETTER_GAP)
            
        component = LETTER_DICT[message[-1]]
        for dot_or_dash in component[:-1]:
            self.morse_key.state = True
            if dot_or_dash == DOT:
                time.sleep(STANDARD_INTERVAL_SECONDS * DOT_DURATION)
            else:
                time.sleep(STANDARD_INTERVAL_SECONDS * DASH_DURATION)
            self.morse_key.state = False
            time.sleep(STANDARD_INTERVAL_SECONDS * MID_LETTER_GAP)
            
        self.morse_key.state = True
        if component[-1] == DOT:
            time.sleep(STANDARD_INTERVAL_SECONDS * DOT_DURATION)
        else:
            time.sleep(STANDARD_INTERVAL_SECONDS * DASH_DURATION)
        self.morse_key.state = False
        time.sleep(STANDARD_INTERVAL_SECONDS * WORD_GAP)
        
        ar = LETTER_DICT['A'] + LETTER_DICT['R']
        for dot_or_dash in ar[:-1]:
            self.morse_key.state = True
            if dot_or_dash == DOT:
                time.sleep(STANDARD_INTERVAL_SECONDS * DOT_DURATION)
            else:
                time.sleep(STANDARD_INTERVAL_SECONDS * DASH_DURATION)
            self.morse_key.state = False
            time.sleep(STANDARD_INTERVAL_SECONDS * MID_LETTER_GAP)
            
        self.morse_key.state = True
        if ar[-1] == DOT:
            time.sleep(STANDARD_INTERVAL_SECONDS * DOT_DURATION)
        else:
            time.sleep(STANDARD_INTERVAL_SECONDS * DASH_DURATION)
        self.morse_key.state = False
        time.sleep(STANDARD_INTERVAL_SECONDS * WORD_GAP)
STANDARD_INTERVAL_SECONDS = 0.1
DOT = '.'
DASH = '-'
DOT_DURATION = 1
MID_LETTER_GAP = 1
DASH_DURATION = 3
LETTER_GAP = 3
WORD_GAP = 7

CODE_DICT = {
               '.-': 'A',
               '-...': 'B',
               '-.-.': 'C',
               '-..': 'D',
               '.': 'E',
               '..-.': 'F',
               '--.': 'G',
               '....': 'H',
               '..': 'I',
               '.---': 'J',
               '-.-': 'K',
               '.-..': 'L',
               '--': 'M',
               '-.': 'N',
               '---': 'O',
               '.--.': 'P',
               '--.-': 'Q',
               '.-.': 'R',
               '...': 'S',
               '-': 'T',
               '..-': 'U',
               '...-': 'V',
               '.--': 'W',
               '-..-': 'X',
               '-..-': 'Y',
               '--..': 'Z',
               '.-.-.': 'AR'
               }

LETTER_DICT = {
               'A': '.-',    
               'B': '-...',  
               'C': '-.-.',  
               'D': '-..',   
               'E': '.',   
               'F': '..-.',  
               'G': '--.',  
               'H': '....', 
               'I': '..',    
               'J': '.---', 
               'K': '-.-',   
               'L': '.-..',  
               'M': '--',    
               'N': '-.',    
               'O': '---',  
               'P': '.--.',  
               'Q': '--.-',  
               'R': '.-.',   
               'S': '...',   
               'T': '-',   
               'U': '..-',  
               'V': '...-',  
               'W': '.--',  
               'X': '-..-',  
               'Y': '-..-',  
               'Z': '--..',
               }

if __name__ == "__main__":
    unittest.main()