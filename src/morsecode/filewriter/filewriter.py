"""
Takes a stream of letters and outputs to file.
"""
from threading import Thread, Event
import time


class FileWriter(Thread):
    """
    The FileWriter listens to a stream of text. It flushes when it receives the AR end-of-message.
    Because a word can contain the letters AR, the input to this class should put a space between every 
    letter. Use two spaces to represent a space between words. The AR is replaced in the output with a double
    line break so that messages appear on seperate lines.   
    """
    
    END_OF_MESSAGE = 'AR'

    def __init__(self, inputStream, outputFile):
        """
        Constructor
        :param:inputStream A TextIO stream feeding messages in letters (i.e. not dots or dashes)
        :param:outputFile A file handle to output to.
        """
        self._stream = inputStream
        self._output = outputFile
        self.performAction = False
        self._terminated = Event()
        super(FileWriter, self).__init__()

        
    def run(self):
        """
        The main routine of the filewriter. Continuously listens to the
        stream of input. Opens a new file when a stream starts and flushes when AR is received.
        """
        while not self._terminated.wait(0.1):
            buffer = ''
            while self.performAction:
                text = self._stream.read()
                if text:
                    buffer += text
                    
                    if self.END_OF_MESSAGE in buffer:
                        messages = buffer.split(sep=self.END_OF_MESSAGE)
                        for message in messages[:-1]:
                            message = self._trimSpacing(message)
                            self._output.write(message + '\n\n')
                            self._output.flush()
                        buffer = messages[-1]                      
                else:
                    time.sleep(0.1)
                    
                
    def terminate(self):
        """
        Kill the thread completely
        """
        self._terminated.set()

    
    def _trimSpacing(self, string):
        """
        Trim the spacing in the string so that single spaces are removed and
        double spaces become a single one.
        """
        singleSpace = ' '
        doubleSpace = '  '
        result = ''
        
        words = string.split(doubleSpace)
        for word in words:
            result += word.replace(singleSpace, '')
            result += singleSpace
        while result.endswith(singleSpace):
            result = result[:-1]
        while result.startswith(singleSpace):
            result = result[1:]
        return result