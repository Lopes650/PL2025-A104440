# Analisador Sintático LL(1)

## 1. Objetivo

O objetivo deste programa é realizar a análise sintática de expressões matemáticas simples usando a técnica de parsing **LL(1)**. A entrada consiste em uma string representando uma expressão matemática, e o analisador converte essa entrada em um valor numérico após a análise e avaliação da expressão.

## 2. Argumentos de Entrada

- **Expressão matemática**: Uma string contendo uma expressão matemática composta por números inteiros, operadores (`+`, `-`, `*`, `/`), parênteses e comentários.
  
## 3. Funcionamento

O analisador é baseado em uma gramática simples para expressões aritméticas. Ele utiliza uma abordagem recursiva de descida para processar a entrada. A gramática e as funções do parser seguem a estrutura de um parser LL(1), ou seja, cada decisão é tomada com base no próximo token.

### Passos do Analisador:

1. **Analisador Léxico**:
   - O código utiliza o PLY (Python Lex-Yacc) para gerar tokens a partir da entrada.
   - O analisador léxico reconhece os seguintes tokens: números, operadores (`+`, `-`, `*`, `/`), parênteses (`(`, `)`), e outros símbolos.

2. **Gramática de Expressões**:
   - O parser implementa a gramática aritmética básica para expressões de somas, subtrações, multiplicações e divisões. A ordem de precedência é corretamente tratada, permitindo que expressões com diferentes níveis de prioridade sejam corretamente avaliadas.

   A gramática usada é a seguinte:

   Expressao → Termo Expressao2 Expressao2 → + Termo Expressao2 | - Termo Expressao2 | ε Termo → Fator Termo2 Termo2 → * Fator Termo2 | / Fator Termo2 | ε Fator → NUM | ( Expressao )

3. **Tokens Reconhecidos**:
- `NUM`: Números inteiros.
- `SUM`: Operador de soma (`+`).
- `SUB`: Operador de subtração (`-`).
- `MUL`: Operador de multiplicação (`*`).
- `DIV`: Operador de divisão (`/`).
- `PA`: Parêntese de abertura (`(`).
- `PF`: Parêntese de fechamento (`)`).

4. **Mecanismo de Análise**:
- O mecanismo de parsing utiliza uma abordagem recursiva de descida com funções como `rec_Expressao`, `rec_Termo`, `rec_Expressao2`, `rec_Termo2`, e `rec_Fator`.
- O código identifica e processa cada token da entrada, validando a expressão matemática de acordo com a gramática definida.

5. **Erro de Sintaxe**:
- Caso seja encontrado um token inesperado ou uma expressão inválida, o programa lança um erro de sintaxe.

## 4. Saída

O programa retorna o resultado da expressão matemática após sua análise e avaliação. Caso a entrada contenha erros sintáticos, o programa exibirá uma mensagem de erro indicando o token inesperado e a posição da linha.

### Exemplo de Saída:

```plaintext
Resultado: 5
Resultado: 53
Resultado: 63
````

## 5. Exemplo de Uso:
#### Entrada (Chamada da função):

```python
rec_Parser("2+3")
rec_Parser("67-(2+3*4)")
rec_Parser("(9-2)*(13-4)")
```
```

#### Output:
```python
Resultado: 5
Resultado: 53
Resultado: 63
```