import ply.lex as lex

# Lista de nomes de tokens

keywords = [
    'KEYWORD_ADDRSPACE', 'KEYWORD_ALIGN', 'KEYWORD_ALLOWZERO', 'KEYWORD_AND',
    'KEYWORD_ANYFRAME', 'KEYWORD_ANYTYPE', 'KEYWORD_ASM', 'KEYWORD_ASYNC',
    'KEYWORD_AWAIT', 'KEYWORD_BREAK', 'KEYWORD_CALLCONV', 'KEYWORD_CATCH',
    'KEYWORD_COMPTIME', 'KEYWORD_CONST', 'KEYWORD_CONTINUE', 'KEYWORD_DEFER',
    'KEYWORD_ELSE', 'KEYWORD_ENUM', 'KEYWORD_ERRDEFER', 'KEYWORD_ERROR',
    'KEYWORD_EXPORT', 'KEYWORD_EXTERN', 'KEYWORD_FALSE', 'KEYWORD_FN',
    'KEYWORD_FOR', 'KEYWORD_IF', 'KEYWORD_INLINE', 'KEYWORD_LINKSECTION',
    'KEYWORD_NOALIAS', 'KEYWORD_NOINLINE', 'KEYWORD_NOSUSPEND', 'KEYWORD_NULL',
    'KEYWORD_OPAQUE', 'KEYWORD_OR', 'KEYWORD_ORELSE', 'KEYWORD_PACKED',
    'KEYWORD_PUB', 'KEYWORD_RESUME', 'KEYWORD_RETURN', 'KEYWORD_STRUCT',
    'KEYWORD_SUSPEND', 'KEYWORD_SWITCH', 'KEYWORD_TEST', 'KEYWORD_THREADLOCAL',
    'KEYWORD_TRUE', 'KEYWORD_TRY', 'KEYWORD_UNDEFINED', 'KEYWORD_UNION',
    'KEYWORD_UNREACHABLE', 'KEYWORD_USINGNAMESPACE', 'KEYWORD_VAR',
    'KEYWORD_VOLATILE', 'KEYWORD_WHILE',
]

# Tipos de dados do Zig
data_types = [
    'TYPE_INT', 'TYPE_BOOL', 'TYPE_VOID', 'TYPE_STRING', 'TYPE_CHAR',
]

numbers = [
    'NUMBER',
]

assigns = [
    'ASSIGN', 'PLUS_ASSIGN', 'MINUS_ASSIGN', 'TIMES_ASSIGN', 'DIVIDE_ASSIGN',
    'MODULUS_ASSIGN', 'SHIFT_LEFT_ASSIGN', 'SHIFT_RIGHT_ASSIGN',
    'BITWISE_AND_ASSIGN', 'BITWISE_OR_ASSIGN', 'BITWISE_XOR_ASSIGN',
    'PLUS_PERCENT_ASSIGN', 'MINUS_PERCENT_ASSIGN', 'TIMES_PERCENT_ASSIGN',
    'PLUS_PIPE_ASSIGN', 'MINUS_PIPE_ASSIGN', 'TIMES_PIPE_ASSIGN',
]

math_operators = [
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULUS',
    'PLUS_PERCENT', 'MINUS_PERCENT', 'TIMES_PERCENT',
    'PLUS_PLUS',
    'PLUS_PIPE', 'MINUS_PIPE', 'TIMES_PIPE',
]

logical_operators = [
    'NOT',
]

compare_operators = [
    'EQUALS_THEN', 'NOT_EQUALS', 'GREATER_THEN', 'LESS_THEN',
    'LESS_EQUALS', 'GREATER_EQUALS'
]

bitwise_operators = [
    'BITWISE_AND', 'BITWISE_OR', 'BITWISE_XOR', 'BITWISE_COMPLEMENT',
    'BITWISE_SHIFT_LEFT', 'BITWISE_SHIFT_RIGHT'
]

others = [
    'IDENTIFIER',
    'IDENTIFIER_ESCAPED',
    'LPAREN', 'RPAREN',
    'LBRACKET', 'RBRACKET',
    'LBRACE', 'RBRACE',
    'SEMICOLON',
    'STRING', 'C_STRING', 'CHARACTER',
    'COMMA', 'DOT',
    'QUESTION_MARK',
    'COLON', 'DOUBLE_COLON',
    'ARROW', 'SWITCH_ARROW',
    'RANGE', 'RANGE_INCLUSIVE',
    'OPTIONAL_UNWRAP', 'DEREF',
    'ELLIPSIS',
    'PIPE',
    'AMPERSAND',
    'AT',
    'HASH',
]

# Junta todos os tokens
tokens = (keywords + data_types + numbers + assigns + math_operators + 
          logical_operators + compare_operators + bitwise_operators + others)

