class node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
    def __repr__(self) -> str:
        if self.left and self.right:
            return f"[{self.left} {self.value} {self.right}]"
        if self.left:
            return f"[{self.left} {self.value}]"
        if self.right:
            return f"[{self.value} {self.right}]"
        return f"[{self.value}]"

class mathRunner:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.current_token = self.tokens[self.index]
        self.result = 0
        self.ast = []
    def error(self):
        raise Exception('Invalid syntax')
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.index += 1
            if self.index > len(self.tokens) - 1:
                self.current_token = None
            else:
                self.current_token = self.tokens[self.index]
        else:
            self.error()
    def factor(self):
        token = self.current_token
        if token.type == 'INTEGER':
            self.eat('INTEGER')
            return node(token.value)
        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            result = self.expr()
            self.eat('RPAREN')
            return result
    def term(self):
        result = self.factor()
        while self.current_token and self.current_token.type in ('MUL', 'DIV'):
            token = self.current_token
            if token.type == 'MUL':
                self.eat('MUL')
                result = node('*')
                result.left = result
                result.right = self.factor()
            elif token.type == 'DIV':
                self.eat('DIV')
                result = node('/')
                result.left = result
                result.right = self.factor()
        return result
    def expr(self):
        result = self.term()
        while self.current_token and self.current_token.type in ('PLUS', 'MINUS'):
            token = self.current_token
            if token.type == 'PLUS':
                self.eat('PLUS')
                result = node('+')
                result.left = result
                result.right = self.term()
            elif token.type == 'MINUS':
                self.eat('MINUS')
                result = node('-')
                result.left = result
                result.right = self.term()
        return result
    def parse(self):
        self.ast = self.expr()
        return self.ast
