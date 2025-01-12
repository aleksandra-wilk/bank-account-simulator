from flask import Flask
from models import db, Client, Account, Card, Credit, Transaction
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


with app.app_context():
    clients = db.session.query(Client).all()

    for client in clients:
        print(client.client_id, client.name, client.password)
