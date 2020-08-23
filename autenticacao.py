from flask import Blueprint, render_template, session, g
from autenticacao_dominio import AutenticacaoDominio

autenticacao = Blueprint('autenticacao', __name__,
                         template_folder='templates',
                         static_folder='static')

autenticacao_dominio = AutenticacaoDominio()


@autenticacao.before_app_request
def load_logged_in_user():
    id_usuario = session.get('id_usuario')
    if id_usuario is None:
        g.usuario = None
    else:
        usuario = autenticacao_dominio.obter_usuario(id_usuario)
        g.usuario = usuario.nome


@autenticacao.route('/login', methods=['GET'])
def view_login():
    return render_template('login.html')


@autenticacao.route('/autenticar', methods=['POST'])
def autenticar():
    return autenticacao_dominio.autenticar()


@autenticacao.route('/logout')
def logout():
    return autenticacao_dominio.logout()


@autenticacao.route('/aviso', methods=['GET'])
def aviso():
    return 'Voce nao tem permissao para acessar esta pagina'
