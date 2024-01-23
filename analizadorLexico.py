import ply.lex as lex

class LexerAnalyzer:
    
    tokens = [
        'VARIABLE', 'TIPO', 'PUNTO_Y_COMA',
        'FUNCION', 'NOMBRE_FUNCION', 'ABRIR_CORCHETE', 'CERRAR_CORCHETE',
        'ABRIR_LLAVES', 'CONTENIDO', 'CERRAR_LLAVES',
        'CONDICIONAL', 'ABRIR_PARENTESIS', 'CERRAR_PARENTESIS', 'OPERADOR', 'NUMERO', 'CICLO', 'MAIN'
    ]

    
    t_PUNTO_Y_COMA = r';'
    t_ABRIR_CORCHETE = r'\['
    t_CERRAR_CORCHETE = r'\]'
    t_ABRIR_LLAVES = r'\{'
    t_CERRAR_LLAVES = r'\}'
    t_ABRIR_PARENTESIS = r'\('
    t_CERRAR_PARENTESIS = r'\)'
    t_TIPO = r'\bint\b|\bstring\b'
    t_ignore = ' \t'

    
    def t_CONTENIDO(self, t):
        r'contenido'
        return t

    def t_CONDICIONAL(self, t):
        r'Vi'
        return t

    def t_CICLO(self, t):
        r'War'
        return t

    def t_FUNCION(self, t):
        r'Fun'
        return t

    def t_MAIN(self, t):
        r'Malph'
        return t

    def t_NUMERO(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_OPERADOR(self, t):
        r'[><=]'
        return t

    def t_NOMBRE_FUNCION(self, t):
        r'[A-Z][a-zA-Z0-9]*'
        return t

    def t_VARIABLE(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        return t


    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    
    def __init__(self):
        self.lexer = lex.lex(module=self)

    
    def analyze(self, data):
        self.lexer.input(data)
        result = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            result.append((tok.type, tok.value))
        return result
