from flask import Flask
from models import db, Client, Account, Card, Credit, Transaction
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


with app.app_context():
    cards = db.session.query(Card).all()

    for card in cards:
        print(card.card_nr, card.account_nr, card.balance)


  