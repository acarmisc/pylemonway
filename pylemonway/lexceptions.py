class LemonwayException(Exception):
    def __init__(self, value, code=None):
        self.value = value
        self.code = code or value.code
    
    def __str__(self):
        return repr(self.value)
