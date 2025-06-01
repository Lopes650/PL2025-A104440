
import sys
import ast


class Emitter:
    def __init__(self):
        self.instructions = []            
        self.labelCount = 0      

    def addInstruction(self, instr):
        self.instructions.append(instr)  

    def getNewLabel(self):
        label = f"L{self.labelCount}"
        self.labelCount += 1
        return label

    def getInstructions(self):
        return "\n".join(self.instructions)
    
def variaveis(blockNode):
    varList = blockNode[1]
    vars = {}
    nextIdx = 0

    for decl in varList:
        if decl[0] == 'decl':
            # Declarações simples
            varNames = decl[1]
            for name in varNames:
                vars[name] = ('local', nextIdx)
                nextIdx += 1

        elif decl[0] == 'decl_array':
            # Declaração de array: decl = ('decl_array', ['nome'], ('array', lower, upper, tipo))
            varNames = decl[1]
            arrayInfo = decl[2]
            lower = arrayInfo[1]
            upper = arrayInfo[2]
            tamanho = upper - lower + 1

            for name in varNames:
                vars[name] = ('array', nextIdx, tamanho, lower, upper)
                nextIdx += 1

    return vars










def genFor(node, vars, emitter):
    """
    Gera código para ciclo for
    node = ('for', var_name, 'to', start_expr, end_expr, statements_list)
    """
    var_name = node[1]
    start_expr = node[3]
    end_expr = node[4]
    statements = node[5]
    
    # Labels para controlo do ciclo
    loop_start = emitter.getNewLabel()
    loop_end = emitter.getNewLabel()
    
    # Inicializar variável do ciclo com valor inicial
    genExpression(start_expr, vars, emitter)
    tipo_var, indice = vars[var_name][:2]
    emitter.addInstruction(f'STOREL {indice}')
    
    # Label do início do ciclo
    emitter.addInstruction(f'{loop_start}:')
    
    # Verificar condição: var <= end_expr
    genExpression(end_expr, vars, emitter)
    emitter.addInstruction(f'PUSHL {indice}')
    emitter.addInstruction('SUPEQ')  # var > end_expr ?
    emitter.addInstruction(f'JZ {loop_end}')  # se verdade, sair do ciclo
    
    # Executar statements do ciclo
    genSubBlock(statements, vars, emitter)
    
    # Incrementar variável do ciclo
    emitter.addInstruction(f'PUSHL {indice}')
    emitter.addInstruction('PUSHI 1')
    emitter.addInstruction('ADD')
    emitter.addInstruction(f'STOREL {indice}')
    
    # Saltar para início do ciclo
    emitter.addInstruction(f'JUMP {loop_start}')
    
    # Label do fim do ciclo
    emitter.addInstruction(f'{loop_end}:')








def genExpression(expr, vars, emitter):
    tipo = expr[0]

    if tipo == 'num':
        valor = expr[1]
        emitter.addInstruction(f'PUSHI {valor}')

    elif tipo == 'var':
        nome = expr[1]
        var_info = vars[nome]
        tipo_var = var_info[0]
        indice = var_info[1]
        if tipo_var == 'local':
            emitter.addInstruction(f'PUSHL {indice}')
        elif tipo_var == 'array':
            emitter.addInstruction(f'PUSHL {indice}')

    elif tipo in ['+', '-', '*', '/', 'mod', 'div']:
        op_esq = expr[1]
        op_dir = expr[2]
        genExpression(op_esq, vars, emitter)
        genExpression(op_dir, vars, emitter)

        # print(f"DEBUG genExpression: tipo = {tipo!r}")

        if tipo == '+':
            emitter.addInstruction('ADD')
        elif tipo == '-':
            emitter.addInstruction('SUB')
        elif tipo == '*':
            emitter.addInstruction('MUL')
        elif tipo == '/':
            emitter.addInstruction('FDIV')
        elif tipo == 'mod':
            emitter.addInstruction('MOD')
        elif tipo == 'div':
            emitter.addInstruction('DIV')

    elif tipo == 'index':
        nome_array = expr[1]
        expr_indice = expr[2]

        # Endereço base do array
        var_info = vars[nome_array]
        idx_arr = var_info[1]
        lower_bound = var_info[3] if len(var_info) > 4 else 0
        
        emitter.addInstruction(f'PUSHL {idx_arr}')
        
        # Gerar índice e ajustar para base 0
        genExpression(expr_indice, vars, emitter)
        if lower_bound != 0:
            emitter.addInstruction(f'PUSHI {lower_bound}')
            emitter.addInstruction('SUB')
        
        # Calcular endereço do elemento
        emitter.addInstruction('PADD')
        
        # Carregar valor
        emitter.addInstruction('LOAD 0')
    
    elif tipo == 'bool':
        # Empilha 1 para true, 0 para false
        valor_bool = expr[1]
        if valor_bool.lower() == 'true':
            emitter.addInstruction('PUSHI 1')
        else:
            emitter.addInstruction('PUSHI 0')








