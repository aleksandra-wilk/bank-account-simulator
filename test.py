from flask import Flask
from db.models import db, Client, Account, Card, Credit, Transaction
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

def products_accounts():
    # Aktywujemy kontekst aplikacji
    with app.app_context():
        accounts = db.session.query(Account).all()
        print(accounts)

products_accounts()

  