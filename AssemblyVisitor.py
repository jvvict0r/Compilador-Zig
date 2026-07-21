from AbstractVisitor import AbstractVisitor
from ExpressionLanguageParser import parse
import AssemblyST as st


def getAssemblyType(type=None):
    return ".word"


class AssemblyVisitor(AbstractVisitor):

    def __init__(self):
        st.beginScope(st.SCOPE_GLOBAL)
        self.funcs = []
        self.text = []
        self.text.append(".text")
        self.text.append("    move $fp, $sp")
        self.data = set()
        self.string_data = {}
        self.str_count = 0
        self.rotulos = {}
        self.var_types = {}
        self.func_ret_types = {}
        # Registrar funcoes nativas
        st.addFunction('print', ['value', '.word'], st.VOID)

    def novo_rotulo(self, string):
        if string not in self.rotulos:
            self.rotulos[string] = 0
        rotulo = f"{string}_{self.rotulos[string]}"
        self.rotulos[string] += 1
        return rotulo

    # Devolve a lista de instrucoes de acordo com o escopo
    def getList(self):
        return self.text if st.getScope() == st.SCOPE_GLOBAL else self.funcs

    def visitProgram(self, program):
        for item in program.items:
            item.accept(self)

    def visitConstDecl(self, constDecl):
        name = constDecl.name
        import SintaxeAbstrata as sa
        if isinstance(constDecl.value, sa.Literal) and isinstance(constDecl.value.str_value if hasattr(constDecl.value, 'str_value') else constDecl.value.value, str) and not isinstance(constDecl.value.value, bool):
            self.var_types[name] = 'string'
        constDecl.value.accept(self)
        self.data.add(name)
        st.addConst(name, getAssemblyType())
        self.text.append(f"    sw $v0, {name}")

    def visitVarDecl(self, varDecl):
        code = self.getList()
        name = varDecl.name
        import SintaxeAbstrata as sa
        # Detectar tipo string (literal ou chamada de funcao que retorna string)
        if isinstance(varDecl.value, sa.Literal) and isinstance(varDecl.value.value, str) and not isinstance(varDecl.value.value, bool):
            self.var_types[name] = 'string'
        elif isinstance(varDecl.value, sa.FunctionCall):
            # Marcar como string somente se a funcao retorna string
            if self.func_ret_types.get(varDecl.value.name) == 'string':
                self.var_types[name] = 'string'
        varDecl.value.accept(self)
        if st.getScope() == st.SCOPE_GLOBAL:
            self.data.add(name)
            st.addVar(name, getAssemblyType())
            code.append(f"    sw $v0, {name}")
        else:
            st.addVar(name, getAssemblyType())
            bind = st.getBindable(name)
            code.append(f"    sw $v0, {bind[st.OFFSET]}($fp)")

    def visitFunction(self, function):
        params = []
        for param in function.params:
            params.append(param.name)
            params.append(getAssemblyType())

        returnType = getAssemblyType()
        # Registrar tipo de retorno da funcao (para detectar string)
        if function.return_type == 'string':
            self.func_ret_types[function.name] = 'string'
        st.addFunction(function.name, params, returnType)
        st.beginScope(function.name)

        code = self.getList()
        code.append(f"{function.name}:")
        code.append("    move $fp, $sp")

        # Parametros ficam em offsets POSITIVOS a partir de $fp
        # Corpo da pilha ao entrar na funcao:
        #   0($fp) = saved $fp
        #   4($fp) = saved $ra
        #   8($fp) = ultimo argumento empilhado
        #   12($fp) = penultimo argumento
        n_params = len(params) // 2
        for k in range(0, len(params), 2):
            param_index = k // 2
            offset = 8 + 4 * (n_params - 1 - param_index)
            st.symbolTable[-1][params[k]] = {
                st.BINDABLE: st.VARIABLE,
                st.TYPE: params[k + 1],
                st.OFFSET: offset
            }

        sp_placeholder_index = len(code)
        code.append("    addi $sp, $sp, 0")
        function.body.accept(self)
        code[sp_placeholder_index] = f"    addi $sp, $sp, {st.getSP()}"

        st.endScope()

    def visitParam(self, param):
        return [param.name, getAssemblyType()]

    def visitBlock(self, block):
        for stmt in block.statements:
            stmt.accept(self)

    def visitExprStmt(self, exprStmt):
        exprStmt.expr.accept(self)

    def visitAssignStmt(self, assignStmt):
        code = self.getList()
        assignStmt.value.accept(self)
        bind = st.getBindable(assignStmt.name)
        if bind is None:
            st.addVar(assignStmt.name, getAssemblyType())
            bind = st.getBindable(assignStmt.name)
        if st.getScope(assignStmt.name) == st.SCOPE_GLOBAL:
            code.append(f"    sw $v0, {assignStmt.name}")
        else:
            code.append(f"    sw $v0, {bind[st.OFFSET]}($fp)")

    def visitReturnStmt(self, returnStmt):
        code = self.getList()
        if returnStmt.value is not None:
            returnStmt.value.accept(self)
        code.append("    move $sp, $fp")
        code.append("    jr $ra")

    def visitIfStmt(self, ifStmt):
        code = self.getList()
        rotulo_else = self.novo_rotulo("else")
        rotulo_fim = self.novo_rotulo("fim_if")

        ifStmt.condition.accept(self)
        if ifStmt.else_block is not None:
            code.append(f"    beq $v0, $zero, {rotulo_else}")
            ifStmt.then_block.accept(self)
            code.append(f"    j {rotulo_fim}")
            code.append(f"{rotulo_else}:")
            ifStmt.else_block.accept(self)
            code.append(f"{rotulo_fim}:")
        else:
            code.append(f"    beq $v0, $zero, {rotulo_fim}")
            ifStmt.then_block.accept(self)
            code.append(f"{rotulo_fim}:")

    def visitWhileStmt(self, whileStmt):
        code = self.getList()
        rotulo_inicial = self.novo_rotulo("while")
        rotulo_final = self.novo_rotulo("fim_while")
        code.append(f"{rotulo_inicial}:")
        whileStmt.condition.accept(self)
        code.append(f"    beq $v0, $zero, {rotulo_final}")
        whileStmt.body.accept(self)
        code.append(f"    j {rotulo_inicial}")
        code.append(f"{rotulo_final}:")

    def visitBinaryExpr(self, binaryExpr):
        code = self.getList()
        # Avalia a expressao esquerda
        binaryExpr.left.accept(self)
        code.append("    addi $sp, $sp, -4")
        st.addSP(-4)
        code.append("    sw $v0, 0($sp)")
        # Avalia a expressao direita
        binaryExpr.right.accept(self)
        # Recupera o operando esquerdo
        code.append("    lw $t0, 0($sp)")
        code.append("    addi $sp, $sp, 4")
        st.addSP(4)

        op = binaryExpr.op
        if op == '+':
            code.append("    add $v0, $t0, $v0")
        elif op == '-':
            code.append("    sub $v0, $t0, $v0")
        elif op == '*':
            code.append("    mul $v0, $t0, $v0")
        elif op == '/':
            code.append("    div $t0, $v0")
            code.append("    mflo $v0")
        elif op == '%':
            code.append("    div $t0, $v0")
            code.append("    mfhi $v0")
        elif op == '<':
            code.append("    slt $v0, $t0, $v0")
        elif op == '>':
            code.append("    slt $v0, $v0, $t0")
        elif op == '<=':
            # a <= b  equivale a  !(a > b)  equivale a  !(b < a)
            code.append("    slt $v0, $v0, $t0")
            code.append("    xori $v0, $v0, 1")
        elif op == '>=':
            # a >= b  equivale a  !(a < b)
            code.append("    slt $v0, $t0, $v0")
            code.append("    xori $v0, $v0, 1")
        elif op == '==':
            code.append("    sub $v0, $t0, $v0")
            code.append("    sltiu $v0, $v0, 1")
        elif op == '!=':
            code.append("    sub $v0, $t0, $v0")
            code.append("    sltu $v0, $zero, $v0")

    def visitUnaryExpr(self, unaryExpr):
        code = self.getList()
        unaryExpr.expr.accept(self)
        if unaryExpr.op == '-':
            code.append("    sub $v0, $zero, $v0")
        elif unaryExpr.op == '!':
            code.append("    xori $v0, $v0, 1")

    def visitLiteral(self, literal):
        code = self.getList()
        value = literal.value
        if isinstance(value, bool):
            code.append(f"    li $v0, {1 if value else 0}")
        elif isinstance(value, (int, float)):
            code.append(f"    li $v0, {int(value)}")
        elif isinstance(value, str):
            # Armazenar string no .data e carregar endereco
            str_label = f"str_{self.str_count}"
            self.str_count += 1
            self.string_data[str_label] = value
            code.append(f"    la $v0, {str_label}")

    def visitIdExp(self, idExp):
        code = self.getList()
        bind = st.getBindable(idExp.name)
        if bind is not None:
            if st.getScope(idExp.name) == st.SCOPE_GLOBAL:
                code.append(f"    lw $v0, {idExp.name}")
            else:
                code.append(f"    lw $v0, {bind[st.OFFSET]}($fp)")

    def visitIdentifier(self, identifier):
        code = self.getList()
        bind = st.getBindable(identifier.name)
        if bind is not None:
            if st.getScope(identifier.name) == st.SCOPE_GLOBAL:
                code.append(f"    lw $v0, {identifier.name}")
            else:
                code.append(f"    lw $v0, {bind[st.OFFSET]}($fp)")

    def visitFunctionCall(self, functionCall):
        code = self.getList()
        # Funcao print(valor)
        if functionCall.name == 'print':
            if len(functionCall.args) > 0:
                arg = functionCall.args[0]
                # Verificar se o argumento e uma string literal
                import SintaxeAbstrata as sa
                if isinstance(arg, sa.Literal) and isinstance(arg.value, str):
                    # Armazenar string no .data como .asciiz
                    str_label = f"str_{self.str_count}"
                    self.str_count += 1
                    self.string_data[str_label] = arg.value
                    # Carregar endereco da string
                    code.append(f"    la $a0, {str_label}")
                    # Syscall 4 = print_string
                    code.append("    li $v0, 4")
                    code.append("    syscall")
                elif isinstance(arg, sa.Identifier) and self.var_types.get(arg.name) == 'string':
                    # Variavel do tipo string - carregar endereco e usar syscall 4
                    arg.accept(self)
                    code.append("    move $a0, $v0")
                    code.append("    li $v0, 4")
                    code.append("    syscall")
                else:
                    # Avaliar expressao inteira
                    arg.accept(self)
                    code.append("    move $a0, $v0")
                    # Syscall 1 = print_int
                    code.append("    li $v0, 1")
                    code.append("    syscall")
            # Imprimir newline (syscall 11, char 10)
            code.append("    li $v0, 11")
            code.append("    li $a0, 10")
            code.append("    syscall")
            return
        # Empilhar argumentos no $sp
        n_args = len(functionCall.args)
        for arg in functionCall.args:
            arg.accept(self)
            code.append("    addi $sp, $sp, -4")
            code.append("    sw $v0, 0($sp)")
        # Salvar contexto (ra + fp)
        code.append("    addi $sp, $sp, -8")
        code.append("    sw $ra, 4($sp)")
        code.append("    sw $fp, 0($sp)")
        # Chamar funcao
        code.append(f"    jal {functionCall.name}")
        # Restaurar contexto
        code.append("    lw $fp, 0($sp)")
        code.append("    lw $ra, 4($sp)")
        code.append("    addi $sp, $sp, 8")
        # Desempilhar argumentos
        if n_args > 0:
            code.append(f"    addi $sp, $sp, {4 * n_args}")

    # Gera codigo assembly final
    def get_code(self):
        finalcode = []
        if self.data or self.string_data:
            finalcode.append(".data")
            for globalVar in sorted(self.data):
                finalcode.append(f"    {globalVar}: .word 0")
            for label, value in self.string_data.items():
                escaped = value.replace('\n', '\\n').replace('\t', '\\t')
                finalcode.append(f'    {label}: .asciiz "{escaped}"')
        finalcode = finalcode + self.text
        finalcode.append("    jal main")
        finalcode.append("    j end")
        finalcode = finalcode + self.funcs
        finalcode.append("\nend:\n    li $v0, 10\n    syscall")
        return "\n".join(finalcode)


def main():
    f = open("input1.zig", "r")
    result = parse(f.read())
    if result is not None:
        assemblyvisitor = AssemblyVisitor()
        result.accept(assemblyvisitor)
        print(assemblyvisitor.get_code())
    else:
        print("Erro no parsing do codigo")


if __name__ == "__main__":
    main()