def genCondition(condition, vars, emitter):
    """
    Gera código para condições
    
    Atenção: As instruções de comparação tiram n (topo) e m (baixo) da stack
    e fazem m OP n. Então para a > b:
    - empilhar a (fica m)
    - empilhar b (fica n) 
    - SUP faz m > n = a > b
    """
    tipo = condition[0]
    
    if tipo in ['>', '<', '>=', '<=', '=', '!=']:
        expr1 = condition[1]  # lado esquerdo
        expr2 = condition[2]  # lado direito
        
        # Para expr1 OP expr2, empilhamos na ordem correta
        genExpression(expr1, vars, emitter)  # empilha primeiro (fica m)
        genExpression(expr2, vars, emitter)  # empilha segundo (fica n)
        
        # Agora aplicar operador: m OP n = expr1 OP expr2
        if tipo == '>':
            emitter.addInstruction('SUP')    # m > n
        elif tipo == '<':
            emitter.addInstruction('INF')    # m < n  
        elif tipo == '>=':
            emitter.addInstruction('SUPEQ')  # m >= n
        elif tipo == '<=':
            emitter.addInstruction('INFEQ')  # m <= n
        elif tipo == '=':
            emitter.addInstruction('EQUAL')  # m = n
        elif tipo == '!=':
            emitter.addInstruction('EQUAL')  
            emitter.addInstruction('NOT')    # (m = n)
    
    elif tipo == 'and':
        expr1 = condition[1]
        expr2 = condition[2]
        
        genCondition(expr1, vars, emitter)
        genCondition(expr2, vars, emitter)
        emitter.addInstruction('AND')
    
    elif tipo == 'or':
        expr1 = condition[1]
        expr2 = condition[2]
        
        genCondition(expr1, vars, emitter)
        genCondition(expr2, vars, emitter)
        emitter.addInstruction('OR')
    
    elif tipo == 'not':
        expr = condition[1]
        genCondition(expr, vars, emitter)
        emitter.addInstruction('NOT')
    
    else:
        # Se não é uma condição, trata como expressão normal
        genExpression(condition, vars, emitter)












def genIf(node, vars, emitter):
    """
    Gera código para estrutura condicional if
    node = ('if', condition, then_stmt, else_stmt) ou ('if', condition, then_stmt)
    """
    condition = node[1]
    then_stmt = node[2]
    if len(node) > 3:
        else_stmt = node[3] 
    else:
        else_stmt = None
    
    # Labels para controlo
    else_label = emitter.getNewLabel()
    end_label = emitter.getNewLabel() if else_stmt else else_label
    
    # Gerar condição (deixa 1 na stack se verdadeira, 0 se falsa)
    genCondition(condition, vars, emitter)
    
    # JZ: se o valor no topo for 0 (falso), salta para else_label
    emitter.addInstruction(f'JZ {else_label}')
    
    # Executar then
    genStatement(then_stmt, vars, emitter)
    
    # Se há else, saltar para fim (evitar executar else)
    if else_stmt:
        emitter.addInstruction(f'JUMP {end_label}')
    
    # Label else
    emitter.addInstruction(f'{else_label}:')
    
    # Executar else se existir
    if else_stmt:
        genStatement(else_stmt, vars, emitter)
        emitter.addInstruction(f'{end_label}:')








