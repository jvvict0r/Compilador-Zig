const limite: int = 5;
var i: int = 0;

fn soma(a: int, b: int) int {
    var c: int = a + b;
    return c;
}

fn obterMensagem() string {
    return "Resultado da soma:";
}

fn main() void {
    print("Contando de 0 ate 4:");

    while (i < limite) {
        print(i);
        i = i + 1;
    }

    var resultadoSoma: int = soma(10, 20);
    var mensagemIntroducao: string = obterMensagem();
    print(mensagemIntroducao);
    print(resultadoSoma);


    var palavraFinal: string = "Projeto Compilador Zig - Linguagens Formais e Tradutores";
    print(palavraFinal);
    return;
}