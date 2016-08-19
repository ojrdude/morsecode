"""
Unit tests for filewriter.py
"""
from _io import BytesIO, TextIOWrapper
import time
import unittest

from morsecode.filewriter.filewriter import FileWriter


class FileWriterTest(unittest.TestCase):
    """
    Unit test for FileWriter Class
    """


    def setUp(self):
        self.inputStream = TextIOWrapper(BytesIO())
        self.outputStream = TextIOWrapper(BytesIO())
        self.fileWriter = FileWriter(self.inputStream, self.outputStream)
        self.fileWriter.start()


    def tearDown(self):
        self.fileWriter.performAction = False
        self.fileWriter.terminate()


    def testSingleWord(self):
        singleWord = 'W O R D  AR'
        expectedOut = 'WORD\n\n'
        self._feedInInput(singleWord)
        self._assertOutput(expectedOut)
        
        
    def testTwoWords(self):
        twoWords = 'T W O  W O R D S  AR'
        expectedOutput = 'TWO WORDS\n\n'
        self._feedInInput(twoWords)
        self._assertOutput(expectedOutput)
        
        
    def testWordEndingInAR(self):
        """
        Test that when a word ends in AR (not the msg end) we still get rest of message
        without line break.
        """
        word = 'R A D A R AR'
        expectedOutput = 'RADAR\n\n'
        self._feedInInput(word)
        self._assertOutput(expectedOutput)


    def testTwoMessages(self):
        messages = 'M E S S A G E  F O R  Y O U  AR  A N O T H E R  AR'
        expectedOutput = 'MESSAGE FOR YOU\n\nANOTHER\n\n'
        self._feedInInput(messages)
        self._assertOutput(expectedOutput)
    
    
    def testNumbers(self):
        message = 'I  A M  2 5 AR'
        expectedOutput = 'I AM 25\n\n'
        self._feedInInput(message)
        self._assertOutput(expectedOutput)
        
        
    def testLeadingWhiteSpace(self):
        oneSpaceStart = ' T R A I L I N G AR'
        expectedOutput = 'TRAILING\n\n'
        self._feedInInput(oneSpaceStart)
        self._assertOutput(expectedOutput)
        twoSpaceStart = '  T R A I L I N G AR'
        self._feedInInput(twoSpaceStart)
        self._assertOutput(expectedOutput)
        
    
    def testTrailingWhiteSpace(self):
        oneSpaceEnd = 'E N D I N G AR '
        expectedOutput = 'ENDING\n\n'
        self._feedInInput(oneSpaceEnd)
        self._assertOutput(expectedOutput)
        twoSpaceEnd = 'E N D I N G AR  '
        self._feedInInput(twoSpaceEnd)
        self._assertOutput(expectedOutput)
        
        
    def _feedInInput(self, inputString):
        """
        Put in the string that the stream should contain, flush and return pointer
        to zero.
        """
        self.inputStream.write(inputString)
        self.inputStream.flush()
        self.inputStream.seek(0)
        self.fileWriter.performAction = True
        
    def _assertOutput(self, expectedOutput):
        for x in range(20):
            try:
                self.outputStream.seek(0)
                self.assertEqual(expectedOutput, self.outputStream.read())
            except AssertionError:
                if x > 8:
                    raise
                time.sleep(0.1)
            else:
                break

if __name__ == "__main__":
    unittest.main()