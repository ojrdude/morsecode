"""
Logging utility.
"""
from _datetime import datetime


class Logger(object):
    """
    Logging class that writes log information to an
    output file. If debug is True, then the output will
    also be output to stdout.
    """
    
    def __init__(self, log_file, debug=False):
        """
        Constructor
        :param:log_file: The location of the log file
        :param:debug: If True, the logs will be printed to stdout
            in addition to the log file. Default: False
        """
        self._log_file = log_file
        self._debug = debug
        
        
    def log(self, application, message):
        """
        Print a log to the log file. If running in
        debug mode, print it to stdout also.
        :param:application: The application that has sent the log.
            (name as a str)
        :param:message: The message to print.
        """
        now = datetime.now()
        with open(self._log_file, 'a') as log_file:
            log_file.write('{time} - {app}: {message}\n'.format(time=now,
                                                              app=application,
                                                              message=message))
        if self._debug:
            print('{app}: {message}'.format(app=application,
                                            message=message))