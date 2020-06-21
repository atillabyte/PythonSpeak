from builtins import int

from Trigger import Trigger
from Enum.TokenType import TokenType
from Enum.TriggerCategory import TriggerCategory

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

    def parse(self, source):
        current = None
        previous = None

        result = []
        block = []

        for token in self.lexer.tokenize(source):
            if token.type is TokenType.Trigger:
                if current is not None:
                    if previous is not None:
                        if previous.category is TriggerCategory.Effect:
                            if current.category is TriggerCategory.Cause:
                                result.append(block)
                                block = []
                    block.append(current)
                    previous = current
                
                category = TriggerCategory(int(token.value[0]))
                id = int(token.value[1])
                
                current = Trigger(category, id)
                current.index = token.position[0]
                current.line = token.position[1]
                current.column = token.position[2]

            elif token.type is TokenType.String:
                current.contents.append(str(token.value[0]))

            elif token.type is TokenType.Number:
                current.contents.append(float(token.value[0]))

            elif token.type is TokenType.EOF:
                if current is not None:
                    if current.category is not TriggerCategory.Undefined:
                        block.append(current)
                        result.append(block)

        return result