def genWhile(node, vars, emitter):
    """
    node = ('while', condition, statements_list)
    """
    condition = node[1]
    statements = node[2]

    # Criar labels para início e fim do ciclo
    loop_start = emitter.getNewLabel()
    loop_end   = emitter.getNewLabel()

    # Label de início do ciclo
    emitter.addInstruction(f'{loop_start}:')

    # Gerar a condição (vai empilhar 1 ou 0)
    genCondition(condition, vars, emitter)

    # Se condição == 0, saltar para fim
    emitter.addInstruction(f'JZ {loop_end}')

    # Corpo do while
    genSubBlock(statements, vars, emitter)

    # Voltar para início do ciclo
    emitter.addInstruction(f'JUMP {loop_start}')

    # Label de fim
    emitter.addInstruction(f'{loop_end}:')











def genProcCall(node, vars, emitter):
    nome_proc = node[1]
    argumentos = node[2]

    nome_proc = nome_proc.lower()

    if nome_proc == 'write' or nome_proc == 'writeln':
        for arg in argumentos:
            if arg [0] == 'string':
                valor_str = arg[1]
                if valor_str.startswith("'") and valor_str.endswith("'"):
                    valor_str = valor_str[1:-1]  # Remove aspas simples
                emitter.addInstruction(f'PUSHS "{valor_str}"')
                emitter.addInstruction("WRITES")
            else:
                genExpression(arg, vars, emitter)
                emitter.addInstruction("WRITEI")
        emitter.addInstruction("WRITELN")

    elif nome_proc == 'read' or nome_proc == 'readln':
        dest = argumentos[0]

        emitter.addInstruction("READ")
        emitter.addInstruction("ATOI")

        if dest[0] == 'var':
            nome_var = dest[1]
            _, indice = vars[nome_var]
            emitter.addInstruction(f"STOREL {indice}")

        elif dest[0] == 'index':
            nome_array = dest[1]
            expr_indice = dest[2]
            
            # Calcular o endereço onde vamos guardar
            var_info = vars[nome_array]
            idx_arr = var_info[1]
            lower_bound = var_info[3] if len(var_info) > 4 else 0
            
            emitter.addInstruction(f"PUSHL {idx_arr}")
            
            genExpression(expr_indice, vars, emitter)

            if lower_bound != 0:
                emitter.addInstruction(f'PUSHI {lower_bound}')
                emitter.addInstruction('SUB')
            
            emitter.addInstruction("PADD")
            
            # Trocar ordem: [valor, endereco] 
            emitter.addInstruction("SWAP")
            emitter.addInstruction("STORE 0")












def genAssign(node, vars, emitter):
    nome_var = node[1]
    expressao = node[2]

    # Gerar o valor da expressão
    genExpression(expressao, vars, emitter)

    # Verificar se é array (índice) ou variável simples
    if isinstance(nome_var, tuple) and nome_var[0] == 'index':
        # É um assignment para array: a[i] := expr
        nome_array = nome_var[1]
        expr_indice = nome_var[2]
        
        # Calcular endereço
        var_info = vars[nome_array]
        idx_arr = var_info[1]
        lower_bound = var_info[3]
        
        emitter.addInstruction(f"PUSHL {idx_arr}")
        
        genExpression(expr_indice, vars, emitter)# calcular valor do indice

        if lower_bound != 0:
            emitter.addInstruction(f'PUSHI {lower_bound}')
            emitter.addInstruction('SUB')
        
        emitter.addInstruction("PADD")
        
        # Trocar ordem e guardar
        emitter.addInstruction("SWAP")
        emitter.addInstruction("STORE 0")
    else:
        # É variável simples
        tipo, indice = vars[nome_var][:2]
        emitter.addInstruction(f'STOREL {indice}')














def genSubBlock(subBlockNode, vars, emitter):
    # print(f"DEBUG genSubBlock: subBlockNode = {subBlockNode}")
    # print(f"DEBUG genSubBlock: type = {type(subBlockNode)}")
    
    if isinstance(subBlockNode, list):
        # subBlockNode é uma lista de statements
        for statementNode in subBlockNode:
            # print(f"DEBUG: Processando statement: {statementNode}")
            genStatement(statementNode, vars, emitter)
    elif isinstance(subBlockNode, tuple):
        # Se for um tuple, é um único statement
        # print(f"DEBUG: subBlockNode é tuple, processando como único")
        genStatement(subBlockNode, vars, emitter)
    else:
        print(f"DEBUG: Tipo inesperado para subBlockNode: {type(subBlockNode)}")
        # print(f"DEBUG: Conteúdo: {subBlockNode}")

















