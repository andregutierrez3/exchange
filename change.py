
from basic import *
from flask import request
from flask_restful import Resource, Api

perfis = {}
deman = {}
oferta = {}
credito = {}

app = Flask(__name__)
api = Api(app)


class Inicio(Resource):
    def get(self):
        if request.args:
            u = request.args.get('usuario')
            s = request.args.get('senha')
            if u in list(perfis.keys()):
                return jsonify({'resposta': 'usuario ja existente'})

            else:
                perfis[u] = s
                credito[u] = 0
                return jsonify({"resposta": "Seu perfil foi criado"})

    def post(self):
        u = request.form.get('usuario')
        s = request.form.get('senha')

        if u in list(perfis.keys()):
            return jsonify({'resposta': 'usuario ja existente'})

        else:
            perfis[u] = s
            credito[u] = 0
            return jsonify({"resposta": "Seu perfil foi criado"})


class Cred(Resource):
    def get(self):
        usuario = request.args.get('usuario')
        return jsonify({'resposta': 'seu credito e {}'.format(credito[usuario])})

    def put(self):
        usuario = request.form.get('usuario')
        credito[usuario] = int(request.form.get('valor')) + int(credito[usuario])
        return jsonify({'resposta': 'seu credito e {}'.format(credito[usuario])})


class Login(Resource):

    def get(self):
        s = request.form.get('senha')
        dicio = {'tipo': request.form.get('operacao'), 'preco': request.form.get('preco'),
                 "quantidade": request.form.get('quantidade'),
                 "produto": request.form.get('produto'),
                 'usuario': request.form.get('usuario')}
        schema = OperacaoSchema()
        result = schema.load(dicio)
        info = result.data
        pprint(result.data)

        if perfis.get('usuario') != s:
            return jsonify({'resposta': 'INVALIDO'})
        elif info.tipo == 'compra' and (credito[info.usuario] < info.preco * info.quantidade):
            return 'E preciso mais credito'
        else:
            return info.atualiza()

    def post(self):
        s = request.form.get('senha')
        dicio = {'tipo': request.form.get('operacao'), 'preco': request.form.get('preco'),
                 "quantidade": request.form.get('quantidade'),
                 "produto": request.form.get('produto'),
                 'usuario': request.form.get('usuario')}
        schema = OperacaoSchema()
        result = schema.load(dicio)
        info = result.data
        pprint(result.data)

        if perfis.get('usuario') != s:
            return jsonify({'resposta': 'INVALIDO'})
        elif info.tipo == 'compra' and (credito[info.usuario] < info.preco * info.quantidade):
            return 'E preciso mais credito'
        else:
            return info.atualiza()

    def delete(self):
        s = request.form.get('senha')

        if perfis.get('usuario') != s:

            return jsonify({'resposta': 'INVALIDO'})

        else:
            return perfis.pop('usuario')


class Transacaocompra(Resource):
    def get(self):
        usuario = request.args.get('usuario')
        pror = request.args.get('pror')
        prer = request.args.get('prer')
        qnt = request.args.get('qnt')
        print(oferta[pror])
        oferta[pror][prer][0] = int(oferta[pror][prer][0]) - qnt

        if oferta[pror][prer][0] <= 0:
            oferta[pror].pop(prer)

        credito[oferta[pror.get(prer)][1]] += prer * qnt
        credito[usuario] -= prer * qnt

        return 'Transacao efetuada'


class Transacaovenda(Resource):
    def get(self):
        usuario = request.args.get('usuario')
        pror = request.args.get('pror')
        prer = request.args.get('prer')
        qnt = request.args.get('qnt')

        print(deman[pror])
        deman[pror][prer][0] = int(deman[pror][prer][0]) - qnt
        if deman[pror][prer][0] <= 0:
            deman[pror].pop(prer)
        credito[usuario] += prer * qnt
        credito[deman[pror.get(prer)][1]] -= prer * qnt

        return 'Transacao efetuada'


api.add_resource(Transacaovenda, '/Transacaovenda')
api.add_resource(Transacaocompra, '/Transacaocompra')
api.add_resource(Login, '/login')
api.add_resource(Cred, '/credito')
api.add_resource(Inicio, '/inicio')
app.run(debug=True)

