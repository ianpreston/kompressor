import re
import enum


class TokenType(enum.Enum):
    INVALID = -1
    (IGNORE,
     DOT,
     IDENT,
     LPAREN,
     RPAREN,
     COMMA,
     STRING,
     INT,
     OPER,
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

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)


class Lexer:
    token_map = {
        TokenType.IGNORE: r' ',
        TokenType.IDENT: r'[a-zA-Z][A-Za-z0-9_]*',
        TokenType.DOT: r'\.',
        TokenType.LPAREN: r'\(',
        TokenType.RPAREN: r'\)',
        TokenType.COMMA: r',',
        TokenType.STRING: r'"(.*?)"',
        TokenType.INT: r'[0-9]+',
        TokenType.OPER: ':=',
        TokenType.SEMICOLON: r';',
    }

    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.cur_token = Token(None, '')

    def match_token(self):
        if not len(self.source):
            return Token(TokenType.EOF, 'EOF')

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
            if token.type == TokenType.EOF:
                yield token
                return
            if token.type == TokenType.IGNORE:
                continue
            yield token
