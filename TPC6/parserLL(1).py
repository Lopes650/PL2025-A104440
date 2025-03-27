import ply.lex as lex

# Definição dos tokens
tokens = ('NUM', 'SUM', 'SUB', 'MUL', 'DIV', 'PA', 'PF')

t_NUM = r'\d+'
t_SUM = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_PA = r'\('
t_PF = r'\)'

def t_newline(t):
    
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    
    print('Caractere desconhecido:', t.value[0], 'Linha:', t.lexer.lineno)
    t.lexer.skip(1)

lexer = lex.lex()

def lexer_input(data):
    
    global lexer
    lexer.input(data)

def parserError(simb):
    
    raise SyntaxError(f"Erro sintático, token inesperado: {simb}")

def rec_term(simb):
    
    global prox_simb
    
    if prox_simb and prox_simb.type == simb:
        prox_simb = lexer.token()
        
    else:
        parserError(prox_simb)

def rec_Fator():
    
    global prox_simb
    
    if prox_simb is None:
        parserError('Esperado fator, mas acabou a entrada.')

    if prox_simb.type == 'NUM':
        
        valor = int(prox_simb.value)
        rec_term('NUM')
        return valor
    elif prox_simb.type == 'PA':
        
        rec_term('PA')
        valor = rec_Expressao()
        rec_term('PF')
        return valor
    else:
        parserError(prox_simb)

def rec_Termo():
    
    valor = rec_Fator()
    return rec_Termo2(valor)

def rec_Termo2(esq):
    
    global prox_simb
    
    if prox_simb is None:
        
        return esq
    if prox_simb.type == 'MUL':
        
        rec_term('MUL')
        fator = rec_Fator()
        return rec_Termo2(esq * fator)
    
    elif prox_simb.type == 'DIV':
        rec_term('DIV')
        fator = rec_Fator()
        
        return rec_Termo2(esq / fator)
    else:
        
        return esq

def rec_Expressao():
    valor = rec_Termo()
    return rec_Expressao2(valor)

def rec_Expressao2(esq):
    
    global prox_simb
    
    if prox_simb is None:
        return esq
    if prox_simb.type == 'SUM':
        rec_term('SUM')
        termo = rec_Termo()
        return rec_Expressao2(esq + termo)
    
    elif prox_simb.type == 'SUB':
        rec_term('SUB')
        termo = rec_Termo()
        return rec_Expressao2(esq - termo)
    
    else:
        return esq

def rec_Parser(data):
    global prox_simb
    lexer_input(data)
    prox_simb = lexer.token()
    resultado = rec_Expressao()
    print("Resultado:", resultado)
    return resultado

# Teste com entradas
rec_Parser("2+3")
rec_Parser("67-(2+3*4)")
rec_Parser("(9-2)*(13-4)")
