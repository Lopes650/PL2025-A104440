import sys
import ply.yacc as yacc
from pascal_lex import tokens

# Definir precedência de operadores
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('nonassoc', 'IFX'),
    ('right', 'ELSE'),
    ('nonassoc', 'EQUALS', 'LESSTHAN', 'GREATERTHAN', 'LESSEQUALS', 'GREATEQUALS', 'LESSGREAT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'DIV', 'MOD'),
    ('nonassoc', 'THEN'),
)

def p_program(p):
    '''program : PROGRAM IDENTIFIER SEMICOLON block PERIOD'''
    p[0] = ('program', p[2], p[4])

def p_block(p):
    '''block : declarations sub_block'''
    p[0] = ('block', p[1], p[2])

def p_declarations_var(p):
    '''declarations : VAR var_list'''
    p[0] = p[2]

def p_declarations_empty(p):
    '''declarations :'''
    p[0] = []

def p_var_list_multi(p):
    '''var_list : var_list decl SEMICOLON'''
    p[0] = p[1] + [p[2]]

def p_var_list_single(p):
    '''var_list : decl SEMICOLON'''
    p[0] = [p[1]]

def p_decl_type(p):
    '''decl : vars COLON type'''
    p[0] = ('decl', p[1], p[3])

def p_decl_array(p):
    '''decl : vars COLON array'''
    p[0] = ('decl_array', p[1], p[3])

def p_vars_multi(p):
    '''vars : vars COMMA IDENTIFIER'''
    p[0] = p[1] + [p[3]]

def p_vars_single(p):
    '''vars : IDENTIFIER'''
    p[0] = [p[1]]

def p_type_simple(p):
    '''type : INTEGER
            | BOOLEAN
            | REAL
            | STRING
            | CHAR'''
    p[0] = p[1]

def p_array(p):
    '''array : ARRAY LBRACKET NUMBER DOUBLEPERIOD NUMBER RBRACKET OF type'''
    p[0] = ('array', p[3], p[5], p[8])




def p_sub_block_non_empty(p):
    'sub_block : BEGIN statement_list END'
    p[0] = p[2]

def p_sub_block_empty(p):
    'sub_block : BEGIN END'
    p[0] = []

def p_statement_list_multi(p):
    '''statement_list : statement_list SEMICOLON statement'''
    p[0] = p[1] + [p[3]]

def p_statement_list_single(p):
    '''statement_list : statement '''
    p[0] = [p[1]]

#def p_statement_list_single_semi(p):
#    '''statement_list : statement SEMICOLON'''
#    p[0] = [p[1]]


#def p_statement_list_last(p):
#    '''statement_list : statement'''
#    p[0] = [p[1]]

def p_statement(p):
    '''statement : atribution_statement
                 | if_statement
                 | while_statement
                 | for_statement
                 | case_statement
                 | procedure_call
                 | sub_block'''
    p[0] = p[1]

def p_statement_empty(p):
    'statement :'
    p[0] = ('empty',)

#def p_statement(p):
#    '''statement : atribution_statement
#                 | if_statement
#                 | while_statement
#                 | for_statement
#                 | case_statement
#                 | procedure_call
#                 | sub_block''' 
#    p[0] = p[1]

# def p_statement_empty(p):
#     'statement :'
#     p[0] = ('empty',)

def p_statement_atrib(p):
    '''atribution_statement : IDENTIFIER ATRIBUTION expression'''
    p[0] = ('assign', p[1], p[3])

def p_statement_if_complete(p):
    '''if_statement : IF expression THEN statement ELSE statement'''
    p[0] = ('if', p[2], p[4], p[6])

def p_statement_if_incomplete(p):
    '''if_statement : IF expression THEN statement %prec IFX'''
    p[0] = ('if', p[2], p[4],)

# def p_else_clause(p):
#     '''else_clause : ELSE statement
#                    |'''
#     p[0] = p[2] if len(p) == 3 else None

def p_statement_while(p):
    '''while_statement : WHILE expression DO statement'''
    p[0] = ('while', p[2], p[4])

def p_statement_for(p):
    '''for_statement : FOR IDENTIFIER ATRIBUTION expression TO expression DO statement
                     | FOR IDENTIFIER ATRIBUTION expression DOWNTO expression DO statement'''
    direction = 'downto' if p[5].lower() == 'downto' else 'to'
    p[0] = ('for', p[2], direction, p[4], p[6], p[8])

def p_statement_case(p):
    '''case_statement : CASE expression OF case_list END'''
    p[0] = ('case', p[2], p[4])

def p_case_list(p):
    '''case_list : case_list SEMICOLON case_item'''
    p[0] = p[1] + [p[3]]

def p_case_list_single(p):
    '''case_list : case_item'''
    p[0] = [p[1]]

def p_case_item(p):
    '''case_item : constant COLON statement'''
    p[0] = (p[1], p[3])

def p_procedure_call(p):
    '''procedure_call : PROCEDURE_NAME LPAREN expr_list RPAREN
                      | IDENTIFIER LPAREN expr_list RPAREN'''
    p[0] = ('proc_call', p[1], p[3])

