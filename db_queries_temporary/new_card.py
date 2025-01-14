from flask import Flask
from models import Client, Account, Card, Credit, Transaction
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

with app.app_context():

    new_card = Card(
        card_nr = 123456797,
        account_nr = 150909666673622,
        balance = 0,
        currency = 'PLN',
    )

    db.session.add(new_card)
    db.session.commit()
    print("Dodano nową kartę")



