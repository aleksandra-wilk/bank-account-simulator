from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import app, db
import random


class Client(db.Model):
    __tablename__ = 'clients'
    client_id = db.Column(Integer, primary_key=True, nullable=False)
    name = db.Column(String, nullable=False)
    surname = db.Column(String, nullable=False)
    email = db.Column(String, nullable=False, unique=True)
    password = db.Column(String, nullable=False)

    accounts = relationship('Account', back_populates='clients')

    def __repr__(self):
        return f"<Client(client_id={self.client_id}, name={self.name}, surname={self.surname}, email={self.email}, password={self.password})>"


class Account(db.Model):
    __tablename__ = 'accounts'
    account_nr = db.Column(Integer, primary_key=True, nullable=False)
    client_id = db.Column(Integer, ForeignKey('clients.client_id'), nullable=False)
    card_nr = db.Column(Integer, nullable=True)
    account_type = db.Column(String, nullable=False)
    balance = db.Column(Integer, default=0)
    currency = db.Column(String, nullable=False)

    clients = relationship('Client', back_populates='accounts')
    transactions = relationship('Transaction', back_populates='accounts')
    credits = relationship('Credit', back_populates='accounts')
    cards = relationship('Card', back_populates='accounts')

    def __repr__(self):
        return f"<Account(account_nr={self.account_nr}, client_id={self.client_id}, card_nr={self.card_nr}, account_type={self.account_type}),balance={self.balance}, currency={self.currency}>"

class Card(db.Model):
    __tablename__ = 'cards'
    card_nr = db.Column(Integer, primary_key=True, nullable=False)
    account_nr = db.Column(Integer, ForeignKey('accounts.account_nr'), nullable=False, unique=True)
    balance = db.Column(Integer, nullable=False)
    currency = db.Column(String, nullable=False)

    accounts = relationship('Account', back_populates='cards')

    def __repr__(self):
        return f"<Card(card_nr={self.card_nr}, account_nr={self.account_nr}, balance={self.balance}, currency={self.currency}>"


class Credit(db.Model):
    __tablename__ = 'credits'
    credit_id = db.Column(Integer, primary_key=True, nullable=False)
    account_nr = db.Column(Integer, ForeignKey('accounts.account_nr'), nullable=False)
    amount = db.Column(Integer, nullable=False)
    date = db.Column(DateTime, nullable=False, default=datetime.now)

    accounts = relationship('Account', back_populates='credits')

    def __repr__(self):
        return f"<Credit(credit_id={self.credit_id}, account_nr={self.account_nr}, amount={self.amount}, date={self.date})>"


class Transaction(db.Model):
    __tablename__ = 'transactions'
    transaction_id = db.Column(Integer, primary_key=True, nullable=False)
    account_nr = db.Column(Integer, ForeignKey('accounts.account_nr'), nullable=False)
    amount = db.Column(Integer, nullable=False)
    currency = db.Column(String, nullable=False)
    date = db.Column(DateTime, nullable=False, default=datetime.now().date)
    receiver_name = db.Column(String, nullable=False)
    receiver_account = db.Column(Integer, nullable=False)

    accounts = relationship('Account', back_populates='transactions')

    def __repr__(self):
        return f"<Transaction(account_nr={self.account_nr}, amount={self.amount}, currency={self.currency}, date={self.date}, receiver_name={self.receiver_name}, receiver_account={self.receiver_account}>"
    

def create_account_db(account_type, client_id, card_nr):
    
    if account_type == 'currency_eur':
        currency = 'EUR'
    elif account_type == 'currency_usd':
        currency = 'USD'
    else:
        currency = 'PLN'
    
    new_account = Account(
        account_nr = random.randint(15_0909_6666_0000_0000, 15_0909_6666_9999_9999),
        client_id = client_id,
        card_nr = card_nr,
        account_type = account_type,
        balance = 0,
        currency = currency
    )
    
    db.session.add(new_account)
    db.session.commit()
    
    return new_account


def create_card_db(account_nr, account_type, balance):
    
    account_type = account_type
    
    if account_type == 'currency_eur':
        currency = 'EUR'
    elif account_type == 'currency_usd':
        currency = 'USD'
    else:
        currency = 'PLN'
    
    new_card = Card(
        card_nr = random.randint(1155_0900_0000_0000, 1155_0900_9999_9999),
        account_nr = account_nr,
        balance = balance,
        currency = currency, 
    )
    
    db.session.add(new_card)
    db.session.commit()

    account = Account.query.filter(Account.account_nr == account_nr).first()
    if account:
        account.card_nr = new_card.card_nr
        db.session.commit()
    
    return new_card


def create_client_db(name, surname, email,password):
    
    new_client = Client(
            name = name,
            surname = surname,
            email = email,
            password = password,
    )
    
    db.session.add(new_client)
    db.session.commit()
    
    return new_client


def create_credit_db(account_nr, amount):
    
    new_credit = Credit(
        credit_id = random.randint(10000, 99999),
        account_nr = account_nr,
        amount = amount,
    )
    
    db.session.add(new_credit)
    db.session.commit()
    
    return new_credit


def create_transaction_db(account_nr, amount, currency, receiver_name, receiver_account):
    
    new_transaction = Transaction(
        account_nr = account_nr,
        amount = amount,
        currency = currency,
        receiver_name = receiver_name,
        receiver_account = receiver_account,
    )
    
    db.session.add(new_transaction)
    db.session.commit()
    
    return new_transaction


if __name__ == "__main__":
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Done")






