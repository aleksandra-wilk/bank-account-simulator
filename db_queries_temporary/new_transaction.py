from flask import Flask
from models import Client, Account, Card, Credit, Transaction
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

with app.app_context():

    new_transaction = Transaction(
        account_id = 123,
        amount = 234,
        currency = 'PLN',
        receiver_name = 'OLA',
        receiver_account = 123455,
    )

    db.session.add(new_transaction)
    db.session.commit()
    print("Dodano nową transakcję")



 

