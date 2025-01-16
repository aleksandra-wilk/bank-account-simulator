import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from flask import Flask
from models import Client, Account, Card, Credit, Transaction
from models import create_account_db, create_card_db, create_client_db, create_credit_db, create_transaction_db
from flask_sqlalchemy import SQLAlchemy
from app import db, app


choice = input("""DODAĆ DO TABELI - WYBIERZ 1 
WYŚWIETLIĆ TABELE - WYBIERZ 2\n""")

if choice == '1': 

    choice2 = input ("""CO CHCESZ DODAĆ? 
1 - NOWY KLIENT
2 - NOWE KONTO 
3 - NOWA KARTA 
4 - NOWY KREDYT
5 - NOWA TRANSAKCJA\n""")
    
    if choice2 == '1': 

        with app.app_context():
    
            create_client_db('Aleksandra', 'Wilk', 'awilk@wp.pl', 'haslo')
            clients = db.session.query(Client).all()

            print("DODANO NOWEGO KLIENTA")
            print(f"WSZYSCY KLIENCI: {clients}")

    elif choice2 == '2': 

        with app.app_context():
    
            create_account_db('current', 12345)
            accounts = db.session.query(Credit).all()

            print("DODANO NOWE KONTO")
            print(f"WSZYSTKIE KONTA: {accounts}")

    elif choice2 == '3': # Dokończyć

        with app.app_context():
    
            create_card_db(345678, 0)
            cards = db.session.query(Card).all()

            print("DODANO NOWĄ KARTĘ""")
            print(f"WSZYSTKIE KARTY: {cards}")

    elif choice2 == '4': 

        with app.app_context():
    
            create_credit_db(2345678, 70_000)
            credits = db.session.query(Credit).all()

            print("DODANO NOWY KREDYT""")
            print(f"WSZYSTKIE KREDTY: {credits}")

    elif choice2 == '5': 

        with app.app_context():
    
            create_transaction_db(1676716721, 500, 'PLN', 'Nadawca', 156156)
            transactions = db.session.query(Transaction).all()

            print("DODANO NOWĄ TRANSAKCJĘ""")
            print(f"WSZYSTKIE TRANSAKCJE: {transactions}")

elif choice == '2':


    choice2 = input ("""CO CHCESZ WYŚWIETLIĆ? 
1 - KLIENTÓW
2 - KONTA 
3 - KARTY 
4 - KREDYTY
5 - TRANSAKCJE\n""")
    
    if choice2 == '1': 

        with app.app_context():
    

            clients = db.session.query(Client).all()
            print(f"WSZYSCY KLIENCI: {clients}")

    elif choice2 == '2': 

        with app.app_context():
    
            accounts = db.session.query(Credit).all()
            print(f"WSZYSTKIE KONTA: {accounts}")

    elif choice2 == '3': 

        with app.app_context():
    
            cards = db.session.query(Card).all()
            print(f"WSZYSTKIE KARTY: {cards}")

    elif choice2 == '4': 

        with app.app_context():
    

            credits = db.session.query(Credit).all()
            print(f"WSZYSTKIE KREDTY: {credits}")

    elif choice2 == '5': 

        with app.app_context():
    
            transactions = db.session.query(Transaction).all()
            print(f"WSZYSTKIE TRANSAKCJE: {transactions}")

     