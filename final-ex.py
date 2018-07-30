from flask import Flask, request, redirect, url_for, jsonify
from class_ex import Operacao

perfis = {}
deman = {}
oferta = {}
credito = {}

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@app.route('/criar', methods=['GET', 'POST'])
def inicio():

    if request.method == 'GET':

        if request.args:
            u = request.args.get('usuario')
            s = request.args.get('senha')

        else:
            return 'Bem Vindo a exchange, mande um post com senha e usuario para criar usuario ou um get com argumentos'

    else:
        u = request.form.get('usuario')
        s = request.form.get('senha')

    if u in list(perfis.keys()):
        return jsonify({'resposta': 'usuario ja existente'})

    else:
        perfis[u] = s
        credito[u] = 0
        return jsonify({"resposta": "Seu perfil foi criado"})


@app.route('/<usuario>/credito', methods=['GET', 'PUT'])
def cred(usuario):
    if request.method == 'GET':
        return jsonify({'resposta': 'seu credito e {}'.format(credito[usuario])})

    elif request.method == 'PUT':
        credito[usuario] = int(request.form.get('valor')) + int(credito[usuario])
        return jsonify({'resposta': 'seu credito e {}'.format(credito[usuario])})


@app.route('/<usuario>', methods=['POST', 'GET', 'DELETE'])
def login(usuario):

    if request.method in ['GET', 'POST']:
        s = request.form.get('senha')
        o = request.form.get('operacao')
        pro = request.form.get('produto')
        pre = int(request.form.get('preco'))
        qnt = int(request.form.get('quantidade'))

        if perfis.get(usuario) != s:
            return jsonify({'resposta': 'INVALIDO'})
        else:
            return redirect(url_for('operacao', usuario=usuario, operacao=o, pro=pro, pre=pre, qnt=qnt))

    elif request.method == 'DELETE':

        s = request.form.get('senha')

        if perfis.get(usuario) != s:

            return jsonify({'resposta': 'INVALIDO'})

        else:
            return perfis.pop(usuario)
    else:
        return jsonify({'resposta': 'Faca um post ou get para acessar usuario ou um delete para excluir'})


@app.route('/<usuario>/<operacao>/<pro>/<int:pre>/<int:qnt>', methods=['GET', 'POST'])
def operacao(usuario, operacao, pro, pre, qnt):

    if operacao == 'compra':

        if credito[usuario] < pre * qnt:
            return 'E preciso mais credito'
        else:
            op=Operacao(operacao, pre, qnt, pro, usuario)
            return op.atualiza()

    elif operacao == 'venda':
        op=Operacao(operacao, pre, qnt, pro, usuario)
        return op.atualiza()


@app.route('/<usuario>/compra/<pror>/<prer>/<qnt>/transacaocompra')
def transacaocompra(usuario, pror, prer, qnt):
    print(oferta[pror])
    oferta[pror][prer][0] = int(oferta[pror][prer][0])-qnt
    if oferta[pror][prer][0] <= 0:
        oferta[pror].pop(prer)

    credito[oferta[pror.get(prer)][1]] += prer * qnt
    credito[usuario] -= prer * qnt

    return 'Transacao efetuada'


@app.route('/<usuario>/venda/<pror>/<prer>/<qnt>/transacaovenda')
def transacaovenda(usuario, pror, prer, qnt):
    print(deman[pror])


    deman[pror][prer][0] = int(deman[pror][prer][0])-qnt
    if deman[pror][prer][0] <= 0:
        deman[pror].pop(prer)
    credito[usuario] += prer * qnt
    credito[deman[pror.get(prer)][1]] -= prer * qnt

    return 'Transacao efetuada'


app.run(debug=True)

