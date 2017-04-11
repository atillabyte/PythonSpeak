from enum import IntEnum

class TokenType(IntEnum):
    Trigger = 1,
    String = 2,
    Number = 3,
    Array = 4,
    Comment = 5,
    Whitespace = 6,
    Word = 7,
    Symbol = 8,
    EOF = 9
