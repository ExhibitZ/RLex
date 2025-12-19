import ply.lex as lex

class RLexer:
    tokens = (
        'IDENTIFIER', 'NUMBER', 'STRING',
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
        'ASSIGN', 'LPAREN', 'RPAREN', 'COMMA',
        'LBRACE', 'RBRACE',
        'NEWLINE', 'GT', 'LT', 'GE', 'LE', 'EQ', 'NE',
        'IF', 'ELSE', 'WHILE', 'FOR', 'IN'
    )

    # Reserved words
    reserved = {
        'if': 'IF',
        'else': 'ELSE',
        'while': 'WHILE',
        'for': 'FOR',
        'in': 'IN'
    }

    # Regular expression rules for simple tokens
    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_TIMES   = r'\*'
    t_DIVIDE  = r'/'
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_LBRACE  = r'\{'
    t_RBRACE  = r'\}'
    t_COMMA   = r','
    t_GT      = r'>'
    t_LT      = r'<'
    t_GE      = r'>='
    t_LE      = r'<='
    t_EQ      = r'=='
    t_NE      = r'!='

    def t_ASSIGN(self, t):
        r'<-|='
        return t

    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_.][a-zA-Z0-9_.]*'
        t.type = self.reserved.get(t.value, 'IDENTIFIER')    # Check for reserved words
        return t

    def t_NUMBER(self, t):
        r'\d+(\.\d*)?|\.\d+'
        if '.' in t.value:
            t.value = float(t.value)
        else:
            t.value = int(t.value)
        return t

    def t_STRING(self, t):
        r'\"([^\\\n]|(\\.))*?\"|\'([^\\\n]|(\\.))*?\''
        t.value = t.value[1:-1] # Strip quotes
        return t

    def t_NEWLINE(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        return t

    # Ignored characters
    t_ignore  = ' \t'

    def t_COMMENT(self, t):
        r'\#.*'
        pass # No return value. Token discarded

    def t_error(self, t):
         # invalid character
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def input(self, data):
        self.lexer.input(data)

    def token(self):
        return self.lexer.token()
