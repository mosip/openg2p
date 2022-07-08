class MOSIPTokenSeederException(Exception):
    def __init__(self, error_code, error_message):
        # super(error_code)
        self.error_code = error_code
        self.error_message = error_message