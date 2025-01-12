from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class Client(db.Model):
    __tablename__ = 'clients'
    client_id = db.Column(Integer, primary_key=True, nullable=False)
    name = db.Column(String, nullable=False)
    surname = db.Column(String, nullable=False)
    email = db.Column(String, nullable=False, unique=True)
    password = db.Column(String, nullable=False)

    accounts = relationship('Account', back_populates='clients')


class Account(db.Model):
    __tablename__ = 'accounts'
    account_nr = db.Column(Integer, primary_key=True, nullable=False)
    client_id = db.Column(Integer, ForeignKey('clients.client_id'), nullable=False)
    card_nr = db.Column(Integer)
    account_type = db.Column(String, nullable=False)
    balance = db.Column(Integer, default=0)
    currency = db.Column(String, nullable=False)

    clients = relationship('Client', back_populates='accounts')
    transactions = relationship('Transaction', back_populates='accounts')
    credits = relationship('Credit', back_populates='accounts')
    cards = relationship('Card', back_populates='accounts')

    def __repr__(self):
        return f"<Account(account_nr={self.account_nr}, client_id={self.client_id}, account_type={self.account_type})>"


class Card(db.Model):
    __tablename__ = 'cards'
    card_nr = db.Column(Integer, primary_key=True, nullable=False)
    account_nr = db.Column(Integer, ForeignKey('accounts.account_nr'), nullable=False, unique=True)
    balance = db.Column(Integer, nullable=False)
    currency = db.Column(String, nullable=False)

    accounts = relationship('Account', back_populates='cards')


class Credit(db.Model):
    __tablename__ = 'credits'
    credit_id = db.Column(Integer, primary_key=True, nullable=False)
    account_nr = db.Column(Integer, ForeignKey('accounts.account_nr'), nullable=False)
    amount = db.Column(Integer, nullable=False)
    date = db.Column(DateTime, nullable=False, default=datetime.now)

    accounts = relationship('Account', back_populates='credits')


class Transaction(db.Model):
    __tablename__ = 'transactions'
    transaction_id = db.Column(Integer, primary_key=True, nullable=False)
    account_id = db.Column(Integer, ForeignKey('accounts.account_nr'), nullable=False)
    amount = db.Column(Integer, nullable=False)
    currency = db.Column(String, nullable=False)
    date = db.Column(DateTime, nullable=False, default=datetime.now)
    receiver_name = db.Column(String, nullable=False)
    receiver_account = db.Column(Integer, nullable=False)

    accounts = relationship('Account', back_populates='transactions')






