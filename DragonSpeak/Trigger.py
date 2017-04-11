class Trigger:
    def __init__(self, category, id):
        self.category = category
        self.id = id

        self.index = None
        self.line = None
        self.column = None

        self.description = None
        self.contents = []

        self.cause = None
        self.conditions = []
        self.areas = []
        self.filters = []
        self.effects = []

    def get_string(self, index):
        try:
            if type(self.contents[index]) == str:
                return self.contents[index]
            else: raise ValueError('The object at index {0} is type "{1}" not "{2}".'
                .format(index, self.contents[index].__class__.__name__, 'str'))
        except IndexError:
            raise IndexError('There are no objects at index {0}.'.format(index),
                             '({0}:{1}) at index {2}, line {3}, column {4}.'.format(int(self.category), int(self.id), self.index, self.line, self.column))
    
    def get_number(self, index):
        try:
            if type(self.contents[index]) == float:
                return self.contents[index]
            else: raise ValueError('The object at index {0} is type "{1}" not "{2}".'
                .format(index, self.contents[index].__class__.__name__, 'float'))
        except IndexError:
            raise IndexError('There are no objects at index {0}.'.format(index),
                            '({0}:{1}) at index {2}, line {3}, column {4}.'.format(int(self.category), int(self.id), self.index, self.line, self.column))
    
    def __eq__(self, trigger):
        return self.category == trigger.category and self.id == trigger.id

    def __hash__(self):
        return self.category * 31 + self.id
