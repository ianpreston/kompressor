class PrattParser:
    lbp_map = {}
    nud_map = {}
    led_map = {}

    @classmethod
    def register_token(cls, token_type, lbp, nud, led):
        cls.lbp_map[token_type] = lbp
        cls.nud_map[token_type] = nud
        cls.led_map[token_type] = led

    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = 0

    @property
    def token(self):
        if self.idx >= len(self.tokens):
            return None
        return self.tokens[self.idx]

    @property
    def last_token(self):
        return self.tokens[self.idx-1]

    def advance(self):
        self.idx += 1

    def program(self):
        return self.expr()

    def expr(self, rbp=0):
        left = self.nud(self.token)
        while rbp < self.lbp(self.token):
            self.advance()
            if not self.token:
                return left
            left = self.led(left, self.last_token)
        return left

    def nud(self, token):
        cable = self.nud_map.get(token.type)
        if not cable:
            raise Exception('Unexpected token', token)
        return cable(token)

    def led(self, left, token):
        cable = self.led_map.get(token.type)
        if not cable:
            raise Exception('Unexpected token', token)
        return cable(self, left, token)

    def lbp(self, token):
        return self.lbp_map.get(token.type, 1)
