"""
Unit tests for filewriter.py
"""
from _io import BytesIO, TextIOWrapper
from queue import Queue, Empty
import time
import unittest
from unittest.mock import Mock

from morsecode.filewriter.filewriter import FileWriter


class FileWriterTest(unittest.TestCase):
    """
    Unit test for FileWriter Class
    """
    
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
        self.msg_queue = Queue()
        self.output_stream = TextIOWrapper(BytesIO())
        self.logger = self._MockLogObject()
        self.file_writer = FileWriter(self.msg_queue, self.output_stream,
                                      logger=self.logger)
        self.file_writer.start()


    def tearDown(self):
        self.file_writer.perform_action = False
        self.file_writer.terminate()


    def test_single_word(self):
        single_word = 'W O R D  AR'
        expected_out = 'WORD\n\n'
        self._feed_in_input(single_word)
        self._assert_output(expected_out)
        
        
    def test_two_words(self):
        two_words = 'T W O  W O R D S  AR'
        expected_output = 'TWO WORDS\n\n'
        self._feed_in_input(two_words)
        self._assert_output(expected_output)
        
        
    def test_word_ending_in_ar(self):
        """
        Test that when a word ends in AR (not the msg end) we still get rest of message
        without line break.
        """
        word = 'R A D A R AR'
        expected_output = 'RADAR\n\n'
        self._feed_in_input(word)
        self._assert_output(expected_output)


    def test_two_messages(self):
        messages = 'M E S S A G E  F O R  Y O U  AR  A N O T H E R  AR'
        expected_output = 'MESSAGE FOR YOU\n\nANOTHER\n\n'
        self._feed_in_input(messages)
        self._assert_output(expected_output)
    
    
    def test_numbers(self):
        message = 'I  A M  2 5 AR'
        expected_output = 'I AM 25\n\n'
        self._feed_in_input(message)
        self._assert_output(expected_output)
        
        
    def test_leading_white_space(self):
        one_space_start = ' T R A I L I N G AR'
        expected_output = 'TRAILING\n\n'
        self._feed_in_input(one_space_start)
        self._assert_output(expected_output)
        two_space_start = '  T R A I L I N G AR'
        self._feed_in_input(two_space_start)
        self._assert_output(expected_output)
        
    
    def test_trailing_white_space(self):
        one_space_end = 'E N D I N G AR '
        expected_output = 'ENDING\n\n'
        self._feed_in_input(one_space_end)
        self._assert_output(expected_output)
        two_space_end = 'E N D I N G AR  '
        self._feed_in_input(two_space_end)
        self._assert_output(expected_output)
    
    def test_log_output(self):
        self.assertFalse(self.logger.loggedMessages)
        self._feed_in_input('yeah')
        time.sleep(1)
        for x in range(10):
            try:
                self.assertTrue(self.logger.loggedMessages, 'Nothing output to logger.')
                return
            except AssertionError:
                if x > 8:
                    raise
        
    def _feed_in_input(self, input_string):
        """
        Put in the string characters onto the queue then start
        the thread.
        """
        for _ in range(1000): # Safer than while True
            try:
                self.msg_queue.get(block=False)
            except Empty:
                break
        for character in input_string:
            self.msg_queue.put(character)
        self.file_writer.perform_action = True
        
    def _assert_output(self, expected_output):
        for x in range(20):
            try:
                self.output_stream.seek(0)
                self.assertEqual(expected_output, self.output_stream.read())
            except AssertionError:
                if x > 8:
                    raise
                time.sleep(0.1)
            else:
                break
        
        self.output_stream.seek(0)

if __name__ == "__main__":
    unittest.main()