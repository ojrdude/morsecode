"""
Unit tests for input reader.
"""
from _io import TextIOWrapper, BytesIO
import time
import unittest

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
        
            
        def getState(self):
            """
            Analogous to GPIO.input() allows the on/off to be polled
            """
            return self.state
        
        
    def setUp(self):
        self.morseKey = self._MockMorseKey()
        self.outputStream = TextIOWrapper(BytesIO())       
        self.inputReader = InputReader(self.morseKey.getState, CODE_DICT, self.outputStream)
        self.inputReader.start()
        time.sleep(0.2) # So that the test definitely starts with Off detected

    def tearDown(self):
        self.inputReader.terminate()


    def testOwain(self):
        for letter in 'OWAI':
            component = LETTER_DICT[letter]
            for dotOrDash in component[:-1]:
                self.morseKey.state = True
                if dotOrDash == DOT:
                    time.sleep(STANDARD_INTERVAL_SECONDS * DOT_DURATION)
                else:
                    time.sleep(STANDARD_INTERVAL_SECONDS * DASH_DURATION)
                self.morseKey.state = False
                time.sleep(STANDARD_INTERVAL_SECONDS * MID_LETTER_GAP)
                
            self.morseKey.state = True
            if component[-1] == DOT:
                time.sleep(STANDARD_INTERVAL_SECONDS * DOT_DURATION)
            else:
                time.sleep(STANDARD_INTERVAL_SECONDS * DASH_DURATION)
            self.morseKey.state = False
            time.sleep(STANDARD_INTERVAL_SECONDS * LETTER_GAP)
            
        component = LETTER_DICT['N']
        for dotOrDash in component[:-1]:
            self.morseKey.state = True
            if dotOrDash == DOT:
                time.sleep(STANDARD_INTERVAL_SECONDS * DOT_DURATION)
            else:
                time.sleep(STANDARD_INTERVAL_SECONDS * DASH_DURATION)
            self.morseKey.state = False
            time.sleep(STANDARD_INTERVAL_SECONDS * MID_LETTER_GAP)
            
        self.morseKey.state = True
        if component[-1] == DOT:
            time.sleep(STANDARD_INTERVAL_SECONDS * DOT_DURATION)
        else:
            time.sleep(STANDARD_INTERVAL_SECONDS * DASH_DURATION)
        self.morseKey.state = False
        time.sleep(STANDARD_INTERVAL_SECONDS * WORD_GAP)
        
        ar = LETTER_DICT['A'] + LETTER_DICT['B']
        time.sleep(10)
        expectedResult = "O W A I N AR"
        self.fail('not yet implemented')
        
        
STANDARD_INTERVAL_SECONDS = 0.1
DOT = '.'
DASH = '-'
DOT_DURATION = 1
MID_LETTER_GAP = 1
DASH_DURATION = 3
LETTER_GAP = 3
WORD_GAP = 7

CODE_DICT = {
               '-.': 'A',
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
               }

LETTER_DICT = {
               'A': '-.',    
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