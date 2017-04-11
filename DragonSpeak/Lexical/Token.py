class Token:
    def __init__(self, type, value, position):
        self.type = type
        self.value = value
        self.position = position

class Definition:
    def __init__(self, type, pattern, ignored = False):
        self.type = type
        self.pattern = pattern
        self.ignored = ignored
