import ply.lex as lex
import ply.yacc as yacc

class LexerAnalyzer:
    tokens = [
        'IDENTIFICADOR', 'TIPO', 'PUNTOYCOMA', 'PALABRA_RESERVADA', 'CORCHETES_ABRE',
        'CORCHETES_CIERRA', 'PARENTESIS_ABRE', 'PARENTESIS_CIERRA', 'FUNCION', 'CONDICIONAL',
        'NUMERO', 'LLAVES_ABRE','LLAVES_CIERRA'
    ]

    t_PUNTOYCOMA = r'\;'
    t_CORCHETES_ABRE = r'\['
    t_CORCHETES_CIERRA = r'\]'
    t_PARENTESIS_ABRE = r'\('
    t_PARENTESIS_CIERRA = r'\)'
    t_LLAVES_ABRE = r'\{'
    t_LLAVES_CIERRA = r'\}'
    
    t_ignore = ' \t\n'
    def t_PALABRA_RESERVADA(self, t):
        r'contenido|Vi|War|Fun|Malph'
        return t
    def t_FUNCION(self, t):
        r'[A-Z][a-z]*'
        return t

    def t_CONDICIONAL(self, t):
        r'\>|\<|\='
        return t
    def t_TIPO(self, t):
        r'int|string'
        return t
    
    
    def t_IDENTIFICADOR(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        return t

    def t_NUMERO(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_error(self, t):
        print(f"Carácter desconocido '{t.value[0]}'")
        t.lexer.skip(1)

    def __init__(self):
        self.lexer = lex.lex(module=self)
        self.parser = yacc.yacc(module=self)
        self.errors = []

    def analyze(self, data):
        self.lexer.input(data)
        result = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            result.append((tok.type, tok.value))
        return result

    def parse(self, data):
        self.errors = []
        result = self.parser.parse(data)
        if self.errors:
            return False, self.errors
        return True, result

    def p_program(self, p):
        '''
        program : expression
        '''
        p[0] = p[1]

    def p_expression(self, p):
        '''
        expression : variable_declaration
                   | main_method
                   | function_definition
                   | while_loop
                   | if_statement
        '''
        p[0] = p[1]
    def p_identificador_o_numero(self, p):
        '''
        identificador_o_numero : IDENTIFICADOR
                           | NUMERO
        '''
        p[0] = p[1]
    def p_condicional_simple_o_doble(self, p):
        '''
        condicional_simple_o_doble : CONDICIONAL
                                   | CONDICIONAL CONDICIONAL
        '''
        if len(p) == 2:  # Solo un condicional
            p[0] = p[1]
        else:  # Dos condicionales
            p[0] = (p[1], p[2])

    def p_variable_declaration(self, p):
        'variable_declaration : IDENTIFICADOR PUNTOYCOMA TIPO'
        p[0] = ('variable_declaration', p[1])

    def p_main_method(self, p):
        'main_method : PALABRA_RESERVADA PALABRA_RESERVADA CORCHETES_ABRE CORCHETES_CIERRA PARENTESIS_ABRE PALABRA_RESERVADA PARENTESIS_CIERRA'
        p[0] = ('main_method')

    def p_function_definition(self, p):
        'function_definition : PALABRA_RESERVADA FUNCION CORCHETES_ABRE CORCHETES_CIERRA PARENTESIS_ABRE PALABRA_RESERVADA PARENTESIS_CIERRA'
        p[0] = ('function_definition', p[2])

    def p_while_loop(self, p):
        'while_loop : PALABRA_RESERVADA LLAVES_ABRE identificador_o_numero condicional_simple_o_doble identificador_o_numero LLAVES_CIERRA PARENTESIS_ABRE PALABRA_RESERVADA PARENTESIS_CIERRA'
        p[0] = ('while_loop', p[3], p[4], p[5])

    def p_if_statement(self, p):
        '''
        if_statement : PALABRA_RESERVADA LLAVES_ABRE identificador_o_numero condicional_simple_o_doble identificador_o_numero LLAVES_CIERRA PARENTESIS_ABRE PALABRA_RESERVADA PARENTESIS_CIERRA
        '''
        p[0] = ('if_statement', p[3], p[4], p[5])


    def p_error(self, p):
        if p:
            error_msg = f"Error de sintaxis en '{p.value}', línea {p.lineno}"
            self.errors.append(error_msg)
            print(error_msg)
        else:
            print("Error de sintaxis al final del archivo")
            self.errors.append("Error de sintaxis al final del archivo")

if __name__ == "__main__":
    analyzer = LexerAnalyzer()
    test_data = "War{val1>val2}(contenido)"
    success, result = analyzer.parse(test_data)
    if not success:
        print("Se encontraron errores:")
        for error in result:
            print(error)
    else:
        print("Análisis completado sin errores.")
