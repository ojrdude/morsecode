"""
Takes a stream of letters and outputs to file.
"""
from threading import Thread, Event


class FileWriter(Thread):
    """
    The FileWriter continuously polls a queue for text. It flushes when it receives the AR end-of-message.
    Because a word can contain the letters AR, the input to this class should put a space between every 
    letter. Use two spaces to represent a space between words. The AR is replaced in the output with a double
    line break so that messages appear on separate lines.   
    """
    
    END_OF_MESSAGE = 'AR'

    def __init__(self, msg_queue, output_file, logger, debug=False):
        """
        Constructor
        :param:msg_queue A queue feeding messages in letters (i.e. not dots or dashes)
        :param:output_file A file handle to output to.
        :param:_logger: A logging class to send logs to.
        """
        self._msg_queue = msg_queue
        self._output = output_file
        self.perform_action = False
        self._debug = debug
        self._logger = logger
        self._terminated = Event()
        super(FileWriter, self).__init__()

        
    def run(self):
        """
        The main routine of the filewriter. Continuously polls the message queue.
        Opens a new file when a stream starts and flushes when AR is received.
        """
        while not self._terminated.wait(0.1):
            buffer = ''
            while self.perform_action:
                
                self._logger.log('FileWriter', 'Polling Message Queue')
                buffer += self._msg_queue.get()
                self._logger.log('FileWriter', 'Retrieved from Message Queue. Buffer = '
                                 + buffer)
                
                if self.END_OF_MESSAGE in buffer:
                    self._logger.log('FileWriter', 'AR in buffer')
                    messages = buffer.split(sep=self.END_OF_MESSAGE)
                    for message in messages[:-1]:
                        message = self._trim_spacing(message)
                        self._logger.log('FileWriter', 'Writing message: ' + message)
                        self._output.write(message + '\n\n')
                        self._output.flush()
                    buffer = messages[-1]  
                    self._logger.log('FileWriter', 'Buffer trimmed. Buffer = ' + buffer)
                    
                
    def terminate(self):
        """
        Kill the thread completely
        """
        self._terminated.set()

    
    def _trim_spacing(self, string):
        """
        Trim the spacing in the string so that single spaces are removed and
        double spaces become a single one.
        """
        single_space = ' '
        double_space = '  '
        result = ''
        
        words = string.split(double_space)
        for word in words:
            result += word.replace(single_space, '')
            result += single_space
        while result.endswith(single_space):
            result = result[:-1]
        while result.startswith(single_space):
            result = result[1:]
        return result