'''
Morse Code input reading.
'''
from threading import Thread, Event
import sys


class InputReader(Thread):
    '''
    Listens to a switch for on/off (e.g. Raspberry Pi GPIO pin). Because this
    providing function can be passed in, this class is not dependent on the GPIO library.
    '''


    def __init__(self, morseSwitch, codeToLetterDict, outputStream):
        '''
        Constructor
        :param:morseSwitch: The function to poll for True or False such as GPIO.input().
        :param:codeToLetterDict A dictionary of letters to interpret morse code with.
        :param:outputStream The stream to output to.
        '''
        self._morseSwitch = morseSwitch
        self._codeDict = codeToLetterDict
        self._outputStream = outputStream
        self._terminated = Event()
        super(InputReader, self).__init__()
    
    
    def run(self):
        '''
        The main routine of the InputReader
        '''
        while not self._terminated.wait(0.01):
            if self._morseSwitch():
                print(1, end='')
            else:
                print(0, end='')
            sys.stdout.flush()
    
    def terminate(self):
        '''
        Kill the thread completely
        '''
        self._terminated.set()
    