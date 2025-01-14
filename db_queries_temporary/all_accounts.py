from flask import Flask
from models import db, Client, Account, Card, Credit, Transaction
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


with app.app_context():
    accounts = db.session.query(Account).all()
    print(accounts)

    for account in accounts:
        print(account.account_nr, account.balance, account.account_type, account.currency)


