import re
import enum


class TokenType(enum.Enum):
    INVALID = -1
    (IGNORE,
     PASS,
     IDENT,
     LPAREN,
     RPAREN,
     COMMA,
     STRING,
     INT,
     ASSIGNMENT,
     SEMICOLON,
     EOF) = range(11)


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return '<Token {type} "{value}">'.format(
            type=self.type,
            value=self.value,
        )


class Lexer:
    token_map = {
        TokenType.IGNORE: r' ',
        TokenType.IDENT: r'[a-zA-Z][A-Za-z0-9_]*',
        TokenType.PASS: r'\.',
        TokenType.LPAREN: r'\(',
        TokenType.RPAREN: r'\)',
        TokenType.COMMA: r',',
        TokenType.STRING: r'"(.*?)"',
        TokenType.INT: r'[0-9]+',
        TokenType.ASSIGNMENT: ':=',
        TokenType.SEMICOLON: r';',
    }

    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.cur_token = Token(None, '')

    def match_token(self):
        if not len(self.source):
            return

        for token_type, regex in self.token_map.items():
            match = re.match(regex, self.source)
            if not match:
                continue

            if match.groups():
                text, value = match.group(0), match.group(1)
            else:
                text = value = match.group(0)

            _, _, self.source = self.source.partition(text)

            return Token(token_type, value)

        raise Exception('Unmatched input', self.source)

    def iter_match_tokens(self):
        while True:
            token = self.match_token()
            if not token:
                return
            if token.type == TokenType.IGNORE:
                continue
            yield token
