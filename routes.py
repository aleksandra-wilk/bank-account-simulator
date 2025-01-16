from flask import redirect, render_template, request, session, url_for, flash
from app import app, db
from models import Client, Account, create_account_db, Card, Credit, Transaction
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
        # Zamiana numeru konta na string
        account.account_nr = str(account.account_nr)
        # Sformatowanie numeru konta ze spacjami 
        account.account_nr = f"{account.account_nr[:2]} {account.account_nr[2:6]} {account.account_nr[6:10]} {account.account_nr[10:14]} {account.account_nr[14:18]}"

    return render_template('products_accounts.html', accounts=accounts)


# Produkty - Konta
@app.route('/products/accounts/new', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        
        account_type = request.form.get('account_type')
        client_id = session.get('client_id')
        
        new_account = create_account_db(account_type=account_type, client_id=client_id)

        db.session.add(new_account)
        db.session.commit()

        return render_template('create_account.html', message="Konto założono pomyślnie."), 201

    elif request.method == 'GET':
        return render_template('create_account.html')


# Produkty - Karty
@app.route('/products/cards')
def products_cards():

    cards = db.session.query(Card).all()

    return render_template('products_cards.html', cards=cards)


# Produkty - Pożyczki
@app.route('/products/loans')
def products_loans():
    return render_template('products_loans.html')


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