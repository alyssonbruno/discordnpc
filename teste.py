import unittest as ut
from atendente import atendente

cliente1 = 'Legolas'
cliente2 = 'Gimli'
produtos = [{ 'nome': 'cerveja', 'valor': 10 },
{ 'nome': 'vinho', 'valor': 30 },
{ 'nome': 'banho', 'valor': 3}]

class TestBotAtendente(ut.TestCase):
    def __init__(self,*arg, **kwarg):
        super().__init__(*arg,**kwarg)
        for p in produtos:
            atendente.cadastrar_produto(p['nome'], p['valor'])

    def test_comprar(self):
        conta = atendente.comprar(cliente1,'cerveja')
        self.assertEqual(conta, 10, 'Comprar cerveja')
        self.assertEqual(atendente.pedir_conta(cliente1), conta, 'pedia conta')
        self.assertEqual(atendente.comprar(cliente1,'banho'),conta+3,'Comprar banho')


    def test_pagar_conta(self):
        conta = atendente.pedir_conta(cliente1)
        valor = 10
        self.assertEqual(atendente.pagar_conta(cliente1,valor),conta-valor, f'Pagando {valor} da conta')
        self.assertEqual(atendente.pagar_conta(cliente1),0, 'Quitando toda a conta')
    def test_repetir_pedido(self):
        pass


if __name__ == '__main__':
    ut.main()
