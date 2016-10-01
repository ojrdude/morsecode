"""
Morse Code input reading.
"""
from datetime import datetime
import sys
from threading import Thread, Event


class InputReader(Thread):
    """
    Listens to a switch for on/off (e.g. Raspberry Pi GPIO pin). Because this
    providing function can be passed in, this class is not dependent on the GPIO library.
    """
    REL_DOT_DURATION = 1
    REL_MID_LETTER_GAP = 1
    REL_DASH_DURATION = 3
    REL_LETTER_GAP = 3
    REL_WORD_GAP = 7
    STANDARD_DURATION_MS = 100
    _ERROR_MARGIN = 1.3

    def __init__(self, morse_switch, code_to_letter_dict, msg_queue):
        """
        Constructor
        :param:morse_switch: The function to poll for True or False such as GPIO.input().
        :param:code_to_letter_dict A dictionary of letters to interpret Morse code with.
        :param:msg_queue The message queue to output to.
        """
        self._morse_switch = morse_switch
        self._codeDict = code_to_letter_dict
        self._msg_queue = msg_queue
        self._terminated = Event()
        self._current_letter = ''
        super(InputReader, self).__init__()
    

    def run(self):
        """
        The main routine of the InputReader
        """
        self._current_letter = ''
        last_state = False
        last_change_time = datetime.now()
        while not self._terminated.wait(0.01):
            state_now = self._morse_switch()
            time_since_last_change = datetime.now() - last_change_time
            time_since_last_change = time_since_last_change.total_seconds() * 1000
            if time_since_last_change > self.STANDARD_DURATION_MS * self.REL_WORD_GAP * self._ERROR_MARGIN:
                if len(self._current_letter) == 0:
                    continue
                self._print_current_letter()
            
            if state_now == last_state:
                continue
            
            last_state = state_now
            duration = (datetime.now() - last_change_time)
            duration = duration.total_seconds() * 1000
            last_change_time = datetime.now()
            if not state_now:
                # End of a dot/dash
                
                if duration > self.STANDARD_DURATION_MS * self.REL_DOT_DURATION * self._ERROR_MARGIN:
                    self._current_letter += "-"
                else:
                    self._current_letter += "."
            
            else:
                # End of a pause
                if duration > self.STANDARD_DURATION_MS * self.REL_MID_LETTER_GAP * self._ERROR_MARGIN:
                    if len(self._current_letter) == 0:
                        continue
                    
                    self._print_current_letter()
                    
                    self._msg_queue.put(' ')
                    if duration > self.STANDARD_DURATION_MS * self.REL_LETTER_GAP * self._ERROR_MARGIN:
                        self._msg_queue.put(' ')
                     
                else:   
                    # Mid-letter pause
                    continue
                
                
            sys.stdout.flush()
    
    
    def _print_current_letter(self):
        try:
            self._msg_queue.put(self._codeDict[self._current_letter])
        except KeyError:
            self._msg_queue.put("?{}?".format(self._current_letter))
        self._current_letter = ''
         
    
    
    def terminate(self):
        """
        Kill the thread completely
        """
        self._terminated.set()
    