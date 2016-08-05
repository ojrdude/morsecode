
class MorseCode(object):
    _MORSE_CODE_MAP = {
            'a': '.-',
            'b': '-...',
            'c': '-.-.',
            'd': '-..',
            'e': '.',
            'f': '..-.',
            'g': '--.',
            'h': '....',
            'i': '..',
            'j': '.---',
            'k': '-.-',
            'l': '.-..',
            'm': '--',
            'n': '-.',
            'o': '---',
            'p': '.--.',
            'q': '--.-',
            'r': '.-.',
            's': '...',
            't': '-',
            'u': '..-',
            'v': '...-',
            'w': '.--',
            'x': '-..-',
            'y': '-.--',
            'z': '--..',
            '1': '.----',
            '2': '..---',
            '3': '...--',
            '4': '....-',
            '5': '.....',
            '6': '-....',
            '7': '--...',
            '8': '---..',
            '9': '----.',
            '0': '-----',
        }
    _DOT_LENGTH = 1
    _DASH_LENGTH = 3
    _MID_LETTER_LENGTH = 1
    _LETTER_SPACE_LENGTH = 3
    _WORD_SPACE_LENGTH = 7
    
    def _letterToMorseCode(self, letter):
        """
        Converts a letter to Morse Code
        """
        try:
            return self._MORSE_CODE_MAP[letter.lower()]
        except AttributeError:
            #TODO: Log out that an invalid letter was received.
        
