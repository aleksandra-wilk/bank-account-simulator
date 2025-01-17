from flask import redirect, render_template, request, session, url_for, flash
from app import app, db
from models import Client, Account, Card, Credit, Transaction
from models import create_account_db, create_card_db, create_client_db, create_credit_db, create_transaction_db

import random

# Strona logowania
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        
        
        # Wstępnie zdefiniowany użytkownik
        LOGIN = "admin"
        PASSWORD = "admin"

        username = request.form.get('username')
        client_id = request.form.get('username')
        password = request.form.get('password')

        # Weryfikacja użytkownika
        if username == LOGIN and password == PASSWORD:
            # Logowanie udane - zapisanie użytkownika w sesji
            session['username'] = username
            session['client_id'] = client_id
            return redirect(url_for('home'))
        else:
            # Nieudane logowanie
            flash("Nieprawidłowa nazwa użytkownika lub hasło.", "danger")

    return render_template('login.html')


# Strona główna
@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))  # Użytkownik musi się zalogować


    return render_template('home_page.html', username=session['username'])


# Produkty - Konta
@app.route('/products/accounts', methods=['GET'])
def products_accounts():
    accounts = db.session.query(Account).all() 

    for account in accounts:
        account.account_nr = str(account.account_nr)
        account.account_nr = f"{account.account_nr[:2]} {account.account_nr[2:6]} {account.account_nr[6:10]} {account.account_nr[10:14]} {account.account_nr[14:18]}"

        if account.card_nr != None:
            account.card_nr = str(account.card_nr)
            account.card_nr = f"{account.card_nr[:4]} {account.card_nr[4:8]} {account.card_nr[8:12]} {account.card_nr[12:16]}"

    return render_template('products_accounts.html', accounts=accounts)


# Produkty - Założenie Konta
@app.route('/products/accounts/new', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        
        account_type = request.form.get('account_type')
        client_id = session.get('client_id')
        want_card = request.form.get('want_card')

        card_nr = None
        if want_card:
            card_nr = random.randint(1155_0900_0000_0000, 1155_0900_9999_9999)

        new_account = create_account_db(account_type, client_id, card_nr)

        db.session.add(new_account)
        db.session.commit()

        return render_template('create_account.html', message="Konto założono pomyślnie.")

    elif request.method == 'GET':
        return render_template('create_account.html')


# Produkty - Karty
@app.route('/products/cards', methods=['GET'])
def products_cards():

    cards = db.session.query(Card).all()

    for card in cards:
        card.account_nr = str(card.account_nr)
        card.account_nr = f"{card.account_nr[:2]} {card.account_nr[2:6]} {card.account_nr[6:10]} {card.account_nr[10:14]} {card.account_nr[14:18]}"

        card.card_nr = str(card.card_nr)
        card.card_nr = f"{card.card_nr[:4]} {card.card_nr[4:8]} {card.card_nr[8:12]} {card.card_nr[12:16]}"



    return render_template('products_cards.html', cards=cards)


# Produkty - Założenie Karty
@app.route('/products/cards/new', methods=['GET', 'POST'])
def create_card():
    if request.method == 'POST':
        
        account_nr = request.form.get('account_nr')

        account = db.session.query(Account).filter(Account.account_nr == account_nr).first()

        if account:  # Dodajemy sprawdzenie, czy konto zostało znalezione
            account_type = account.account_type
            balance = account.balance

            # Tworzymy kartę
            new_card = create_card_db(account_nr, account_type, balance)
            db.session.add(new_card)
            db.session.commit()
            
            return render_template('create_card.html', message='Karta założona pomyślnie.')
    
    elif request.method == 'GET':
        
        accounts = db.session.query(Account).filter(Account.card_nr == None).all()

        return render_template('create_card.html', accounts=accounts)


# Produkty - Pożyczki
@app.route('/products/loans')
def products_loans():

    credits = db.session.query(Credit).all()

    for credit in credits:
        credit.account_nr = str(credit.account_nr)
        credit.account_nr = f"{credit.account_nr[:2]} {credit.account_nr[2:6]} {credit.account_nr[6:10]} {credit.account_nr[10:14]} {credit.account_nr[14:18]}"

    return render_template('products_loans.html', credits=credits)


# Płatności - Przelew krajowy
@app.route('/payments/domestic')
def payments_domestic():
    return render_template('payments_domestic.html')


# Płatności - Przelew własny
@app.route('/payments/own')
def payments_own():
    return render_template('payments_own.html')


# Płatności - Przelew zagraniczny
@app.route('/payments/foreign')
def payments_foreign():
    return render_template('payments_foreign.html')


# Oferty
@app.route('/offers')
def offers():
    return render_template('offers.html')


# Zarządzanie finansami
@app.route('/financial_management')
def financial_management():
    return render_template('fin_man.html')


# Wylogowanie
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))