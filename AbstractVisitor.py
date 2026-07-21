from abc import abstractmethod, ABCMeta


class AbstractVisitor(metaclass=ABCMeta):
    @abstractmethod
    def visitProgram(self, program): pass

    @abstractmethod
    def visitConstDecl(self, constDecl): pass

    @abstractmethod
    def visitVarDecl(self, varDecl): pass

    @abstractmethod
    def visitFunction(self, function): pass

    @abstractmethod
    def visitParam(self, param): pass

    @abstractmethod
    def visitBlock(self, block): pass

    @abstractmethod
    def visitExprStmt(self, exprStmt): pass

    @abstractmethod
    def visitAssignStmt(self, assignStmt): pass

    @abstractmethod
    def visitReturnStmt(self, returnStmt): pass

    @abstractmethod
    def visitIfStmt(self, ifStmt): pass

    @abstractmethod
    def visitWhileStmt(self, whileStmt): pass

    @abstractmethod
    def visitBinaryExpr(self, binaryExpr): pass

    @abstractmethod
    def visitUnaryExpr(self, unaryExpr): pass

    @abstractmethod
    def visitLiteral(self, literal): pass

    @abstractmethod
    def visitIdentifier(self, identifier): pass

    @abstractmethod
    def visitFunctionCall(self, functionCall): pass