def p_function_call(p):
    '''function_call : FUNCTION_NAME LPAREN expr_list RPAREN
                     | IDENTIFIER LPAREN expr_list RPAREN'''
    p[0] = ('func_call', p[1], p[3])

def p_expr_list_multi(p):
    '''expr_list : expr_list COMMA expression'''
    p[0] = p[1] + [p[3]]

def p_expr_list_single(p):
    '''expr_list : expression'''
    p[0] = [p[1]]

def p_expr_list_empty(p):
    '''expr_list :'''
    p[0] = []

# Expressões unificadas (aritméticas e booleanas)
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression DIV expression
                  | expression MOD expression
                  | expression EQUALS expression
                  | expression LESSTHAN expression
                  | expression GREATERTHAN expression
                  | expression LESSEQUALS expression
                  | expression GREATEQUALS expression
                  | expression LESSGREAT expression
                  | expression AND expression
                  | expression OR expression'''
    p[0] = (p[2], p[1], p[3])

def p_expression_not(p):
    '''expression : NOT expression'''
    p[0] = ('not', p[2])

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expression_factor(p):
    '''expression : factor'''
    p[0] = p[1]

def p_factor_number(p):
    '''factor : NUMBER'''
    p[0] = ('num', p[1])

def p_factor_boolean(p):
    '''factor : BOOLEAN_LITERAL'''
    p[0] = ('bool', p[1])

def p_factor_id(p):
    '''factor : IDENTIFIER'''
    p[0] = ('var', p[1])

def p_factor_index(p):
    'factor : IDENTIFIER LBRACKET expression RBRACKET'
    p[0] = ('index', p[1], p[3])

def p_factor_char(p):
    '''factor : CHAR_LITERAL'''
    p[0] = ('char', p[1])

def p_factor_string(p):
    '''factor : STRING_LITERAL'''
    p[0] = ('string', p[1])

def p_factor_func(p):
    '''factor : function_call'''
    p[0] = p[1]

def p_constant(p):
    '''constant : NUMBER
                | BOOLEAN_LITERAL
                | IDENTIFIER
                | CHAR_LITERAL
                | STRING_LITERAL'''
    p[0] = p[1]

def p_error(p):
    if p:
        print(f"Erro de sintaxe em {p.type} ('{p.value}')")
    else:
        print("Erro de sintaxe em EOF")

parser = yacc.yacc()

EXEMPLOS = {
    "1": '''
    program HelloWorld;
    begin
        writeln('Ola, Mundo!');
    end.''',

    "2": '''
    program Maior3;
    var
        num1, num2, num3, maior: Integer;

    begin
        { Ler 3 números }
        Write('Introduza o primeiro número: ');
        ReadLn(num1);

        Write('Introduza o segundo número: ');
        ReadLn(num2);

        Write('Introduza o terceiro número: ');
        ReadLn(num3);

        { Calcular o maior }
        if num1 > num2 then
            if num1 > num3 then maior := num1
            else maior := num3
        else
            if num2 > num3 then maior := num2
            else maior := num3;

        { Escrever o resultado }
        WriteLn('O maior é: ', maior)
    end.''',

    "3": '''
    program Fatorial;
    var
        n, i, fat: integer;
    begin
        writeln('Introduza um número inteiro positivo:');
        readln(n);
        fat := 1;
        for i := 1 to n do
            fat := fat * i;
        writeln('Fatorial de ', n, ': ', fat);
    end.''',

    "4": '''
    program NumeroPrimo;
    var
        num, i: integer;
        primo: boolean;
    begin
        writeln('Introduza um número inteiro positivo:');
        readln(num);
        primo := true;
        i := 2;
        while (i <= (num div 2)) and primo do
            begin
                if (num mod i) = 0 then
                    primo := false;
                i := i + 1;
            end;
        if primo then
            writeln(num, ' é um número primo')
        else
            writeln(num, ' não é um número primo')
    end.''',

    "5": '''
    program SomaArray;
    var
        numeros: array[1..5] of integer;
        i, soma: integer;
    begin
        soma := 0;
        writeln('Introduza 5 números inteiros:');
        for i := 1 to 5 do
        begin
            readln(numeros[i]);
            soma := soma + numeros[i];
        end;
        
        writeln('A soma dos números é: ', soma);
    end.''',

    "6": '''
    program BinarioParaInteiro;
    var
        bin: string;
        i, valor, potencia: integer;

    begin
        writeln('Introduza uma string binária:');
        readln(bin);

        valor := 0;
        potencia := 1;
        for i := length(bin) downto 1 do
        begin
            if bin[i] = '1' then
                valor := valor + potencia;
            potencia := potencia * 2;
        end;

        writeln('O valor inteiro correspondente é: ', valor);
    end.'''
}

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in EXEMPLOS:
        sys.stderr.write("Número entre <1..6>\n")
        sys.exit(1)

    key = sys.argv[1]
    texto = EXEMPLOS[key]

    ast = parser.parse(texto)
    # Imprime a AST pura no stdout
    print(ast)


if __name__ == "__main__":
    main()


