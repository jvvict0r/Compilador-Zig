import logging
import ply.yacc as yacc
from ExpressionLanguageLex import tokens, lexer
import SintaxeAbstrata as sa

arquivos_zig = []
isFine = True
QUIET_PLY = True

# Precedência de operadores
precedence = (
    ('nonassoc', 'IFX'),
    ('nonassoc', 'KEYWORD_ELSE'),
    ('left', 'EQUALS_THEN', 'NOT_EQUALS', 'LESS_THEN', 'LESS_EQUALS', 'GREATER_THEN', 'GREATER_EQUALS'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULUS'),
    ('right', 'NOT', 'UMINUS', 'UPLUS'),
)

# Programa

def p_program(p):
    'program : items'
    p[0] = sa.Program(p[1])


def p_items(p):
    '''items : items item
             | item'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_item(p):
    '''item : function
            | const_decl SEMICOLON
        | var_decl SEMICOLON'''
    p[0] = p[1]

# Declarações

def p_const_decl(p):
    'const_decl : KEYWORD_CONST IDENTIFIER type_annot_opt ASSIGN expression'
    p[0] = sa.ConstDecl(p[2], p[3], p[5])


def p_var_decl(p):
    'var_decl : KEYWORD_VAR IDENTIFIER type_annot_opt ASSIGN expression'
    p[0] = sa.VarDecl(p[2], p[3], p[5])


def p_type_annot_opt(p):
    '''type_annot_opt : COLON type_spec
                      | empty'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None


def p_type_spec(p):
    '''type_spec : data_type
                 | IDENTIFIER'''
    p[0] = p[1]


def p_data_type(p):
    '''data_type : TYPE_INT
                 | TYPE_BOOL
                 | TYPE_VOID
                 | TYPE_STRING
                 | TYPE_CHAR'''
    p[0] = p[1]

# Funções

def p_function(p):
    'function : visibility_opt KEYWORD_FN IDENTIFIER LPAREN params_opt RPAREN return_type_opt block'
    p[0] = sa.Function(p[3], p[5] or [], p[7], p[8], p[1])


def p_visibility_opt(p):
    '''visibility_opt : KEYWORD_PUB
                      | empty'''
    p[0] = p[1]


def p_return_type_opt(p):
    '''return_type_opt : type_spec
                       | empty'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = None


def p_params_opt(p):
    '''params_opt : params
                  | empty'''
    p[0] = p[1]


def p_params(p):
    '''params : params COMMA param
              | param'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_param(p):
    'param : IDENTIFIER COLON type_spec'
    p[0] = sa.Param(p[1], p[3])

# Blocos e comandos

def p_block(p):
    'block : LBRACE stmts_opt RBRACE'
    p[0] = sa.Block(p[2] or [])


def p_stmts_opt(p):
    '''stmts_opt : stmts
                 | empty'''
    p[0] = p[1]


def p_stmts(p):
    '''stmts : stmts stmt
             | stmt'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_stmt(p):
    '''stmt : expr_stmt SEMICOLON
        | assign_stmt SEMICOLON
        | return_stmt SEMICOLON
            | var_decl SEMICOLON
            | const_decl SEMICOLON
            | if_stmt
            | while_stmt
            | block'''
    p[0] = p[1]


def p_expr_stmt(p):
    'expr_stmt : expression'
    p[0] = sa.ExprStmt(p[1])


def p_assign_stmt(p):
    'assign_stmt : IDENTIFIER ASSIGN expression'
    p[0] = sa.AssignStmt(p[1], p[3])


def p_return_stmt(p):
    '''return_stmt : KEYWORD_RETURN expression
                   | KEYWORD_RETURN'''
    if len(p) == 3:
        p[0] = sa.ReturnStmt(p[2])
    else:
        p[0] = sa.ReturnStmt(None)


def p_if_stmt(p):
    '''if_stmt : KEYWORD_IF LPAREN expression RPAREN block %prec IFX
               | KEYWORD_IF LPAREN expression RPAREN block KEYWORD_ELSE block'''
    if len(p) == 6:
        p[0] = sa.IfStmt(p[3], p[5], None)
    else:
        p[0] = sa.IfStmt(p[3], p[5], p[7])


def p_while_stmt(p):
    'while_stmt : KEYWORD_WHILE LPAREN expression RPAREN block'
    p[0] = sa.WhileStmt(p[3], p[5])

# Expressões

def p_expression_binary(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MODULUS expression
                  | expression EQUALS_THEN expression
                  | expression NOT_EQUALS expression
                  | expression LESS_THEN expression
                  | expression LESS_EQUALS expression
                  | expression GREATER_THEN expression
                  | expression GREATER_EQUALS expression'''
    p[0] = sa.BinaryExpr(p[2], p[1], p[3])


def p_expression_unary(p):
    '''expression : NOT expression
                  | MINUS expression %prec UMINUS
                  | PLUS expression %prec UPLUS
                  '''
    p[0] = sa.UnaryExpr(p[1], p[2])


def p_expression_postfix(p):
    'expression : primary'
    p[0] = p[1]


def p_primary(p):
    '''primary : NUMBER
               | STRING
               | CHARACTER
               | KEYWORD_TRUE
               | KEYWORD_FALSE
               | LPAREN expression RPAREN
               | call'''
    if len(p) == 2:
        if isinstance(p[1], sa.FunctionCall):
            p[0] = p[1]
        elif p.slice[1].type == 'KEYWORD_TRUE':
            p[0] = sa.Literal(True)
        elif p.slice[1].type == 'KEYWORD_FALSE':
            p[0] = sa.Literal(False)
        elif isinstance(p[1], (int, float)):
            p[0] = sa.Literal(p[1])
        elif isinstance(p[1], str) and p.slice[1].type in ('STRING', 'CHARACTER'):
            p[0] = sa.Literal(p[1])
        else:
            p[0] = sa.Identifier(p[1])
    else:
        p[0] = p[2]


def p_primary_id(p):
    '''primary : IDENTIFIER'''
    p[0] = sa.Identifier(p[1])


def p_call(p):
    '''call : IDENTIFIER LPAREN args_opt RPAREN'''
    p[0] = sa.FunctionCall(p[1], p[3] or [])


def p_args_opt(p):
    '''args_opt : args
                | empty'''
    p[0] = p[1]


def p_args(p):
    '''args : args COMMA expression
            | expression'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_empty(p):
    'empty :'
    p[0] = None


def p_error(p):
    global isFine
    if p:
        print(f"Erro sintático próximo a '{p.value}' na linha {p.lineno}")
    else:
        print("Erro sintático no fim do arquivo")
    isFine = False

def build_parser():
    if QUIET_PLY:
        return yacc.yacc(start='program', errorlog=yacc.NullLogger())
    return yacc.yacc(start='program')


def parse(data):
    parser = build_parser()
    return parser.parse(data, lexer=lexer)


def print_result(result):
    if hasattr(result, 'print') and callable(getattr(result, 'print')):
        result.print()
        print()
    else:
        print(result)


def main():
    global isFine
    logging.basicConfig(filename='logSintatico.txt', level=logging.INFO, filemode='w')

    if arquivos_zig:
        for arquivo in arquivos_zig:
            isFine = True
            print(f"-----------Analise Sintatica do arquivo: {arquivo}-----------")
            logging.info(f"-----------Analise Sintatica do arquivo: {arquivo}-----------")

            with open(arquivo, 'r', encoding='utf-8') as f:
                lexer.input(f.read())
                result = build_parser().parse(debug=0)

            print_result(result)
            logging.info(result)

            if isFine:
                print("Analise sintatica realizada com sucesso!")
                logging.info("Analise sintatica realizada com sucesso!")
            else:
                print("Analise sintatica constatou erro!")
                logging.info("Analise sintatica constatou erro!")

            print("\n")
    else:
        f = open("input1.zig", "r")
        result = parse(f.read())
        if result is not None:
            print_result(result)
        else:
            print("Erro: programa nao foi reconhecido pelo parser.")


if __name__ == "__main__":
    main()
