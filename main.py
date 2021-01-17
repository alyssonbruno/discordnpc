#!/bin/env python3
import discord
from random import choice
from time import asctime, time
from json import loads
from typing import Optional
from atendente import atendente

print(f'Iniciando o BOT as {asctime()}')

TIMEOUT_EM_MINUTOS=10
client = discord.Client()
conta = {}
produto_padrao = [{'nome':'cerveja', 'dados': {'preço': 3, 'alias': ['birra'] }}, {'nome': 'comida', 'dados': {'preço': 5, 'alias': ['refeição', 'gororoba', 'almoço', 'janta']}},{'nome':'vinho', 'dados': {'preço': 15, 'alias': []}}]
json_frase = ','.join([ s.strip() for s in open('/home/ubuntu/bots/discord/frases.txt').readlines() ])
json_txt = ','.join([ s.strip() for s in open('/home/ubuntu/bots/discord/produtos.txt').readlines() ])

OPERACOES = {
        'comprar':atendente.comprar,
        'pagar': atendente.pagar_conta,
        'repetir': lambda cliente: print(cliente)
}

busca = None
produtos = None
frases = None
agora = None
antes = None
def comprar(cliente,produto):
    pass

OPERACOES['comprar'] = comprar

def pagar(cliente):
    pass

OPERACOES['pagar'] = pagar

def repetir_pedido(cliente):
    pass

OPERACOES['repetir'] = repetir_pedido

def limpar_cache() -> None:
    global agora, antes, produtos, busca, conj
    agora = time()
    if (antes is None) or ((agora-antes)>TIMEOUT_EM_MINUTOS*60):
        antes = agora
        busca = None
        produtos = None
        frases = None
        conj = None

def carregar_produtos() -> Optional[list]:
    global produtos
    if produtos is None:
        try:
            produtos = loads(f'[{json_txt}]')
        except:
            print('Arquivo não encontrado, usando dados default')
            produtos = produto_padrao
    return produtos

def busca_produto(produto: str) -> Optional[str]:
    for from_json in carregar_produtos():
        nome = from_json['nome']
        apelidos = from_json['dados']['alias']
        if produto == nome or produto in apelidos:
            return nome
    else:
        return None

def escolhe_frase(produto: str) -> str:
    global frases
    if frases is None:
        frases = loads(f'[{json_frase}]')
    for from_json in frases:
        if produto in from_json['produtos']:
            return choice(from_json['frases'])
    return 'A atendente trouxe {produto} para {cliente}, informando que a conta foi {valor}'

def monta_busca():
    global busca
    if busca is None:
        busca = []
        for from_json in carregar_produtos():
            nome = from_json['nome']
            dados = from_json['dados']
            conj = carregar_conj()
            busca += [(c.format(a), nome) for c in conj for a in dados['alias']] + [(c.format(nome), nome) for c in conj]
        print(busca)
    return busca

def totalizar(c):
    retorno = 0
    if c not in conta.keys():
        return '0'
    else:
        for from_json in carregar_produtos():
            nome = from_json['nome']
            dados = from_json['dados']
            if nome in conta[c].keys():
                retorno += conta[c][nome] * dados['preço']
    return f'{retorno} PC'

def incluir(c, p):
    if c in conta.keys():
        if p in conta[c].keys():
            conta[c][p] += 1
        else:
            conta[c][p] = 1
    else:
        conta[c] = {}
        conta[c][p] = 1

def produto_frase(cli, frase):
    rep = ['quero mais']
    pag = ['pagando', 'pago']
    for f,p in monta_busca():
        #print(f'frase: {frase} \t busca: {p}')
        if frase.find(f)>=0:
            return busca_produto(p)
    else:
        for m in rep:
            if frase.find(m)>=0:
                return -1
        else:
            for m in pag:
                if frase.find(m)>=0:
                    return -2
    return None
    
@client.event
async def on_ready():
    print('Logado no Discord como {0.user}'.format(client))

@client.event
async def on_message(message):
    # print(f'processando mensagem: {message.content}')
    limpar_cache()
    if message.author == client.user:
        return
    _talk = message.content.lower()
    _cliente = message.author.display_name
    _produto = produto_frase(_cliente, _talk)
    # print(_produto, type(_produto))
    if type(_produto) is str:
        incluir(_cliente, _produto)
        _valor = totalizar(_cliente)
        _frase = escolhe_frase(_produto)
        # print(f'Enviando a frase: {_frase}')
        await message.channel.send(_frase.format(cliente=_cliente, produto=_produto, valor=_valor).strip())

if __name__ == '__main__':
    chave = None
    if 'KEY_ATENDENTE' in os.environ.keys:
        chave = os.environ['KEY_ATENDENTE']
    client.run(chave)
