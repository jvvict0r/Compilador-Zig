# Tabela de Simbolos para Geracao de Assembly
# Dicionario que representa a tabela de simbolos.
symbolTable = []
INT = 'int'
FLOAT = 'float'
BOOL = 'bool'
VOID = 'void'
STRING = 'string'
CHAR = 'char'
TYPE = 'type'
PARAMS = 'params'
BINDABLE = 'bindable'
FUNCTION = 'fun'
VARIABLE = 'var'
CONSTANT = 'const'
SCOPE = 'scope'
SCOPE_GLOBAL = 'global'
OFFSET = 'offset'
SP = 'sp'
# Se DEBUG = -1, imprime conteudo da tabela de simbolos apos cada mudanca
DEBUG = 0
Number = [INT, FLOAT]


def printTable():
    global DEBUG
    if DEBUG == -1:
        print('Tabela:', symbolTable)

def beginScope(nameScope):
    global symbolTable
    symbolTable.append({})
    symbolTable[-1][SCOPE] = nameScope
    symbolTable[-1][SP] = 0
    printTable()

def endScope():
    global symbolTable
    symbolTable = symbolTable[0:-1]
    printTable()

def addVar(name, type):
    global symbolTable
    if name not in symbolTable[-1]:
        symbolTable[-1][SP] -= 4
        symbolTable[-1][name] = {BINDABLE: VARIABLE, TYPE: type, OFFSET: symbolTable[-1][SP]}
    else:
        symbolTable[-1][name] = {BINDABLE: VARIABLE, TYPE: type, OFFSET: symbolTable[-1][name][OFFSET]}
    printTable()

def addConst(name, type):
    global symbolTable
    if name not in symbolTable[-1]:
        symbolTable[-1][SP] -= 4
        symbolTable[-1][name] = {BINDABLE: CONSTANT, TYPE: type, OFFSET: symbolTable[-1][SP]}
    else:
        symbolTable[-1][name] = {BINDABLE: CONSTANT, TYPE: type, OFFSET: symbolTable[-1][name][OFFSET]}
    printTable()

def addFunction(name, params, returnType):
    global symbolTable
    symbolTable[-1][name] = {BINDABLE: FUNCTION, PARAMS: params, TYPE: returnType}
    printTable()

def addSP(value):
    global symbolTable
    symbolTable[-1][SP] += value

def getSP():
    return symbolTable[-1][SP]

def getBindable(bindableName):
    global symbolTable
    for i in reversed(range(len(symbolTable))):
        if bindableName in symbolTable[i].keys():
            return symbolTable[i][bindableName]
    return None

def getScope(bindableName=None):
    global symbolTable
    if bindableName is None:
        return symbolTable[-1][SCOPE]
    for i in reversed(range(len(symbolTable))):
        if bindableName in symbolTable[i].keys():
            return symbolTable[i][SCOPE]
    return symbolTable[-1][SCOPE]

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
    print('\n# Adicionando var b do tipo int')
    addVar('b', INT)
    print('\n# Consultando SP')
    print(getSP())
    print('\n# Removendo escopo add')
    endScope()

if __name__ == "__main__":
    main()
