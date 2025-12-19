import ply.yacc as yacc
from r_interpreter.lexer import RLexer

class RParser:
    tokens = RLexer.tokens

    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('left', 'EQ', 'NE', 'GT', 'LT', 'GE', 'LE'),
    )

    def p_program(self, p):
        '''program : statements'''
        p[0] = p[1]

    def p_statements_multiple(self, p):
        '''statements : statements NEWLINE statement'''
        if p[3] is not None:
             p[0] = p[1] + [p[3]]
        else:
             p[0] = p[1]

    def p_statements_single(self, p):
        '''statements : statement'''
        if p[1] is not None:
            p[0] = [p[1]]
        else:
            p[0] = []

    def p_statement_assign(self, p):
        '''statement : IDENTIFIER ASSIGN expression'''
        p[0] = ('assign', p[1], p[3])

    def p_statement_expr(self, p):
        '''statement : expression'''
        p[0] = ('expr', p[1])
    
    def p_statement_empty(self, p):
        '''statement : empty'''
        p[0] = None

    def p_statement_if(self, p):
        '''statement : IF LPAREN expression RPAREN statement'''
        p[0] = ('if', p[3], p[5], None)

    def p_statement_if_else(self, p):
        '''statement : IF LPAREN expression RPAREN statement ELSE statement'''
        p[0] = ('if', p[3], p[5], p[7])

    def p_statement_while(self, p):
        '''statement : WHILE LPAREN expression RPAREN statement'''
        p[0] = ('while', p[3], p[5])

    def p_statement_for(self, p):
        '''statement : FOR LPAREN IDENTIFIER IN expression RPAREN statement'''
        p[0] = ('for', p[3], p[5], p[7])

    def p_statement_block(self, p):
        '''statement : LBRACE statements RBRACE'''
        p[0] = ('block', p[2])
    
    # Allow empty block {}
    def p_statement_empty_block(self, p):
        '''statement : LBRACE RBRACE'''
        p[0] = ('block', [])

    def p_expression_binop(self, p):
        '''expression : expression PLUS expression
                      | expression MINUS expression
                      | expression TIMES expression
                      | expression DIVIDE expression
                      | expression GT expression
                      | expression LT expression
                      | expression GE expression
                      | expression LE expression
                      | expression EQ expression
                      | expression NE expression'''
        p[0] = ('binop', p[2], p[1], p[3])

    def p_expression_group(self, p):
        '''expression : LPAREN expression RPAREN'''
        p[0] = p[2]

    def p_expression_number(self, p):
        '''expression : NUMBER'''
        p[0] = ('number', p[1])

    def p_expression_string(self, p):
        '''expression : STRING'''
        p[0] = ('string', p[1])

    def p_expression_identifier(self, p):
        '''expression : IDENTIFIER'''
        p[0] = ('identifier', p[1])

    def p_expression_call(self, p):
        '''expression : IDENTIFIER LPAREN args RPAREN'''
        p[0] = ('call', p[1], p[3])

    def p_args(self, p):
        '''args : args COMMA expression
                | expression'''
        if len(p) == 4:
            p[0] = p[1] + [p[3]]
        else:
            p[0] = [p[1]]

    def p_args_empty(self, p):
        '''args : empty'''
        p[0] = []

    def p_empty(self, p):
        'empty :'
        pass

    def p_error(self, p):
        if p:
            print(f"Syntax error at '{p.value}'")
        else:
            print("Syntax error at EOF")

    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)

    def parse(self, data):
        self.lexer = RLexer()
        self.lexer.build()
        return self.parser.parse(data, lexer=self.lexer.lexer)
