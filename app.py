from flask import Flask
from flask_misaka import Misaka
from artigo import artigo
from admin_artigo import admin_artigo
from autenticacao import autenticacao
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
app.register_blueprint(admin_artigo, url_prefix='/admin/artigo')
app.register_blueprint(artigo, url_prefix='/artigo')
app.register_blueprint(autenticacao, url_prefix='/autenticacao')

md = Misaka(fenced_code=True)
md.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
