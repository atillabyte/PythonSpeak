import re

from fields import Fields

from Lexical.Lexer import Lexer
from Lexical.Parser import Parser
from Lexical.Token import Token

from Enum.TokenType import TokenType

from Page import Page

class DragonSpeakEngine:
    def __init__(self, options = None):
        self.options = options

        self.lexer = Lexer()
        self.parser = Parser(self.lexer)

        # set the default definitions unless overridden with the 'options' param
        self.lexer.add_definition(TokenType.Trigger,    re.compile('\(([0-9]{1})\:([0-9]{1,99999})\)'))
        self.lexer.add_definition(TokenType.String,     re.compile('\{(.*?)\}'))
        self.lexer.add_definition(TokenType.Number,     re.compile('[-+]?([0-9]*\.[0-9]+|[0-9]+)'))
        self.lexer.add_definition(TokenType.Comment,    re.compile('\".*[\r|\n]'), True)
        self.lexer.add_definition(TokenType.Word,       re.compile('\w+'), True)
        self.lexer.add_definition(TokenType.Symbol,     re.compile('\W'), True)
        self.lexer.add_definition(TokenType.Whitespace, re.compile('\s+'), True)

    def load_script(self, source_text, options = None):
        blocks = self.parser.parse(source_text)
        page = Page(self, options).insert(blocks)

        return page

# todo: implement custom token patterns
class DragonSpeakEngineOptions():
      pass

class DragonSpeakPageOptions(Fields.ignore_unhandled_cause_triggers[True]
                                     .allow_handler_overrides[False]
                                     .on_discover_trigger[None]): pass
