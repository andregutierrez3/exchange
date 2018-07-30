from flask import Flask, redirect, url_for, jsonify

perfis = {}
deman = {}
oferta = {}
credito = {}

app = Flask(__name__)


class Operacao:
    def __init__(self, tipo, preco, qnt, pro, usuario):
        self.tipo = tipo
        self.preco = preco
        self.quantidade = qnt
        self.produto = pro
        self.usuario = usuario
        return

    def atualiza(self):
        if self.tipo == 'compra':
            l = list(oferta.get(self.produto, {'nao': ''}).keys())
            l.sort()
            for el in l:
                if el == 'nao':
                    print(deman)
                    if self.produto in deman:
                        deman[self.produto].update({self.preco: [self.quantidade, self.usuario]})
                    else:
                        deman[self.produto] = {self.preco: [self.quantidade, self.usuario]}

                    return jsonify({'resposta': 'pedido posto em espera'})

                elif self.preco >= el:

                    if oferta[self.produto][el][0] >= self.quantidade:
                        return redirect(url_for('transacaocompra', usuario=self.usuario, pror=self.produto, prer=el, qnt=self.quantidade))

                    elif oferta[self.produto][el][0] <= self.quantidade:

                        oferta[self.produto][el][0] -= self.quantidade
                        if oferta[self.produto][el][0] <= 0:
                            oferta[self.produto].pop(el)

                        credito[[oferta[self.produto].get(el)][1]] += el * self.quantidade
                        credito[self.usuario] -= el * self.quantidade
                        self.quantidade -= el[0]
                        Operacao.atualiza(self)
            else:
                if self.produto in deman:
                    deman[self.produto].update({self.preco: [self.quantidade, self.usuario]})
                else:
                    deman[self.produto] = {self.preco: [self.quantidade, self.usuario]}

                return jsonify({'resposta': 'pedido posto em espera'})
        elif self.tipo == 'venda':
            l = list(deman.get(self.produto, {'nao': ''}).keys())
            l.sort()
            for el in l:
                print(l)
                if el == 'nao':
                    print(deman)
                    if self.produto in oferta:
                        oferta[self.produto].update({self.preco: [self.quantidade, self.usuario]})
                    else:
                        oferta[self.produto] = {self.preco: [self.quantidade, self.usuario]}

                    return jsonify({'resposta': 'pedido posto em espera'})

                elif self.preco <= el:

                    if deman[self.produto][el][0] >= self.quantidade:
                        return redirect(url_for('transacaovenda', usuario=self.usuario, pror=self.produto, prer=el, qnt=self.quantidade))

                    elif deman[self.produto][el][0] < self.quantidade:

                        deman[self.produto][el][0] -= self.quantidade

                        if deman[self.produto][el][0] <= 0:
                            deman[self.produto].pop(el)

                        credito[self.usuario] += el * self.quantidade
                        credito[[deman[self.produto].get(el)][1]] -= el * self.quantidade
                        self.quantidade -= el[0]
                        Operacao.atualiza(self)

            else:
                if self.produto in oferta:
                    oferta[self.produto].update({self.preco: [self.quantidade, self.usuario]})
                else:
                    oferta[self.produto] = {self.preco: [self.quantidade, self.usuario]}

                return jsonify({'resposta': 'pedido posto em espera'})


