import ply.lex as lex

class LexerAnalyzer:
    
    tokens = [
        'IDENTIFICADORES', 'TIPO', 'SIGNOS',
         'CORCHETES','LLAVES', 'PALABRA_RESERVADA',
        'PARENTESIS', 'NUMERO','ASIGNACION', 'DESCONOCIDO'
    ]

    t_ASIGNACION = r'\='
    t_CORCHETES = r'\[|\]'
    t_LLAVES = r'\{|\}'
    t_PARENTESIS = r'\(|\)'
    t_TIPO = r'\bint\b|\bstring\b'
    t_ignore = ' \t\n'

    def t_PALABRA_RESERVADA(self, t):
        r'contenido|Vi|War|Fun|Malph'
        return t

    def t_NUMERO(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_SIGNOS(self, t):
        r'[><;]'
        return t

    def t_IDENTIFICADORES(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        return t

    

    def t_error(self, t):
        if t.value[0].isspace():  
            self.lexer.skip(1)    
        else:
            print(f"Carácter desconocido '{t.value[0]}'")
            t.type = 'DESCONOCIDO'  
            t.value = t.value[0]    
            self.lexer.skip(1)
            return t 
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


lexer_analyzer = LexerAnalyzer()
input_data = "int x = 10; // Esto es un ejemplo con un + desconocido"
result = lexer_analyzer.analyze(input_data)
for token in result:
    print(token)
