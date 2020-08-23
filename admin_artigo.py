from flask import Blueprint
from artigo_dominio import ArtigoDominio
from flask import render_template
from autenticacao_dominio import login_obrigatorio

admin_artigo = Blueprint('admin_artigo', __name__)

artigo_negocio = ArtigoDominio()


@admin_artigo.route('/cadastro', methods=['GET'])
@login_obrigatorio
def view_cadastra_artigo():
    return render_template('novo_artigo.html')


@admin_artigo.route('/cadastrar', methods=['POST'])
@login_obrigatorio
def cadastrar():
    return artigo_negocio.cadastrar()


@admin_artigo.route('/editar/<id_artigo>', methods=['POST'])
def editar(id_artigo):
    return id_artigo
