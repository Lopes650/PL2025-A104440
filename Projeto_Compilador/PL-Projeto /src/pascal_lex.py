# Analisador Léxico para Pascal Standard - ISO 7185

import ply.lex as lex

tokens = [
    'LESSGREAT', 'LESSEQUALS', 'GREATEQUALS', 'ATRIBUTION', 'DOUBLEPERIOD',
    'PLUSEQUALS', 'MINUSEQUALS', 'TIMESEQUALS', 'DIVIDEEQUALS', 'LBRACKETSUB', 'RBRACKETSUB',

    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS', 'LESSTHAN', 'GREATERTHAN', 'LBRACKET', 'RBRACKET',
    'PERIOD', 'COMMA', 'LPAREN', 'RPAREN', 'COLON', 'SEMICOLON', 'CARET',

    'IDENTIFIER', 'NUMBER', 'STRING_LITERAL', 'CHAR_LITERAL', 'BOOLEAN_LITERAL', 'FUNCTION_NAME', 'PROCEDURE_NAME',

    'AND','ARRAY','BEGIN','CASE','CONST','DIV','DOWNTO','DO','ELSE','END', 'FILE','FOR','FUNCTION','GOTO','IF','IN',
    'LABEL','MOD','NIL','NOT', 'OF','OR','PACKED','PROCEDURE','PROGRAM','RECORD','REPEAT','SET', 'THEN','TO','TYPE',
    'UNTIL','VAR','WHILE','WITH',

    'INTEGER','BOOLEAN','REAL','CHAR','STRING'
]

# <> <= >= := .. += -= *= /= (. .)
# + - * / = < > [ ] . , ( ) : ; ^

#* Pares de Símbolos Reservados

t_LESSGREAT = r'<>'
t_LESSEQUALS = r'<='
t_GREATEQUALS = r'>='
t_ATRIBUTION = r':='
t_DOUBLEPERIOD = r'\.\.'
t_PLUSEQUALS = r'\+='
t_MINUSEQUALS = r'-='
t_TIMESEQUALS = r'\*='
t_DIVIDEEQUALS = r'/='
t_LBRACKETSUB = r'\(\.'
t_RBRACKETSUB = r'\.\)'

#* Símbolos Reservados

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LESSTHAN = r'<'
t_GREATERTHAN = r'>'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_PERIOD = r'\.'
t_COMMA = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COLON = r':'
t_SEMICOLON = r';'
t_CARET = r'\^'

#* Palavras reservadas e números

# Tipos básicos
def t_INTEGER(t):  r'[iI][nN][tT][eE][gG][eE][rR]';  t.type='INTEGER';  return t
def t_BOOLEAN(t):  r'[bB][oO][oO][lL][eE][aA][nN]';  t.type='BOOLEAN';  return t
def t_REAL(t):     r'[rR][eE][aA][lL]';     t.type='REAL';     return t
def t_CHAR(t):     r'[cC][hH][aA][rR]';     t.type='CHAR';     return t
def t_STRING(t):   r'[sS][tT][rR][iI][nN][gG]';   t.type='STRING';   return t

# ——— Palavras Reservadas ISO 7185 ———

def t_AND(t):      r'[aA][nN][dD]';      t.type='AND';      return t
def t_ARRAY(t):    r'[aA][rR][rR][aA][yY]';    t.type='ARRAY';    return t
def t_BEGIN(t):    r'[bB][eE][gG][iI][nN]';    t.type='BEGIN';    return t
def t_CASE(t):     r'[cC][aA][sS][eE]';     t.type='CASE';     return t
def t_CONST(t):    r'[cC][oO][nN][sS][tT]';    t.type='CONST';    return t
def t_DIV(t):      r'[dD][iI][vV]';      t.type='DIV';      return t
def t_DOWNTO(t):   r'[dD][oO][wW][nN][tT][oO]';   t.type='DOWNTO';   return t
def t_DO(t):       r'[dD][oO]';       t.type='DO';       return t
def t_ELSE(t):     r'[eE][lL][sS][eE]';     t.type='ELSE';     return t
def t_END(t):      r'[eE][nN][dD]';      t.type='END';      return t
def t_FILE(t):     r'[fF][iI][lL][eE]';     t.type='FILE';     return t
def t_FOR(t):      r'[fF][oO][rR]';      t.type='FOR';      return t
def t_FUNCTION(t): r'[fF][uU][nN][cC][tT][iI][oO][nN]'; t.type='FUNCTION'; return t
def t_GOTO(t):     r'[gG][oO][tT][oO]';     t.type='GOTO';     return t
def t_IF(t):       r'[iI][fF]';       t.type='IF';       return t
def t_IN(t):       r'[iI][nN]';       t.type='IN';       return t
def t_LABEL(t):    r'[lL][aA][bB][eE][lL]';    t.type='LABEL';    return t
def t_MOD(t):      r'[mM][oO][dD]';      t.type='MOD';      return t
def t_NIL(t):      r'[nN][iI][lL]';      t.type='NIL';      return t
def t_NOT(t):      r'[nN][oO][tT]';      t.type='NOT';      return t
def t_OF(t):       r'[oO][fF]';       t.type='OF';       return t
def t_OR(t):       r'[oO][rR]';       t.type='OR';       return t
def t_PACKED(t):   r'[pP][aA][cC][kK][eE][dD]';   t.type='PACKED';   return t
def t_PROCEDURE(t):r'[pP][rR][oO][cC][eE][dD][uU][rR][eE]'; t.type='PROCEDURE';return t
def t_PROGRAM(t):  r'[pP][rR][oO][gG][rR][aA][mM]';  t.type='PROGRAM';  return t
def t_RECORD(t):   r'[rR][eE][cC][oO][rR][dD]';   t.type='RECORD';   return t
def t_REPEAT(t):   r'[rR][eE][pP][eE][aA][tT]';   t.type='REPEAT';   return t
def t_SET(t):      r'[sS][eE][tT]';      t.type='SET';      return t
def t_THEN(t):     r'[tT][hH][eE][nN]';     t.type='THEN';     return t
def t_TO(t):       r'[tT][oO]';       t.type='TO';       return t
def t_TYPE(t):     r'[tT][yY][pP][eE]';     t.type='TYPE';     return t
def t_UNTIL(t):    r'[uU][nN][tT][iI][lL]';    t.type='UNTIL';    return t
def t_VAR(t):      r'[vV][aA][rR]';      t.type='VAR';      return t
def t_WHILE(t):    r'[wW][hH][iI][lL][eE]';    t.type='WHILE';    return t
def t_WITH(t):     r'[wW][iI][tT][hH]';     t.type='WITH';     return t

