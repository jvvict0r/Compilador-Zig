symbolTable = []
DEBUG = 0

# Tipos da linguagem
INT = 'int'
FLOAT = 'float'
BOOL = 'bool'
VOID = 'void'
STRING = 'string'
CHAR = 'char'

# Constantes
TYPE = 'type'
PARAMS = 'params'
BINDABLE = 'bindable'
FUNCTION = 'fun'
VARIABLE = 'var'
CONSTANT = 'const'
SCOPE = 'scope'
OFFSET = 'offset'
SP = 'sp'

# Conjuntos de tipos
Number = [INT, FLOAT]

def printTable():
    global DEBUG
    if DEBUG == -1:
        print('Tabela:', symbolTable)


def beginScope(nameScope):
    global symbolTable
    symbolTable.append({})
    symbolTable[-1][SCOPE] = nameScope
    printTable()


def endScope():
    global symbolTable
    symbolTable = symbolTable[0:-1]
    printTable()


def addVar(name, type, offset=None):
    global symbolTable
    symbolTable[-1][name] = {BINDABLE: VARIABLE, TYPE: type, OFFSET: offset}
    printTable()


def addConst(name, type, offset=None):
    global symbolTable
    symbolTable[-1][name] = {BINDABLE: CONSTANT, TYPE: type, OFFSET: offset}
    printTable()


def addFunction(name, params, returnType):
    global symbolTable
    symbolTable[-1][name] = {BINDABLE: FUNCTION, PARAMS: params, TYPE: returnType}
    printTable()


def getBindable(bindableName):
    global symbolTable
    for i in reversed(range(len(symbolTable))):
        if bindableName in symbolTable[i].keys():
            return symbolTable[i][bindableName]
    return None


def getScope(bindableName):
    global symbolTable
    for i in reversed(range(len(symbolTable))):
        if bindableName in symbolTable[i].keys():
            return symbolTable[i][SCOPE]
    return None


def getCurrentScope():
    global symbolTable
    if len(symbolTable) > 0:
        return symbolTable[-1][SCOPE]
    return None


def main():
    global DEBUG
    DEBUG = -1
    print('\n# Criando escopo global')
    beginScope('global')
    print('\n# Adicionando funcao add')
    addFunction('add', ['a', INT, 'b', INT], INT)
    print('\n# Criando escopo add')
    beginScope('add')
    print('\n# Adicionando var a do tipo int')
    addVar('a', INT)
    print('\n# Pegar escopo de var a')
    print(getScope('a'))
    print('\n# Adicionando var b do tipo int')
    addVar('b', INT)
    print('\n# Adicionando const c do tipo int')
    addConst('c', INT)
    print('\n# Consultando bindable inexistente')
    print(str(getBindable('naoexiste')))
    print('\n# Consultando bindable add')
    print(str(getBindable('add')))
    print('\n# Removendo escopo add')
    endScope()


if __name__ == "__main__":
    main()