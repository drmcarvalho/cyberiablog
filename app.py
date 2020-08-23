from flask import Flask
from flask_misaka import Misaka
from artigo import artigo
from admin_artigo import admin_artigo
from autenticacao import autenticacao
from dotenv import load_dotenv


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/saaaffwwjjaJSQH'
app.register_blueprint(admin_artigo, url_prefix='/admin/artigo')
app.register_blueprint(artigo, url_prefix='/artigo')
app.register_blueprint(autenticacao, url_prefix='/autenticacao')

md = Misaka()
md.init_app(app)

if __name__ == '__main__':
    load_dotenv()
    app.run(debug=True)
