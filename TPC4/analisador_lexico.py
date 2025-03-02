import re

# Token definition with regex patterns
TOKEN_PATTERNS = [
    (r'\bSELECT\b', 'SELECT'),
    (r'\bWHERE\b', 'WHERE'),
    (r'\bLIMIT\b', 'LIMIT'),
    (r'\?[a-zA-Z_][a-zA-Z0-9_]*', 'VAR'),  # Variáveis (ex: ?nome, ?desc)
    (r'[a-zA-Z_][a-zA-Z0-9_-]*:', 'PREFIX'),  # Prefixos (ex: dbo:, foaf:)
    (r'\ba\b', 'A'),  # <- **Mover "a" antes de IDENTIFIER**
    (r'[a-zA-Z_][a-zA-Z0-9_-]*', 'IDENTIFIER'),  # Identificadores gerais
    (r'"[^"]*"@[a-zA-Z]+', 'LITERAL'),  # Literais com idioma
    (r'"[^"]*"', 'LITERAL'),  # Literais sem idioma
    (r'\.', 'DOT'),
    (r'\{', 'LBRACE'),
    (r'\}', 'RBRACE'),
    (r'\d+', 'NUMBER'),
    (r'#.*', 'COMMENT'),  # Comentários
    (r'\s+', None)  # Espaços em branco (ignorados)
]


class LexToken:
    """Class to represent a token in the required format."""
    def __init__(self, type_, value, line, pos):
        self.type = type_
        self.value = value
        self.line = line
        self.pos = pos

    def __repr__(self):
        return f"LexToken({self.type}, {repr(self.value)}, {self.line}, {self.pos})"

def lexer(query):
    tokens = []
    line = 1
    pos = 0

    while query:
        match_found = False
        for pattern, token_type in TOKEN_PATTERNS:
            regex = re.match(pattern, query, re.IGNORECASE)
            if regex:
                match_found = True
                value = regex.group()
                if token_type:  # Ignore whitespace and comments
                    tokens.append(LexToken(token_type, value, line, pos))
                query = query[len(value):]  # Remove recognized part
                pos += len(value)
                break

        if not match_found:
            raise SyntaxError(f"Token inválido: {query[0]} na linha {line}, posição {pos}")

        # Handle line counting
        if '\n' in query[:1]:
            line += 1
            pos = 0

    return tokens

# Test Query
query = """# DBPedia: obras de Chuck Berry
select ?nome ?desc where {
?s a dbo:MusicalArtist.
?s foaf:name "Chuck Berry"@en .
?w dbo:artist ?s.
?w foaf:name ?nome.
?w dbo:abstract ?desc
} LIMIT 1000"""

# Run Lexer
tokens = lexer(query)

# Print Tokens
for token in tokens:
    print(token)
