import functools
from werkzeug.security import check_password_hash
from database_helper import query, factory_conexao
from data import UsuarioData
from flask import request, session, g, redirect, url_for


class AutenticacaoDominio:
    def autenticar(self):
        email = request.form["email"]
        senha = request.form["senha"]
        conexao = factory_conexao()
        usuario = UsuarioData()
        try:
            for registro in query(
                    conexao, "select id, email, senha from usuario where email = %s", params=(email,)
            ):
                usuario.id = registro["id"]
                usuario.email = registro["email"]
                usuario.senha = registro["senha"]
        finally:
            conexao.close()
        if not usuario.email or not check_password_hash(usuario.senha, senha):
            return redirect(url_for("autenticacao.view_login"))
        session.clear()
        session["id_usuario"] = usuario.id
        return redirect(url_for('artigo.view_listar'))

    def logout(self):
        session.clear()
        return redirect(url_for('artigo.view_listar'))

    def obter_usuario(self, id_usuario):
        conexao = factory_conexao()
        usuario = UsuarioData()
        try:
            for registro in query(conexao, "select nome from usuario where id = %s", (id_usuario,)):
                usuario.nome = registro["nome"]
        finally:
            conexao.close()
        return usuario


def login_obrigatorio(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.usuario is None:
            return redirect(url_for("autenticacao.aviso"))
        return view(**kwargs)
    return wrapped_view
