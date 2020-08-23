from data import ArtigoData
from database_helper import query, factory_conexao, execute
from flask_paginate import Pagination, get_page_args
from flask import request, redirect, url_for
from pymysql import MySQLError
from flask_misaka import markdown


class ArtigoDominio:
    def listar(self, deletado=False):
        search = False
        q = request.args.get('q')
        page, per_page, offset = get_page_args(
            page_parameter="page", per_page_parameter="per_page"
        )
        params = None
        sql = "select * from artigo "
        sql_count = "select count(*) as total from artigo "
        where = ""
        if deletado:
            where += "where deletado = 1 "
        else:
            where += "where deletado = 0 "
        if q:
            search = True
            where += "and (titulo like %s or corpo like %s) "
            params = ("%" + q + "%", "%" + q + "%")
        sql += where
        sql_count += where
        sql += " limit {}, {};".format(offset, per_page)
        conexao = factory_conexao()
        artigos = []
        try:
            for registro in query(conexao, sql, params=params):
                artigo = ArtigoData()
                artigo.id_artigo = registro["id_artigo"]
                artigo.titulo = markdown(registro["titulo"])
                artigo.corpo = markdown(registro["corpo"])
                artigo.data_publicacao = registro["data_publicacao"]
                artigo.data_edicao = registro["data_edicao"]
                artigo.tags = registro["tags"]
                artigos.append(artigo)
            total = 0
            for registro in query(conexao, sql_count, params=params):
                total = registro['total']
        finally:
            conexao.close()
        pagination = Pagination(
            page=page,
            total=total,
            search=search,
            per_page=per_page,
            record_name="artigos",
            show_single_page=True,
            css_framework="bootstrap4",
        )
        return {
            "template": "index.html",
            "artigos": artigos,
            "page": page,
            "per_page": per_page,
            "pagination": pagination,
        }

    def cadastrar(self):
        titulo = request.form["titulo"]
        corpo = request.form["corpo"]
        if self._vazio(titulo):
            return redirect(url_for("admin_artigo.view_cadastra_artigo"))
        if self._vazio(corpo):
            return redirect(url_for("admin_artigo.view_cadastra_artigo"))
        if not self._corpo_maximo_minimo(corpo):
            return redirect(url_for("admin_artigo.view_cadastra_artigo"))
        if not self._titulo_maximo_minimo(titulo):
            return redirect(url_for("admin_artigo.view_cadastra_artigo"))
        sql = "insert into artigo (titulo, corpo) value (%s, %s)"
        conexao = factory_conexao()
        try:
            execute(conexao, sql, (titulo, corpo))
        except MySQLError as error:
            conexao.rollback()
            raise error
        finally:
            conexao.close()
        return redirect(url_for('artigo.view_listar'))

    def alterar(self, id_artigo):
        pass

    def apagar(self, id_artigo):
        pass

    def visualizar_artigo(self, id_artigo):
        conexao = factory_conexao()
        if not self._artigo_existe(id_artigo) or self._artigo_deletado(id_artigo):
            return {"template": 'indisponivel.html'}
        try:
            artigo = ArtigoData()
            for registro in query(
                    conexao, "select * from artigo where id_artigo = %s", (id_artigo,)
            ):
                artigo.titulo = markdown(registro["titulo"])
                artigo.corpo = markdown(registro["corpo"])
                artigo.id_artigo = registro["id_artigo"]
                artigo.data_publicacao = registro["data_publicacao"]
                artigo.data_edicao = registro["data_edicao"]
        finally:
            conexao.close()
        return {"template": "artigo_visualizar.html", "artigo": artigo}

    def _artigo_deletado(self, id_artigo):
        conexao = factory_conexao()
        try:
            for registro in query(
                    conexao, "select deletado from artigo where id_artigo = %s", (id_artigo,)
            ):
                return registro["deletado"] == 1
        finally:
            conexao.close()

    def _artigo_existe(self, id_artigo):
        conexao = factory_conexao()
        try:
            for registro in query(
                    conexao, "select count(*) as count from artigo where id_artigo = %s", (id_artigo,)
            ):
                return registro["count"] > 0
        finally:
            conexao.close()

    def _titulo_maximo_minimo(self, campo):
        return 10 <= len(campo) <= 100

    def _corpo_maximo_minimo(self, campo):
        return 50 <= len(campo) <= 1000000

    def _vazio(self, valor):
        return not valor or not valor.strip()
