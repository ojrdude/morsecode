import unittest
from morsecode import MorseCode

class TestMorseCode(unittest.TestCase):
    """
    Unit tests for MorseCode class
    """

    def setUp(self):
        self._morseCode = MorseCode()

    def testWordToMorseCode(self):
        self.assertEqual('---.--.-..-.',
                          self._morseCode.wordToMorseCode('Owain'))
        
        self.assertEqual(''.join([
            '-----','.----','..---','...--','....-','.....','-....',
            '--...','---..','----.']),
                                 self._morseCode.wordToMorseCode('0123456789'))

        self.assertEqual(''.join([
                          '..---',
                          '...--',
                          '-----',
                          '---..',
                          '----.',
                          '-----',
                          '.----',
                          '....-',
                          '.....',
                          '-....',
                          '--...',
                          ]),
                         self._morseCode.wordToMorseCode('23089014567'))

        self.assertEqual(''.join([
            '-..-', '-.--', '--..', '--.-', '..-'
            ]), self._morseCode.wordToMorseCode('XyZQU'))

if __name__ == '__main__':
    unittest.main()
