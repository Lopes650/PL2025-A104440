# Projeto de Processamento de Linguagens
## Construção de um Compilador para Pascal Standard

- André Barbosa Teixeira - a104002
- João Andrade Costa - a104258
- Rodrigo Guedes Lopes - a104440

## Introdução

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Neste projeto, o objetivo era desenvolver um compilador para a linguagem **Pascal Standard (ISO 7185)**. Este compilador deve ser capaz de analisar, interpretar, e traduzir código Pascal para um formato intermédio, e deste para código máquina da VM disponibilizada. O compilador deve ser capaz de lidar com declaração de variáveis, expressões aritméticas, e comandos de controlo de fluxo.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; O projeto será repartido por etapas, estas sendo:

1. Análise Léxica;
2. Análise Sintática;
3. Análise Semântica;
4. Geração de Código;
5. Testes.


## Análise Léxica

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Para começar a primeira etapa deste projeto, primeiro analisamos esta linguagem, para isto seguimos o documento [*iso7185*](https://www.cs.utexas.edu/~novak/iso7185.pdf) e os aspetos relevantes de [*freepascal.org*](https://www.freepascal.org/docs-html/ref/refli2.html). A primeira parte a destacar são os símbolos e os pares de símbolos reservados: 

- `\+ - * / = < > [ ] . , ( ) : ; ^`
- `<> <= >= := .. += -= *= /= (. .)`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Em seguida, anotamos também as palavras reservadas:
- `AND, ARRAY, BEGIN, CASE, CONST, DIV, DOWNTO, DO, ELSE, END, FILE, FOR, FUNCTION, GOTO, IF, IN, LABEL, MOD, NIL, NOT, OF, OR, PACKED, PROCEDURE, PROGRAM, RECORD, REPEAT, SET, THEN, TO, TYPE, UNTIL, VAR, WHILE, WITH`

Tipos de variáveis (embora não sejam palavras reservadas, são cruciais para o funcionamento do programa, e consideramos melhor implementar como se fossem):

- `INTEGER, BOOLEAN, REAL, CHAR, STRING`

E Funções e Procedimentos *built-in*:
- `ABS, SQR, SIN, COS, EXP, LN, SQRT, ODD, PRED, SUCC, ORD, CHR, EOF, EOLN`
- `READLN, WRITELN, RESET, REWRITE, CLOSE, GET, PUT, PACK, UNPACK, PAGE`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Após ter a lista definida, teríamos de implementar o *lexer* com *ply.lex* e usar estes símbolos e palavras como *tokens*, definidos pelas suas expressões regulares respetivas. Para além destes, foram adicionados os *tokens*:
- `IDENTIFIER` - para capturar nomes de variáveis que o utilizador define;
- `NUMBER`- para capturar os números introduzidos;
- `CHAR_LITERAL`- para capturar os caracteres únicos;
- `STRING_LITERAL` - para capturar *strings* inteiras;
- `BOOLEAN_LITERAL`- para capturar valores booleanos.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Para além disto, os *tokens* relativos a funções e procedimentos foram agrupados, definindo um *.type* relativo ao conjunto em que se enquadram: `FUNCTION_NAME` ou `PROCEDURE_NAME`. Na gramática é assim que vão ser chamados.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Por fim, tratamos dos valores a ignorar como o caso dos comentários e espaços em branco. Para os comentários, começando pelos comentários de uma linha, tudo o que seguir `//` (inclusivé) vai ser ignorado. Para os outros, qualquer conteúdo que estiver em ambas as fórmulas abaixo, irá ser ignorado:
- `{` *comentário* `}` ;
- `(*` *comentário* `*)` .

Tudo o que não se incluir nestes padrões irá ser considerado um **caráter ilegal**, levando a caso de erro. Com isto, a análise léxica está concluída.



## Análise Sintática

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Na análise sintática teriámos agora de construir um *parser* para validar a estrutura gramatical do código, para isso, a ferramenta *ply.yacc* foi utilizada. Com os *tokens* definidos anteriormente, teríamos de construir uma gramática *Bottom-Up*, esta foi guiada pelos exemplos de código presentes no enunciado e os documentos previamente referidos. A sua versão final é a que está transcrita abaixo.

```txt
program -> PROGRAM IDENTIFIER SEMICOLON block PERIOD

block -> declarations sub_block

declarations -> VAR var_list
    | ε

var_list -> var_list decl SEMICOLON
    | decl SEMICOLON

decl -> vars COLON type
    | vars COLON array
    | vars COLON string

vars -> vars COMMA IDENTIFIER
    | IDENTIFIER

type -> INTEGER
    | BOOLEAN
    | REAL
    | STRING
    | CHAR

array -> ARRAY LBRACKET NUMBER PERIOD PERIOD NUMBER RBRACKET OF type


sub_block -> BEGIN statement_list END

statement_list -> statement_list statement SEMICOLON
    | statement SEMICOLON

statement -> atribution_statement
    | if_statement
    | while_statement
    | for_statement
    | case_statement
    | procedure_call
    | sub_block
    | ε

atribution_statement -> IDENTIFIER ATRIBUTION expression

if_statement -> IF cond THEN statement ELSE statement
    | IF cond THEN statement

while_statement -> WHILE cond DO statement

for_statement -> FOR atribution_statement TO expression DO statement
    | FOR atribution_statement DOWNTO expression DO statement

case_statement -> CASE expression OF case_list END

case_list -> case_list SEMICOLON case_item
    | case_item

case_item -> constant COLON statement

procedure_call -> PROCEDURE_NAME LPAREN expr_list RPAREN
    | IDENTIFIER LPAREN expr_list RPAREN

function_call -> FUNCTION_NAME LPAREN expr_list RPAREN
    | IDENTIFIER LPAREN expr_list RPAREN

expr_list -> expr_list COMMA expression
    | expression
    | ε

expression -> expression PLUS expression
    | expression MINUS expression
    | expression TIMES expression
    | expression DIVIDE expression
    | expression DIV expression
    | expression EQUALS expression
    | expression LESSTHAN expression
    | expression GREATERTHAN expression
    | expression LESSEQUALS expression
    | expression GREATEQUALS expression
    | expression LESSGREAT expression
    | expression AND expression
    | expression OR expression
    | NOT expression
    | LPAREN expression RPAREN
    | factor

factor -> NUMBER
    | BOOLEAN_LITERAL
    | IDENTIFIER
    | IDENTIFIER LBRACKET expression RBRACKET
    | CHAR_LITERAL
    | STRING_LITERAL
    | function_call

constant -> NUMBER
    | BOOLEAN_LITERAL
    | IDENTIFIER
    | CHAR_LITERAL
    | STRING_LITERAL
```

>Nota: Esta gramática deteta chamadas de funções criadas pelo utilizador, mas não suporta a sua implementação.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Para esta gramática funcionar, regras de precedência tiveram de ser definidas, evitando conflitos. Com isto definido, as produções foram passadas para *yacc*, com uma final a capturar e assinalar erros de sintaxe. Se estes não existirem, o parser gera as tabelas LALR e é criada também uma **AST**. O código gerado vai usar esta como intermediária.


## Análise Semântica

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Infelizmente, devido a constrangimentos de tempo, não realizámos análise semântica do código; passámos a gerar o código máquina desde que a sintaxe do programa fornecido esteja correta.


## Geração de Código

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Este módulo converte a AST gerada pelo parser numa sequência de instruções para a VM, usando um **Emitter** para acumular comandos e gerar rótulos.

#### Emitter

* Armazena instruções numa lista e cria rótulos únicos (`getNewLabel`).
* Método `addInstruction(instr)` adiciona uma linha; `getInstructions()` retorna todo o código concatenado.

#### Tabela de Variáveis

A função `variaveis(blockNode)` percorre declarações simples e de arrays, atribuindo a cada nome:

* Escalares: `('local', índice)`
* Arrays: `('array', índice, tamanho, lower, upper)`
  Esses índices referenciam posições no frame ou na memória da VM.

#### Geração de Construtos

* **`genWhile`**: avalia a condição antes do laço, insere rótulo de início e, caso verdadeiro, gera o corpo e faz salto de retorno até a condição.
* **`genFor`**: inicializa a variável de ciclo, testa `var <= end`, gera corpo, incrementa `i` e repete até sair.
* **`genIf`**: avalia condição, insere rótulo de salto (`JZ`) para o bloco *else*, gera o bloco *then* e, se houver, o *else*.

#### Expressões e Condições

* **`genExpression(expr)`**: empilha literais (`PUSHI`), carrega variáveis (`PUSHL idx`), executa operações binárias (`ADD, SUB, MUL, DIV, MOD`) ou acesso a arrays via cálculo de endereço (`PADD, LOAD`).
* **`genCondition(cond)`**: testa operadores relacionais (`SUP, INF, SUPEQ, INFEQ, EQUAL, NOT`) e lógicos (`AND, OR, NOT`), chamando `genExpression` conforme necessário.

#### Chamadas de I/O e Atribuições

* **`genProcCall`**: trata `writeln`/`write` (imprime strings ou valores) e `readln` (lê da entrada, converte com `ATOI`, faz `STOREL` ou `STORE`).
* **`genAssign`**: para variáveis simples usa `STOREL idx`; para arrays, calcula endereço, troca a pilha e faz `STORE 0`.

#### Fluxo Principal

A função `geradorPrograma(astRoot, vars, emitter)`:

1. Emite `START`;
2. Para cada `decl_array`, faz `ALLOC tamanho` e `STOREL idx`;
3. Chama `genBlock` para processar todos os statements do bloco;
4. Emite `STOP`.

Este design modular permite estender facilmente a geração de código para novos construtos adicionando novas funções `genXxx`.



## Testes

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Na etapa final, para testar o nosso compilador, utilizamos os primeiros 6 exemplos fornecidos no enunciado, garantindo as funcionalidades básicas da linguagem.

Por exemplo, gerando a árvore do exemplo 1 com o *parser*, obtemos a seguinte AST:

```
('program', 'HelloWorld', ('block', [], [('proc_call', 'writeln', [('string', "'Ola, Mundo!'")]), ('empty',)]))
````

Se passarmos este resultado ao nosso gerador, obtemos o seguinte código máquina, testado como funcional na VM:

```
START
PUSHS "Ola, Mundo!"
WRITES
WRITELN
STOP
```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Porém, esta forma de gerar o código-máquina é lenta e trabalhosa. Para acelerar, o parser recebe como argumento um número de 1 a 6 indicativo dos exemplos dados. Como escreve o resultado para o *stdout*, o nosso gerador vai ler diretamente de lá a **AST** criada e gera o código máquina correspondente. Aqui em baixo está um exemplo de utilização, gerando o mesmo resultado que a antiga forma manual.

```
python pascal_yacc.py 1 | python AstToAssembly.py
```

>Nota: Em MACOS, *python3* é utilizado


## Considerações Finais

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Após a realização deste projeto, não conseguimos os 6 exemplos de objetivo, apenas os 5 primeiros, no futuro, dada a oportunidade, procuraríamos fazer algumas melhorias, nomeadamente:

- Suporte a mais operadores Pascal (vários foram capturados como *tokens* mas não utilizados na gramática);
- Análise semântica;
- Mais otimizações no código;
- *Suite* de testes mais alargada, cobrindo mais programas para além dos exemplos fornecidos.

Apesar destas limitações, construímos um compilador robusto para os casos fornecidos.