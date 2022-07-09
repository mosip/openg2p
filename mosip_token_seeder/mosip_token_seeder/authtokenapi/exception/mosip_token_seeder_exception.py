class MOSIPTokenSeederException(Exception):
    def __init__(self, error_code, error_message):
        self.error_code = error_code
        self.error_message = error_message
        super().__init__(error_code)
    
    def __str__(self):
        return '[%s] %s' % (self.error_code, self.error_message)

class MOSIPTokenSeederNoException(MOSIPTokenSeederException):
    def __init__(self, error_code, error_message, return_status_code):
        self.return_status_code = return_status_code
        super().__init__(error_code, error_message)