# Palavras reservadas do Zig
reserved = {
    'addrspace': 'KEYWORD_ADDRSPACE',
    'align': 'KEYWORD_ALIGN',
    'allowzero': 'KEYWORD_ALLOWZERO',
    'and': 'KEYWORD_AND',
    'anyframe': 'KEYWORD_ANYFRAME',
    'anytype': 'KEYWORD_ANYTYPE',
    'asm': 'KEYWORD_ASM',
    'async': 'KEYWORD_ASYNC',
    'await': 'KEYWORD_AWAIT',
    'break': 'KEYWORD_BREAK',
    'callconv': 'KEYWORD_CALLCONV',
    'catch': 'KEYWORD_CATCH',
    'comptime': 'KEYWORD_COMPTIME',
    'const': 'KEYWORD_CONST',
    'continue': 'KEYWORD_CONTINUE',
    'defer': 'KEYWORD_DEFER',
    'else': 'KEYWORD_ELSE',
    'enum': 'KEYWORD_ENUM',
    'errdefer': 'KEYWORD_ERRDEFER',
    'error': 'KEYWORD_ERROR',
    'export': 'KEYWORD_EXPORT',
    'extern': 'KEYWORD_EXTERN',
    'false': 'KEYWORD_FALSE',
    'fn': 'KEYWORD_FN',
    'for': 'KEYWORD_FOR',
    'if': 'KEYWORD_IF',
    'inline': 'KEYWORD_INLINE',
    'linksection': 'KEYWORD_LINKSECTION',
    'noalias': 'KEYWORD_NOALIAS',
    'noinline': 'KEYWORD_NOINLINE',
    'nosuspend': 'KEYWORD_NOSUSPEND',
    'null': 'KEYWORD_NULL',
    'opaque': 'KEYWORD_OPAQUE',
    'or': 'KEYWORD_OR',
    'orelse': 'KEYWORD_ORELSE',
    'packed': 'KEYWORD_PACKED',
    'pub': 'KEYWORD_PUB',
    'resume': 'KEYWORD_RESUME',
    'return': 'KEYWORD_RETURN',
    'struct': 'KEYWORD_STRUCT',
    'suspend': 'KEYWORD_SUSPEND',
    'switch': 'KEYWORD_SWITCH',
    'test': 'KEYWORD_TEST',
    'threadlocal': 'KEYWORD_THREADLOCAL',
    'true': 'KEYWORD_TRUE',
    'try': 'KEYWORD_TRY',
    'undefined': 'KEYWORD_UNDEFINED',
    'union': 'KEYWORD_UNION',
    'unreachable': 'KEYWORD_UNREACHABLE',
    'usingnamespace': 'KEYWORD_USINGNAMESPACE',
    'var': 'KEYWORD_VAR',
    'volatile': 'KEYWORD_VOLATILE',
    'while': 'KEYWORD_WHILE',

    # Tipos primitivos (sem duplicação)
    'int': 'TYPE_INT',
    'bool': 'TYPE_BOOL',
    'void': 'TYPE_VOID',
    'string': 'TYPE_STRING',
    'char': 'TYPE_CHAR',
}

# Comentários (ignorados)
def t_IDENTIFIER_ESCAPED(t):
    r'@"([^"\\]|\\.)+"'
    t.value = t.value[2:-1]
    return t

def t_COMMENT_BLOCK(t):
    r'/\*[\s\S]*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass

def t_COMMENT(t):
    r'//.*'
    pass

# Símbolos especiais (ordem importa para tokens compostos)
t_ELLIPSIS = r'\.\.\.'
t_DOUBLE_COLON = r'::'
t_SWITCH_ARROW = r'=>'
t_ARROW = r'->'

t_RANGE_INCLUSIVE = r'\.\.='
t_RANGE = r'\.\.'
t_OPTIONAL_UNWRAP = r'\.\?'
t_DEREF = r'\.\*'

t_SEMICOLON = r';'
t_COLON = r':'
t_DOT = r'\.'
t_QUESTION_MARK = r'\?'
t_COMMA = r','
t_PIPE = r'\|'
t_AMPERSAND = r'&'
t_AT = r'@'
t_HASH = r'\#'

