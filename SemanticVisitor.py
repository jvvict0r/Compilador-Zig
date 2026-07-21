from Visitor import Visitor
from AbstractVisitor import AbstractVisitor
import SymbolTable as st
import SintaxeAbstrata as sa

def coercion(type1, type2):
    if type1 is None or type2 is None:
        return None
    
    if type1 in st.Number and type2 in st.Number:
        if type1 == st.FLOAT or type2 == st.FLOAT:
            return st.FLOAT
        return st.INT
    
    if type1 == type2:
        return type1
    
    return None


class SemanticVisitor(AbstractVisitor):
    def __init__(self):
        self.printer = Visitor()
        self.n_errors = 0
        st.beginScope('global')
        # Registrar funcoes built-in (nativas)
        st.addFunction('print', ['value', st.INT], st.VOID)

    def visitProgram(self, program):
        for item in program.items:
            item.accept(self)

    def visitConstDecl(self, constDecl):
        typeValue = constDecl.value.accept(self)
        
        if constDecl.type_spec is not None:
            declaredType = constDecl.type_spec
            if typeValue is not None and typeValue != declaredType:
                if coercion(typeValue, declaredType) is None:
                    self.n_errors += 1
                    print(f"\n\t[Erro] Tipo incompatível na declaração da constante '{constDecl.name}'.")
                    print(f"\tTipo declarado: {declaredType}, tipo da expressão: {typeValue}\n")
            st.addConst(constDecl.name, declaredType)
            return declaredType
        else:
            st.addConst(constDecl.name, typeValue)
            return typeValue

    def visitVarDecl(self, varDecl):
        typeValue = varDecl.value.accept(self)
        
        if varDecl.type_spec is not None:
            declaredType = varDecl.type_spec
            if typeValue is not None and typeValue != declaredType:
                if coercion(typeValue, declaredType) is None:
                    self.n_errors += 1
                    print(f"\n\t[Erro] Tipo incompatível na declaração da variável '{varDecl.name}'.")
                    print(f"\tTipo declarado: {declaredType}, tipo da expressão: {typeValue}\n")
            st.addVar(varDecl.name, declaredType)
            return declaredType
        else:
            st.addVar(varDecl.name, typeValue)
            return typeValue

    def visitFunction(self, function):
        params = []
        for param in function.params:
            params.append(param.name)
            params.append(param.type_spec)
        
        returnType = function.return_type if function.return_type else st.VOID
        st.addFunction(function.name, params, returnType)
        
        st.beginScope(function.name)
        
        for i in range(0, len(params), 2):
            st.addVar(params[i], params[i + 1])
        
        function.body.accept(self)
        st.endScope()

    def visitParam(self, param):
        return [param.name, param.type_spec]

    def visitBlock(self, block):
        for stmt in block.statements:
            stmt.accept(self)

    def visitExprStmt(self, exprStmt):
        exprStmt.expr.accept(self)

    def visitAssignStmt(self, assignStmt):
        typeValue = assignStmt.value.accept(self)
        
        bindable = st.getBindable(assignStmt.name)
        if bindable is None:
            self.n_errors += 1
            print(f"\n\t[Erro] Variável '{assignStmt.name}' não foi declarada.\n")
            return None
        
        if bindable[st.BINDABLE] == st.CONSTANT:
            self.n_errors += 1
            print(f"\n\t[Erro] Não é possível reatribuir valor à constante '{assignStmt.name}'.\n")
            return None
        
        varType = bindable[st.TYPE]
        if varType is not None and typeValue is not None:
            if coercion(varType, typeValue) is None:
                self.n_errors += 1
                print(f"\n\t[Erro] Tipos incompatíveis na atribuição.")
                print(f"\tVariável '{assignStmt.name}' é do tipo {varType}, mas recebeu {typeValue}\n")
        
        return varType

    def visitReturnStmt(self, returnStmt):
        typeExp = None
        if returnStmt.value is not None:
            typeExp = returnStmt.value.accept(self)
        else:
            typeExp = st.VOID
        
        scope = st.getCurrentScope()
        bindable = st.getBindable(scope)
        
        if bindable is not None and bindable[st.BINDABLE] == st.FUNCTION:
            expectedType = bindable[st.TYPE]
            if expectedType != typeExp:
                if coercion(expectedType, typeExp) is None:
                    self.n_errors += 1
                    returnStmt.accept(self.printer)
                    print(f"\n\t[Erro] O retorno da função '{scope}' é do tipo {expectedType},")
                    print(f"\tno entanto, o retorno passado foi do tipo {typeExp}\n")
        
        return typeExp

    def visitIfStmt(self, ifStmt):
        condType = ifStmt.condition.accept(self)
        
        if condType != st.BOOL:
            self.n_errors += 1
            print(f"\n\t[Erro] A condição do 'if' deve ser do tipo bool, mas é do tipo {condType}\n")
        
        ifStmt.then_block.accept(self)
        
        if ifStmt.else_block is not None:
            ifStmt.else_block.accept(self)

    def visitWhileStmt(self, whileStmt):
        condType = whileStmt.condition.accept(self)
        
        if condType != st.BOOL:
            self.n_errors += 1
            print(f"\n\t[Erro] A condição do 'while' deve ser do tipo bool, mas é do tipo {condType}\n")
        
        whileStmt.body.accept(self)

    def visitBinaryExpr(self, binaryExpr):
        tipoLeft = binaryExpr.left.accept(self)
        tipoRight = binaryExpr.right.accept(self)
        
        comparison_ops = ['<', '>', '<=', '>=', '==', '!=']
        if binaryExpr.op in comparison_ops:
            c = coercion(tipoLeft, tipoRight)
            if c is None:
                self.n_errors += 1
                print(f"\n\t[Erro] Comparação inválida. Expressão esquerda é do tipo {tipoLeft},")
                print(f"\tenquanto a expressão direita é do tipo {tipoRight}\n")
            return st.BOOL

        arithmetic_ops = ['+', '-', '*', '/', '%']
        if binaryExpr.op in arithmetic_ops:
            c = coercion(tipoLeft, tipoRight)
            if c is None:
                self.n_errors += 1
                print(f"\n\t[Erro] Operação aritmética inválida '{binaryExpr.op}'.")
                print(f"\tExpressão esquerda é do tipo {tipoLeft},")
                print(f"\tenquanto a expressão direita é do tipo {tipoRight}\n")
            return c

        logical_ops = ['and', 'or']
        if binaryExpr.op in logical_ops:
            if tipoLeft != st.BOOL or tipoRight != st.BOOL:
                self.n_errors += 1
                print(f"\n\t[Erro] Operação lógica '{binaryExpr.op}' requer operandos booleanos.")
                print(f"\tTipos recebidos: {tipoLeft} e {tipoRight}\n")
            return st.BOOL
        
        return coercion(tipoLeft, tipoRight)

    def visitUnaryExpr(self, unaryExpr):
        tipoExpr = unaryExpr.expr.accept(self)
        
        if unaryExpr.op == '!':
            if tipoExpr != st.BOOL:
                self.n_errors += 1
                print(f"\n\t[Erro] Operador '!' requer operando booleano, mas recebeu {tipoExpr}\n")
            return st.BOOL

        if unaryExpr.op in ['-', '+']:
            if tipoExpr not in st.Number:
                self.n_errors += 1
                print(f"\n\t[Erro] Operador '{unaryExpr.op}' requer operando numérico, mas recebeu {tipoExpr}\n")
            return tipoExpr
        
        return tipoExpr

    def visitLiteral(self, literal):
        value = literal.value
        
        if isinstance(value, bool):
            return st.BOOL
        elif isinstance(value, int):
            return st.INT
        elif isinstance(value, float):
            return st.FLOAT
        elif isinstance(value, str):
            return st.STRING
        
        return None

    def visitIdentifier(self, identifier):
        bindable = st.getBindable(identifier.name)
        
        if bindable is not None:
            return bindable[st.TYPE]
        
        self.n_errors += 1
        print(f"\n\t[Erro] Identificador '{identifier.name}' não foi declarado.\n")
        return None

    def visitFunctionCall(self, functionCall):
        bindable = st.getBindable(functionCall.name)
        
        if bindable is None:
            self.n_errors += 1
            print(f"\n\t[Erro] Função '{functionCall.name}' não foi declarada.\n")
            return None
        
        if bindable[st.BINDABLE] != st.FUNCTION:
            self.n_errors += 1
            print(f"\n\t[Erro] '{functionCall.name}' não é uma função.\n")
            return None
        
        # Função print aceita (int, string)
        if functionCall.name == 'print':
            if len(functionCall.args) != 1:
                self.n_errors += 1
                print(f"\n\t[Erro] 'print' espera exatamente 1 argumento, recebeu {len(functionCall.args)}\n")
            else:
                functionCall.args[0].accept(self)
            return st.VOID
        
        # Verificar número de parâmetros
        paramsList = bindable[st.PARAMS]
        expectedCount = len(paramsList) // 2
        actualCount = len(functionCall.args)
        
        if expectedCount != actualCount:
            self.n_errors += 1
            print(f"\n\t[Erro] Chamada da função '{functionCall.name}' com número incorreto de argumentos.")
            print(f"\tEsperado: {expectedCount}, recebido: {actualCount}\n")
            return bindable[st.TYPE]
        
        # Verificar tipos dos parâmetros
        expectedTypes = paramsList[1::2]  # tipos nas posições ímpares
        actualTypes = []
        for arg in functionCall.args:
            actualTypes.append(arg.accept(self))
        
        for i, (expected, actual) in enumerate(zip(expectedTypes, actualTypes)):
            if actual is not None and expected != actual:
                if coercion(expected, actual) is None:
                    self.n_errors += 1
                    paramName = paramsList[i * 2]
                    print(f"\n\t[Erro] Tipo incompatível no argumento '{paramName}' da função '{functionCall.name}'.")
                    print(f"\tEsperado: {expected}, recebido: {actual}\n")
        
        return bindable[st.TYPE]

    def getnerros(self):
        return self.n_errors


def main():
    from ExpressionLanguageParser import parse
    print("# Análise Semântica #")
    print("=" * 50)
    f = open("input1.zig", "r")
    result = parse(f.read())
    
    if result is not None:
        svisitor = SemanticVisitor()
        result.accept(svisitor)
        print("=" * 50)
        print(f"Foram encontrados {svisitor.getnerros()} erro(s) semântico(s)")
    else:
        print("Erro no parsing do código")


if __name__ == "__main__":
    main()