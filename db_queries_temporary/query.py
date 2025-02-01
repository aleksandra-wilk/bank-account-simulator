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
import random


choice = input("""
    CO CHCESZ ZROBIĆ?
    DODAĆ DO TABELI - WYBIERZ 1
    WYŚWIETLIĆ TABELE - WYBIERZ 2 \n
               """)

if choice == '1': 

    choice2 = input ("""
    CO CHCESZ DODAĆ? 
    1 - NOWY KLIENT
    2 - NOWE KONTO 
    3 - NOWA KARTA 
    4 - NOWY KREDYT
    5 - NOWA TRANSAKCJA
    6 - DOŁADUJ KONTO\n
                     """)
    
    if choice2 == '1': 

        with app.app_context():
    
            create_client_db('Aleksandra', 'Wilk', 'awilk@wp.pl', 'haslo')
            clients = db.session.query(Client).all()

            print("DODANO NOWEGO KLIENTA")
            print(f"WSZYSCY KLIENCI: \n{clients}")

    elif choice2 == '2': 

        with app.app_context():
    
            create_account_db('current', 12345)
            accounts = db.session.query(Credit).all()

            print("DODANO NOWE KONTO")
            print(f"WSZYSTKIE KONTA: \n{accounts}")

    elif choice2 == '3': # Dokończyć

        with app.app_context():
    
            random_account = random.randint(15_0909_6666_0000_0000, 15_0909_6666_9999_9999)
            
            create_card_db(random_account, 'current', 0)
            cards = db.session.query(Card).all()

            print("DODANO NOWĄ KARTĘ""")
            print(f"WSZYSTKIE KARTY: \n{cards}")

    elif choice2 == '4': 

        with app.app_context():
    
            create_credit_db(11_1160_8800_8977_2456, 70_000)
            credits = db.session.query(Credit).all()

            print("DODANO NOWY KREDYT""")
            print(f"WSZYSTKIE KREDTY: \n{credits}")

    elif choice2 == '5': 

        with app.app_context():
    
            create_transaction_db(account_nr=150909666619426836, amount=500, currency='PLN', receiver_name='Nadawca', receiver_account=158899000022220000, title='Tytuł')
            transactions = db.session.query(Transaction).all()

            print("DODANO NOWĄ TRANSAKCJĘ""")
            print(f"WSZYSTKIE TRANSAKCJE: \n{transactions}")

    elif choice2 == '6':

        with app.app_context():
    
            account = db.session.query(Account).first()
            account.balance += 100

            db.session.commit()

            print("DOŁADOWANO KONTO")



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
            print(f"WSZYSCY KLIENCI: \n{clients}")

    elif choice2 == '2': 

        with app.app_context():
    
            accounts = db.session.query(Credit).all()
            print(f"WSZYSTKIE KONTA: \n{accounts}")

    elif choice2 == '3': 

        with app.app_context():
    
            cards = db.session.query(Card).all()
            print(f"WSZYSTKIE KARTY: \n{cards}")

    elif choice2 == '4': 

        with app.app_context():
    
            credits = db.session.query(Credit).all()
            print(f"WSZYSTKIE KREDTY: \n{credits}")

    elif choice2 == '5': 

        with app.app_context():
    
            transactions = db.session.query(Transaction).all()
            print(f"WSZYSTKIE TRANSAKCJE: \n{transactions}")

     