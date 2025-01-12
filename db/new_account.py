from flask import Flask
from db.models import Client, Account, Card, Credit, Transaction
from flask_sqlalchemy import SQLAlchemy
import random


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

with app.app_context():

    new_account = Account(
        account_nr = random.randint(15_0909_6666_0000_0000, 15_0909_6666_9999_9999),
        client_id = 1234,
        card_nr = random.randint(9999_6666_0000_0000, 9999_6666_9999_9999),
        account_type = 'test',
        balance = 0,
        currency = 'PLN'
    )

    db.session.add(new_account)
    db.session.commit()
    print("Dodano nowe konto")

  