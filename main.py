from fekepinterest import app, database
from flask import Flask
from flask_cors import CORS



""" if __name__ == '__main__':
   database, app.run(debug=True) """
CORS(app) # Isso libera o acesso para o seu frontend

app = Flask(__name__)
CORS(app) # Isso libera o acesso para o seu frontend