def genCase(node, vars, emitter):
    """
    Gera código para a instrução case:
    node = ('case', expr_chave, [(const1, stmt1), (const2, stmt2), ...])
    """
    expr_chave = node[1]
    case_list = node[2]

    # 1. Obter (ou criar) índice temporário para guardar o valor da chave
    if '__case_temp' not in vars:
        temp_idx = len(vars)
        vars['__case_temp'] = ('local', temp_idx)
    else:
        temp_idx = vars['__case_temp'][1]

    # 2. Avaliar a expressão chave e guardar em temp
    genExpression(expr_chave, vars, emitter)
    emitter.addInstruction(f'STOREL {temp_idx}')

    # 3. Label de fim do case (para saltar após executar um ramo)
    end_case = emitter.getNewLabel()

    # 4. Para cada ramo, criar um label e gerar o teste
    #    Se não houver correspondência, saltar para o próximo rótulo de teste.
    for i, (const_i, stmt_i) in enumerate(case_list):
        # Label para este ramo
        case_label = emitter.getNewLabel()

        # Se for o último ramo, o próximo teste salta para end_case
        if i == len(case_list) - 1:
            next_test = end_case
        else:
            next_test = emitter.getNewLabel()

        # 4.1. Testar: carregar temp, empilhar constante e comparar
        emitter.addInstruction(f'PUSHL {temp_idx}')
        emitter.addInstruction(f'PUSHI {const_i}')
        emitter.addInstruction('EQUAL')
        # Se for 0 (falso), saltar para próximo teste
        emitter.addInstruction(f'JZ {next_test}')
        # Senão (isto é, igual), saltar para o bloco deste ramo
        emitter.addInstruction(f'JUMP {case_label}')

        # 4.2. Rótulo de início do bloco deste ramo
        emitter.addInstruction(f'{case_label}:')
        genStatement(stmt_i, vars, emitter)
        # Após executar, saltar para o fim do case
        emitter.addInstruction(f'JUMP {end_case}')

        # 4.3. Colocar rótulo para próximo teste (ou end_case se for o último)
        emitter.addInstruction(f'{next_test}:')

    # 5. Rótulo de fim do case
    emitter.addInstruction(f'{end_case}:')
















def genStatement(node, vars, emitter):
    tipo = node[0]

    if tipo == 'assign':
        genAssign(node, vars, emitter)
    elif tipo == 'for':
        genFor(node, vars, emitter)
    elif tipo == 'proc_call':
        genProcCall(node, vars, emitter)
    elif tipo == 'if':  # Adicionar esta linha
        genIf(node, vars, emitter)
    elif tipo == 'while':
        genWhile(node, vars, emitter)
    elif tipo == 'case':
        genCase(node, vars, emitter)
    elif tipo == 'empty':
        pass
    else:
        print(f"Statement não implementado: {tipo}")










def genBlock(blockNode, vars, emitter):
    statementList = blockNode[2]
    genSubBlock(statementList, vars, emitter)











def geradorPrograma(astRoot, vars, emitter):
    # 1. Emitir START
    emitter.addInstruction("START")

    # 2. Alocar arrays antes de executar o bloco
    blockNode = astRoot[2]
    decls = blockNode[1]

    for decl in decls:
        if decl[0] == 'decl_array':
            varNames = decl[1]

            for name in varNames:
                # Encontrar índice e alocar
                var_info = vars[name]
                emitter.addInstruction(f'ALLOC {var_info[2]}')
                emitter.addInstruction(f'STOREL {var_info[1]}')

    # 3. Gerar o resto do bloco
    genBlock(blockNode, vars, emitter)
    emitter.addInstruction("STOP")








def main():
    
    entrada = sys.stdin.read()

    try:
        astRoot = ast.literal_eval(entrada)
    except Exception as e:
        print(f"Erro ao fazer parse do AST: {e}")
        return

    emitter = Emitter()
    vars = variaveis(astRoot[2])
    
    print("Tabela de variáveis:", vars)
    
    geradorPrograma(astRoot, vars, emitter)

    print("\nCódigo gerado:")
    print(emitter.getInstructions())


if __name__ == "__main__":
    main()