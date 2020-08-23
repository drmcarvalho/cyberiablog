from flask import Blueprint, render_template
from artigo_dominio import ArtigoDominio


artigo = Blueprint('artigo', __name__,
                   template_folder='templates',
                   static_folder='static')

artigo_dominio = ArtigoDominio()


@artigo.route("/<int:id_artigo>")
def view_artigo_visualizar(id_artigo):
    dictionary = artigo_dominio.visualizar_artigo(id_artigo)
    return render_template(
        dictionary["template"],
        artigo=dictionary["artigo"] if "artigo" in dictionary else None,
    )


@artigo.route('/listar')
def view_listar():
    dictionary = artigo_dominio.listar()
    return render_template(
        dictionary['template'],
        artigos=dictionary['artigos'],
        page=dictionary['page'],
        per_page=dictionary['per_page'],
        pagination=dictionary['pagination']
    )