# Operadores de atribuição (ordem importa - mais longos primeiro)
t_PLUS_PERCENT_ASSIGN = r'\+%='
t_MINUS_PERCENT_ASSIGN = r'-%='
t_TIMES_PERCENT_ASSIGN = r'\*%='
t_PLUS_PIPE_ASSIGN = r'\+\|='
t_MINUS_PIPE_ASSIGN = r'-\|='
t_TIMES_PIPE_ASSIGN = r'\*\|='
t_SHIFT_LEFT_ASSIGN = r'<<='
t_SHIFT_RIGHT_ASSIGN = r'>>='
t_PLUS_ASSIGN = r'\+='
t_MINUS_ASSIGN = r'-='
t_TIMES_ASSIGN = r'\*='
t_DIVIDE_ASSIGN = r'/='
t_MODULUS_ASSIGN = r'%='
t_BITWISE_AND_ASSIGN = r'&='
t_BITWISE_OR_ASSIGN = r'\|='
t_BITWISE_XOR_ASSIGN = r'\^='

# Operadores wrapping do Zig (ordem importa)
t_PLUS_PERCENT = r'\+%'
t_MINUS_PERCENT = r'-%'
t_TIMES_PERCENT = r'\*%'

# Operadores saturating
t_PLUS_PIPE = r'\+\|'
t_MINUS_PIPE = r'-\|'
t_TIMES_PIPE = r'\*\|'

# Operadores aritméticos
t_PLUS_PLUS = r'\+\+'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULUS = r'%'

# Operadores de comparação
t_EQUALS_THEN = r'=='
t_NOT_EQUALS = r'!='
t_GREATER_EQUALS = r'>='
t_LESS_EQUALS = r'<='
t_GREATER_THEN = r'>'
t_LESS_THEN = r'<'

t_ASSIGN = r'='

# Operadores lógicos
t_NOT = r'!'

# Operadores bitwise
t_BITWISE_SHIFT_LEFT = r'<<'
t_BITWISE_SHIFT_RIGHT = r'>>'
t_BITWISE_AND = r'&'
t_BITWISE_OR = r'\|'
t_BITWISE_XOR = r'\^'
t_BITWISE_COMPLEMENT = r'~'

# Delimitadores
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

# Strings
def t_C_STRING(t):
    r'c"([^"\\]|\\.)*"'
    t.value = t.value[2:-1]
    return t

def t_STRING(t):
    r'"([^"\\]|\\.)*"'
    t.value = t.value[1:-1]
    t.value = t.value.replace('\\n', '\n')
    t.value = t.value.replace('\\t', '\t')
    t.value = t.value.replace('\\r', '\r')
    t.value = t.value.replace('\\\\', '\\')
    t.value = t.value.replace('\\"', '"')
    t.value = t.value.replace('\\0', '\0')
    return t

# Caracteres
def t_CHARACTER(t):
    r"'([^'\\]|\\.)'"
    t.value = t.value[1:-1]
    if len(t.value) == 2 and t.value[0] == '\\':
        escapes = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\', "'": "'", '0': '\0'}
        t.value = escapes.get(t.value[1], t.value[1])
    return t

# Números
def t_NUMBER(t):
    r'0[xX][0-9A-Fa-f_]+|0[bB][01_]+|0[oO][0-7_]+|[0-9][0-9_]*(\.[0-9][0-9_]*)?([eE][+-]?[0-9][0-9_]*)?'
    raw = t.value.replace('_', '')
    if raw.startswith(('0x', '0X')):
        t.value = int(raw, 16)
    elif raw.startswith(('0b', '0B')):
        t.value = int(raw, 2)
    elif raw.startswith(('0o', '0O')):
        t.value = int(raw, 8)
    elif '.' in raw or 'e' in raw or 'E' in raw:
        t.value = float(raw)
    else:
        t.value = int(raw)
    return t

# Identificadores e palavras reservadas
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

# Ignorar espaços e tabs
t_ignore = ' \t'

# Contar linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Tratamento de erros
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

# Construir o lexer
lexer = lex.lex()

# Código de teste
f = open("input1.zig", "r")
code = f.read()

if __name__ == "__main__":
    print("\n" + "=" * 100)
    print(" " * 30 + "ANALISADOR LEXICO - LINGUAGEM ZIG")
    print("=" * 100)
    
    print("\nCodigo fonte:")
    print("-" * 100)
    print(code)
    print("-" * 100)
    
    print("\nTokens encontrados:")
    print("-" * 100)
    print(f"{'TIPO':<40} {'VALOR':<40} {'LINHA':<10}")
    print("-" * 100)
    
    lexer.input(code)
    
    # Realizando analise lexica
    token_count = 0
    for tok in lexer:
        token_count += 1
        valor = str(tok.value)
        
        # Formata melhor os valores
        if isinstance(tok.value, str):
            if len(valor) > 37:
                valor = valor[:34] + "..."
            valor = f'"{valor}"'
        else:
            valor = str(valor)
        
        print(f'{tok.type:<40} {valor:<40} {tok.lineno:<10}')
    
    print("-" * 100)
    print(f"Analise lexica concluida! Total de tokens: {token_count}")
    print("=" * 100 + "\n")