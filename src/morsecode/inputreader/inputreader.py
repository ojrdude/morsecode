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

    def __init__(self, morseSwitch, codeToLetterDict, msgQueue):
        """
        Constructor
        :param:morseSwitch: The function to poll for True or False such as GPIO.input().
        :param:codeToLetterDict A dictionary of letters to interpret Morse code with.
        :param:msgQueue The message queue to output to.
        """
        self._morseSwitch = morseSwitch
        self._codeDict = codeToLetterDict
        self._msgQueue = msgQueue
        self._terminated = Event()
        self._currentLetter = ''
        super(InputReader, self).__init__()
    

    def run(self):
        """
        The main routine of the InputReader
        """
        self._currentLetter = ''
        lastState = False
        lastChangeTime = datetime.now()
        while not self._terminated.wait(0.01):
            stateNow = self._morseSwitch()
            timeSinceLastChange = datetime.now() - lastChangeTime
            timeSinceLastChange = timeSinceLastChange.total_seconds() * 1000
            if timeSinceLastChange > self.STANDARD_DURATION_MS * self.REL_WORD_GAP * self._ERROR_MARGIN:
                if len(self._currentLetter) == 0:
                    continue
                self._printCurrentLetter()
            
            if stateNow == lastState:
                continue
            
            lastState = stateNow
            duration = (datetime.now() - lastChangeTime)
            duration = duration.total_seconds() * 1000
            lastChangeTime = datetime.now()
            if not stateNow:
                # End of a dot/dash
                
                if duration > self.STANDARD_DURATION_MS * self.REL_DOT_DURATION * self._ERROR_MARGIN:
                    self._currentLetter += "-"
                else:
                    self._currentLetter += "."
            
            else:
                # End of a pause
                if duration > self.STANDARD_DURATION_MS * self.REL_MID_LETTER_GAP * self._ERROR_MARGIN:
                    if len(self._currentLetter) == 0:
                        continue
                    
                    self._printCurrentLetter()
                    
                    self._msgQueue.put(' ')
                    if duration > self.STANDARD_DURATION_MS * self.REL_LETTER_GAP * self._ERROR_MARGIN:
                        self._msgQueue.put(' ')
                     
                else:   
                    # Mid-letter pause
                    continue
                
                
            sys.stdout.flush()
    
    
    def _printCurrentLetter(self):
        try:
            self._msgQueue.put(self._codeDict[self._currentLetter])
        except KeyError:
            self._msgQueue.put("?{}?".format(self._currentLetter))
        self._currentLetter = ''
         
    
    
    def terminate(self):
        """
        Kill the thread completely
        """
        self._terminated.set()
    