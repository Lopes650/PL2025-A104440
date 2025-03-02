# Analisador Léxico para SPARQL

## 1. Objetivo

O objetivo do programa é realizar a análise léxica de consultas SPARQL, convertendo a entrada de texto em uma sequência de tokens. O analisador utiliza expressões regulares para identificar padrões sintáticos e classificar os tokens conforme suas categorias.

## 2. Argumentos de Entrada

- **Consulta SPARQL**: Um arquivo de texto contendo a consulta SPARQL a ser analisada.

## 3. Funcionamento

O analisador realiza a tokenização da entrada com as seguintes transformações:

1. **Identificação de Palavras-chave:**
   - Detecta palavras-chave como `SELECT`, `WHERE` e `LIMIT`, categorizando-as como tokens correspondentes.
   - Utiliza a expressão regular `\bSELECT\b|\bWHERE\b|\bLIMIT\b`.

2. **Identificação de Variáveis:**
   - Variáveis SPARQL iniciadas por `?`, como `?nome` e `?desc`, são reconhecidas.
   - Utiliza a expressão `\?[a-zA-Z_][a-zA-Z0-9_]*`.

3. **Identificação de Prefixos:**
   - Reconhece prefixos como `dbo:` e `foaf:`.
   - Utiliza a expressão `[a-zA-Z_][a-zA-Z0-9_-]*:`.

4. **Identificação de Identificadores:**
   - Identificadores gerais são tokens que representam entidades ou propriedades na consulta.
   - Utiliza a expressão `[a-zA-Z_][a-zA-Z0-9_-]*`.

5. **Identificação de Literais:**
   - Literais com idioma são detectados no formato `"Texto"@en`.
   - Literais sem idioma são capturados como `"Texto"`.
   - Utiliza as expressões `"[^"]*"@[a-zA-Z]+` e `"[^"]*"`.

6. **Identificação de Símbolos Especiais:**
   - Pontuação e operadores são reconhecidos, como `{`, `}`, `.`.
   - Utiliza expressões como `\{`, `\}`, `\.`.

7. **Identificação de Comentários:**
   - Comentários iniciados por `#` são capturados e tratados como tokens de comentário.
   - Utiliza a expressão `#.*`.

8. **Ignoração de Espaços em Branco:**
   - Espaços e quebras de linha são ignorados.

## 4. Saída

O programa retorna uma lista de tokens no formato `LexToken(TIPO, 'valor', linha, posição)`, permitindo a interpretação estruturada da consulta SPARQL.

## 5. Exemplo de Uso

### **Entrada (SPARQL):**

```sparql
# DBPedia: obras de Chuck Berry
SELECT ?nome ?desc WHERE {
?s a dbo:MusicalArtist.
?s foaf:name "Chuck Berry"@en .
?w dbo:artist ?s.
?w foaf:name ?nome.
?w dbo:abstract ?desc
} LIMIT 1000
```

### **Saída (Tokens):**

```plaintext
LexToken(COMMENT, '# DBPedia: obras de Chuck Berry', 1, 0)
LexToken(SELECT, 'SELECT', 2, 1)
LexToken(VAR, '?nome', 2, 8)
LexToken(VAR, '?desc', 2, 14)
LexToken(WHERE, 'WHERE', 2, 20)
LexToken(LBRACE, '{', 2, 26)
LexToken(VAR, '?s', 3, 1)
LexToken(A, 'a', 3, 4)
LexToken(PREFIX, 'dbo:', 3, 6)
LexToken(IDENTIFIER, 'MusicalArtist', 3, 10)
LexToken(DOT, '.', 3, 23)
LexToken(VAR, '?s', 4, 1)
LexToken(PREFIX, 'foaf:', 4, 4)
LexToken(IDENTIFIER, 'name', 4, 9)
LexToken(LITERAL, '"Chuck Berry"@en', 4, 14)
LexToken(DOT, '.', 4, 31)
LexToken(VAR, '?w', 5, 1)
LexToken(PREFIX, 'dbo:', 5, 4)
LexToken(IDENTIFIER, 'artist', 5, 8)
LexToken(VAR, '?s', 5, 15)
LexToken(DOT, '.', 5, 17)
LexToken(VAR, '?w', 6, 1)
LexToken(PREFIX, 'foaf:', 6, 4)
LexToken(IDENTIFIER, 'name', 6, 9)
LexToken(VAR, '?nome', 6, 14)
LexToken(DOT, '.', 6, 19)
LexToken(VAR, '?w', 7, 1)
LexToken(PREFIX, 'dbo:', 7, 4)
LexToken(IDENTIFIER, 'abstract', 7, 8)
LexToken(VAR, '?desc', 7, 17)
LexToken(RBRACE, '}', 8, 1)
LexToken(LIMIT, 'LIMIT', 8, 3)
LexToken(NUMBER, '1000', 8, 9)
```


