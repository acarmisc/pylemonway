class LemonwayException(Exception):
    def __init__(self, value, code):
        self.value = value
        self.code = code
    
    def __str__(self):
        return repr(self.value)
