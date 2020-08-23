from flask import Flask
from flask_misaka import Misaka
from artigo import artigo
from admin_artigo import admin_artigo
from autenticacao import autenticacao
from dotenv import load_dotenv


app = Flask(__name__)
app.secret_key = b'\x1e\x08I\xfa\xbfl\xf7\x8fL\x82KW\xa9\x19\x1bW\x0b\x9f\x14~@\x9c\xedl'
app.register_blueprint(admin_artigo, url_prefix='/admin/artigo')
app.register_blueprint(artigo, url_prefix='/artigo')
app.register_blueprint(autenticacao, url_prefix='/autenticacao')

md = Misaka(fenced_code=True)
md.init_app(app)

if __name__ == '__main__':
    load_dotenv()
    app.run(debug=True)
