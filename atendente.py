class Cliente:
    _clientes = {}
    def __init__(self, nome: str)->None:
        if nome not in self._clientes.keys():
            self._clientes[nome] = {'conta': 0}
        self.dados = self._clientes[nome]

    def movimenta_conta(self, valor: int)->int:
        self.dados['conta'] += valor
        return self.dados['conta']

class Produto:
    _produtos = {}
    def __init__(self, nome: str, preco: int = 0)->None:
        if nome not in self._produtos.keys():
            self._produtos[nome] = { 'preco': preco }
        self.dados = self._produtos[nome]

class _Atendente:
    def cadastrar_produto(self, nome, valor) -> int:
        p = Produto(nome, valor)
        return p.dados['preco']

    def comprar(self, nome_cliente: str, nome_produto: str, quantidade: int=1)->int:
        cliente = Cliente(nome_cliente)
        produto = Produto(nome_produto)
        return cliente.movimenta_conta(produto.dados['preco']*quantidade)

    def pedir_conta(self, nome_cliente: str) -> int:
        cliente = Cliente(nome_cliente)
        return cliente.dados['conta']

    def pagar_conta(self, nome_cliente: str, valor: int = 0)->int:
        cliente = Cliente(nome_cliente)
        deve = cliente.dados['conta']
        if valor == 0:
            valor = deve
        sobra = cliente.movimenta_conta(valor*-1)
        return sobra


atendente = _Atendente()