# ——— Funções built-in ———
def t_ABS(t):   r'[aA][bB][sS]';   t.type='FUNCTION_NAME'; return t
def t_SQR(t):   r'[sS][qQ][rR]';   t.type='FUNCTION_NAME'; return t
def t_SIN(t):   r'[sS][iI][nN]';   t.type='FUNCTION_NAME'; return t
def t_COS(t):   r'[cC][oO][sS]';   t.type='FUNCTION_NAME'; return t
def t_EXP(t):   r'[eE][xX][pP]';   t.type='FUNCTION_NAME'; return t
def t_LN(t):    r'[lL][nN]';      t.type='FUNCTION_NAME'; return t
def t_SQRT(t):  r'[sS][qQ][rR][tT]';  t.type='FUNCTION_NAME'; return t
def t_ODD(t):   r'[oO][dD][dD]';   t.type='FUNCTION_NAME'; return t
def t_PRED(t):  r'[pP][rR][eE][dD]';  t.type='FUNCTION_NAME'; return t
def t_SUCC(t):  r'[sS][uU][cC][cC]';  t.type='FUNCTION_NAME'; return t
def t_ORD(t):   r'[oO][rR][dD]';   t.type='FUNCTION_NAME'; return t
def t_CHR(t):   r'[cC][hH][rR]';   t.type='FUNCTION_NAME'; return t
def t_EOF(t):   r'[eE][oO][fF]';   t.type='FUNCTION_NAME'; return t
def t_EOLN(t):  r'[eE][oO][lL][nN]';  t.type='FUNCTION_NAME'; return t

# ——— Procedures built-in ———
def t_READLN(t):  r'[rR][eE][aA][dD][lL][nN]'; t.type='PROCEDURE_NAME'; return t
def t_WRITELN(t): r'[wW][rR][iI][tT][eE][lL][nN]'; t.type='PROCEDURE_NAME'; return t
def t_RESET(t):   r'[rR][eE][sS][eE][tT]';   t.type='PROCEDURE_NAME'; return t
def t_REWRITE(t): r'[rR][eE][wW][rR][iI][tT][eE]'; t.type='PROCEDURE_NAME'; return t
def t_CLOSE(t):   r'[cC][lL][oO][sS][eE]';   t.type='PROCEDURE_NAME'; return t
def t_GET(t):     r'[gG][eE][tT]';     t.type='PROCEDURE_NAME'; return t
def t_PUT(t):     r'[pP][uU][tT]';     t.type='PROCEDURE_NAME'; return t
def t_PACK(t):    r'[pP][aA][cC][kK]';    t.type='PROCEDURE_NAME'; return t
def t_UNPACK(t):  r'[uU][nN][pP][aA][cC][kK]'; t.type='PROCEDURE_NAME'; return t
def t_PAGE(t):    r'[pP][aA][gG][eE]';    t.type='PROCEDURE_NAME'; return t


def t_CHAR_LITERAL(t):
    r"'.'"
    t.value = t.value[1]                                # Remove as aspas simples

    return t

def t_STRING_LITERAL(t):
    r"'[^'\n]*'"
    
    return t

def t_BOOLEAN_LITERAL(t):
    r'true|false'

    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z][a-zA-Z0-9]*'            # ISO 7185 não permite underscores nas variáveis, e tem de começar por letra
    return t

t_ignore_COMMENT1 = r'\{(.|\n)*?\}'                 # { comment }
t_ignore_COMMENT2 = r'\(\*(.|\n)*?\*\)'             # (* comment *)
t_ignore_COMMENT3 = r'\/\/.*$'                      # / /comment (mas sem o espaço entre os /)
t_ignore = " \t\n\r"

def t_error(t):
    print('Caráter ilegal: ', t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()