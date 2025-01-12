from flask import Flask
from models import Client, Account, Card, Credit, Transaction
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

with app.app_context():

    new_client = Client(
            client_id = 150999,
            name = 'ola',
            surname = 'w',
            email = 'ola@ola.pl',
            password = 'ola',
    )

    db.session.add(new_client)
    db.session.commit()
    print("Dodano nowego klienta")



