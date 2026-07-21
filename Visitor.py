from AbstractVisitor import AbstractVisitor
from ExpressionLanguageParser import parse

tab = 0

def blank():
    p = ''
    for x in range(tab):
        p = p + ' '
    return p


class Visitor(AbstractVisitor):

    def visitProgram(self, program):
        for item in program.items:
            item.accept(self)
            print()

    def visitConstDecl(self, constDecl):
        type_part = f": {constDecl.type_spec}" if constDecl.type_spec else ""
        print(f"{blank()}const {constDecl.name}{type_part} = ", end="")
        constDecl.value.accept(self)
        print(";")

    def visitVarDecl(self, varDecl):
        type_part = f": {varDecl.type_spec}" if varDecl.type_spec else ""
        print(f"{blank()}var {varDecl.name}{type_part} = ", end="")
        varDecl.value.accept(self)
        print(";")

    def visitFunction(self, function):
        global tab
        vis = "pub " if function.visibility else ""
        params_txt = ", ".join([p.format() for p in function.params])
        ret = f" {function.return_type}" if function.return_type else ""
        print(f"{blank()}{vis}fn {function.name}({params_txt}){ret} ", end="")
        function.body.accept(self)

    def visitParam(self, param):
        print(f"{param.name}: {param.type_spec}", end="")

    def visitBlock(self, block):
        global tab
        print("{")
        tab += 4
        for stmt in block.statements:
            print(blank(), end="")
            stmt.accept(self)
            print()
        tab -= 4
        print(f"{blank()}}}", end="")

    def visitExprStmt(self, exprStmt):
        exprStmt.expr.accept(self)
        print(";", end="")

    def visitAssignStmt(self, assignStmt):
        print(f"{assignStmt.name} = ", end="")
        assignStmt.value.accept(self)
        print(";", end="")

    def visitReturnStmt(self, returnStmt):
        if returnStmt.value is None:
            print("return;", end="")
        else:
            print("return ", end="")
            returnStmt.value.accept(self)
            print(";", end="")

    def visitIfStmt(self, ifStmt):
        global tab
        print("if (", end="")
        ifStmt.condition.accept(self)
        print(") ", end="")
        ifStmt.then_block.accept(self)
        if ifStmt.else_block:
            print(" else ", end="")
            ifStmt.else_block.accept(self)

    def visitWhileStmt(self, whileStmt):
        print("while (", end="")
        whileStmt.condition.accept(self)
        print(") ", end="")
        whileStmt.body.accept(self)

    def visitBinaryExpr(self, binaryExpr):
        print("(", end="")
        binaryExpr.left.accept(self)
        print(f" {binaryExpr.op} ", end="")
        binaryExpr.right.accept(self)
        print(")", end="")

    def visitUnaryExpr(self, unaryExpr):
        print(f"{unaryExpr.op}", end="")
        unaryExpr.expr.accept(self)

    def visitLiteral(self, literal):
        if isinstance(literal.value, str):
            print(f'"{literal.value}"', end="")
        else:
            print(literal.value, end="")

    def visitIdentifier(self, identifier):
        print(identifier.name, end="")

    def visitFunctionCall(self, functionCall):
        print(f"{functionCall.name}(", end="")
        for i, arg in enumerate(functionCall.args):
            arg.accept(self)
            if i < len(functionCall.args) - 1:
                print(", ", end="")
        print(")", end="")


def main():
    f = open("input1.zig", "r")
    result = parse(f.read())
    if result is None:
        print("Erro: programa nao foi reconhecido pelo parser.")
        return
    visitor = Visitor()
    result.accept(visitor)


if __name__ == "__main__":
    main()