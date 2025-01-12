from flask import Flask
from models import db, Client, Account, Card, Credit, Transaction
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


with app.app_context():
    transactions = db.session.query(Transaction).all()

    for transaction in transactions:
        print(transaction.transaction_id, transaction.amount, transaction.date)
