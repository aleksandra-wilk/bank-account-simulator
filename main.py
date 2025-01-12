from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from db.models import db, Client, Account, Card, Credit, Transaction
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
import random


def create_app():


    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    

    # Klucz do sesji
    app.secret_key = "your_secret_key"

    # Wstępnie zdefiniowany użytkownik
    LOGIN = "admin"
    PASSWORD = "admin"


    # Strona logowania
    @app.route('/', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
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
            new_account = Account(
                account_nr = random.randint(15_0909_6666_0000_0000, 15_0909_6666_9999_9999),
                client_id = session['client_id'],
                card_nr = random.randint(9999_6666_0000_0000, 9999_6666_9999_9999),
                account_type = request.form.get('account_type'),
                balance = 0,
                currency = 'PLN'
            )

            db.session.add(new_account)
            db.session.commit()
            print("Dodano nowe konto")

            return render_template('create_account.html', message="Konto założono pomyślnie.")

        return render_template('create_account.html')
    

    # Produkty - Karty
    @app.route('/products/cards')
    def products_cards():
        return render_template('products_cards.html')


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
    

    return app, db


if __name__ == "__main__":


    app, db = create_app()
    with app.app_context():  # Kontekst aplikacji jest wymagany do pracy z bazą danych
        db.create_all() 
    app.run(debug=True)
