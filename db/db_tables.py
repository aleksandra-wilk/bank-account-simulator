from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Client(Base):
    __tablename__ = 'clients'
    client_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

    accounts = relationship('Account', back_populates='clients')


class Account(Base):
    __tablename__ = 'accounts'
    account_nr = Column(Integer, primary_key=True, nullable=False)
    client_id = Column(Integer, ForeignKey('clients.client_id'), nullable=False)
    card_nr = Column(Integer)
    account_type = Column(String, nullable=False)
    balance = Column(Integer, nullable=False)
    currency = Column(String, nullable=False)

    clients = relationship('Client', back_populates='accounts')
    transactions = relationship('Transaction', back_populates='accounts')
    credits = relationship('Credit', back_populates='accounts')


class Card(Base):
    __tablename__ = 'cards'
    card_nr = Column(Integer, primary_key=True, nullable=False)
    account_nr = Column(Integer, nullable=False)
    balance = Column(Integer, nullable=False)
    currency = Column(String, nullable=False)

    accounts = relationship('Account')


class Credit(Base):
    __tablename__ = 'credits'
    credit_id = Column(Integer, primary_key=True)
    account_nr = Column(Integer, ForeignKey('accounts.account_nr'))
    amount = Column(Integer)
    date = Column(DateTime)

    accounts = relationship('Account', back_populates='credits')


class Transaction(Base):
    __tablename__ = 'transactions'
    transaction_id = Column(Integer, primary_key=True, nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.account_id'), nullable=False)
    amount = Column(Integer, nullable=False)
    currency = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    receiver_name = Column(String, nullable=False)
    receiver_account = Column(Integer, nullable=False)

    accounts = relationship('Account', back_populates='transactions')






