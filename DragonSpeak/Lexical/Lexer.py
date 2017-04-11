import re

from Lexical.Token import Token, Definition
from Enum.TokenType import TokenType

class Lexer:
    def __init__(self):
        self.token_definitions = [];
        self.term_pattern = re.compile('\r\n|\r|\n')

    def add_definition(self, type, pattern, ignored = False):
        definition = Definition(type, pattern, ignored)
        self.token_definitions.append(definition)

    def tokenize(self, source):
        cur_index = 0
        cur_line = 1
        cur_column = 0

        while cur_index < len(source):
            match_token = None

            for definition in self.token_definitions:
                matches = definition.pattern.search(source, cur_index)
                success = matches is not None and (matches.regs is not None and len(matches.regs) >= 1)

                if not success: continue

                match = matches.regs[0]
                index = match[0]
                length = match[1] - index

                if index - cur_index != 0: continue

                value = source[index:index+length]
                terminator = self.term_pattern.search(value)

                cur_index += length
                cur_line += [0 if terminator is None or terminator.regs is None or len(terminator.regs) < 1 else 1][0]
                cur_column = [cur_column + length if terminator is None else len(value) - (terminator.regs[0][0] + terminator.regs[0][1])][0]

                match_token = Token(definition.type, matches.groups(), [cur_index, cur_line, cur_column])
                break

            if definition.ignored is False:
                yield match_token

        yield Token(TokenType.EOF, None, [cur_index, cur_line, cur_column])
