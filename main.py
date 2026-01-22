import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 1. Pega a URL da variável de ambiente que configuramos no Render
# Se não houver variável (localmente), ele usa um sqlite para não dar erro
database_url = os.environ.get("DATABASE_URL")

if database_url:
    # 2. CORREÇÃO CRÍTICA: O Render dá "postgres://", o SQLAlchemy exige "postgresql://"
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Fallback para desenvolvimento local
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)

with app.app_context():
    db.create_all()  # Isso cria as tabelas automaticamente se elas não existirem


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)