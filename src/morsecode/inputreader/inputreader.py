"""
Morse Code input reading.
"""
from datetime import datetime, timedelta
from threading import Thread, Event


class InputReader(Thread):
    """
    Listens to a switch for on/off (e.g. Raspberry Pi GPIO pin). Because this
    providing function can be passed in, this class is not dependent on the GPIO library.
    """

    
    def __init__(self, morse_switch, code_to_letter_dict, msg_queue,
                 logger, debug=False, config=None):
        """
        Constructor
        :param:morse_switch: The function to poll for True or False such as GPIO.input().
        :param:code_to_letter_dict A dictionary of letters to interpret Morse code with.
        :param:msg_queue The message queue to output to.
        :param:logger: A logging class to send logs to.
        :param:debug: True to print logging to stdout as well as log file.
        :param:config: A dict containing all the timing values for the reader.
        """
        self._morse_switch = morse_switch
        self._codeDict = code_to_letter_dict
        self._msg_queue = msg_queue
        self._debug = debug
        self._terminated = Event()
        self._current_letter = ''
        self._logger = logger
        self._last_state = False
        super(InputReader, self).__init__()
        
    def run(self):
        """
        The main routine of the InputReader
        """
        self._current_letter = ''
        while not self._terminated.wait(0.01):
            if self._morse_switch():
                self._current_letter += self._detect_dot_or_dash()
            else:
                self._detect_gap()
                
    def _detect_dot_or_dash(self):
        """
        Monitor the Morse Key, measuring how long it takes to turn
        off. Return '-' if the duration is long, and return '.' if not.
        """
        self._logger.log('Input', 'Detecting Dot or Dash')
        start_time = datetime.now()
        while self._morse_switch():
            pass
        end_time = datetime.now()
        difference = end_time - start_time
        if difference > timedelta(seconds=1.5):
            return '-'
        else:
            return '.'
        
    def _detect_gap(self):
        """
        Monitor the Morse Key, measuring how long it takes to turn
        on again. If the wait is very long, put a space on the
        message queue. If the wait is long enough, but shorter than
        a space, put the current letter on the queue.
        """
        self._logger.log('Input', 'Detecting Gap')
        start_time = datetime.now()
        while not self._morse_switch():
            difference = datetime.now() - start_time
            if difference > timedelta(seconds = 13): # Fudge end of message
                self._logger.log('Input', 'Very long pause treated as End of Message')
                self._current_letter = ''
                self._msg_queue.put('AR')
                return
        end_time = datetime.now()
        difference = end_time - start_time
        if difference > timedelta(seconds=6.5): # About 7 seconds
            self._logger.log('Input', 'Space detected')
            self._msg_queue.put('  ')
        elif difference > timedelta(seconds=2.7): # About 3 seconds
            self._print_current_letter()            
        
    def _print_current_letter(self):
        """
        Put the current letter on the message queue
        """
        try:
            self._logger.log('Input', 'Putting Letter On Queue')
            self._msg_queue.put(self._codeDict[self._current_letter])
        except KeyError:
            self._logger.log('Input', 'Unknown Letter. Putting raw Morse Code' +\
                             'On Queue')
            self._msg_queue.put("?{}?".format(self._current_letter))
        
        self._msg_queue.put(' ')
        self._current_letter = ''
    
    def terminate(self):
        """
        Kill the thread completely
        """
        self._terminated.set()