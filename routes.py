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

# Przelew Krajowy
@app.route('/payments/domestic', methods=['GET', 'POST'])
def payments_domestic():
    if request.method == 'POST':
        # Pobranie danych wpisanych przez użytkownika
        sender_account = request.form.get('sender_account').replace(' ', '')
        receiver_account = request.form.get('receiver_account').replace(' ', '')
        receiver_name = request.form.get('receiver_name')
        amount = float(request.form.get('amount', 0))
        title = request.form.get('title', "Przelew krajowy")

        # Weryfikacja istnienia konta nadawcy
        sender = db.session.query(Account).filter_by(account_nr=sender_account).first()
        if not sender:
            flash("Podane konto nadawcy nie istnieje.", "danger")
            return redirect(url_for('payments_domestic'))

        # Sprawdzenie czy na koncie znajdują się wystarczające środki
        if sender.balance < amount:
            flash("Brak wystarczających środków na koncie.", "danger")
            return redirect(url_for('payments_domestic'))

        # Zmniejszenie salda
        sender.balance -= amount

        # Dodanie transakcji do bazy danych
        new_transaction = (Transaction
            (
            account_nr=sender.account_nr,
            amount=amount,
            currency='PLN',
            receiver_name=receiver_name,
            receiver_account=receiver_account,
            transfer_title = title
            ))

        db.session.add(new_transaction)
        db.session.commit()

        # Po zatwierdzeniu transakcji, zapisujemy zmiany w koncie
        db.session.commit()

        # Wyświetlenie informacji na stronie o wykonanym przelewie
        flash("Przelew wykonano pomyślnie.", "success")
        return redirect(url_for('payments_domestic'))

    # Pobieranie kont użytkownika z bazy danych
    accounts = db.session.query(Account).filter_by(client_id=session.get('client_id')).all()
    return render_template('payments_domestic.html', accounts=accounts)


# Płatności - Przelew własny
@app.route('/payments/own', methods=['GET', 'POST'])
def payments_own():
    # Pobranie kont użytkownika
    user_id = session.get('client_id') #Pobieranie id zalogowanego użytkownika
    accounts = Account.query.filter_by(client_id=user_id).all() #Pobranie z bazy wszystkich kont zalogowanego użutkownika

    if request.method == 'POST':
        # Pobieranie danych z formularza
        sender_account_nr = request.form.get('sender_account') #Konto, z którego wysyłamy przelew
        receiver_account_nr = request.form.get('receiver_account') #Konto, na które wysyłamy przelew
        amount = float(request.form.get('amount', 0)) #Kwota przelewu
        title = request.form.get('title', 'Przelew Własny')

        # Konto nadawcy i odbiorcy nie może być takie samo
        if sender_account_nr == receiver_account_nr:
            flash("Nie można wysłać przelewu na to samo konto.", "danger")
            return render_template('payments_own.html', accounts=accounts)

        # Pobieranie kont z bazy danych i sprawdzenie czy należą do użytkownika
        sender_account = Account.query.filter_by(account_nr=sender_account_nr, client_id=user_id).first()
        receiver_account = Account.query.filter_by(account_nr=receiver_account_nr, client_id=user_id).first()

        # Sprawdzenie salda konta nadawcy
        if sender_account.balance < amount:
            flash("Brak wystarczających środków na koncie nadawcy.", "danger")
            return render_template('payments_own.html', accounts=accounts)

        # Przetwarzanie przelewu
        sender_account.balance -= amount #Odjęcie kwoty z konta, z którego przelewamy
        receiver_account.balance += amount #Dodanie kwoty do konta, na które przelewamy

        # Dodanie transakcji do bazy danych
        new_transaction = Transaction(
            account_nr=sender_account_nr, #Numer konta, z którego wysłano przelew
            amount=amount,  #Kwota
            currency=sender_account.currency, #Waluta
            receiver_name="Odbiorca", #Nazwa odbiorcy
            receiver_account=receiver_account_nr, #Numer konta odbiorcy
            transfer_title = title
        )
        db.session.add(new_transaction) #Dodanie do bazy danych

        # Zatwierdzenie zmian w bazie danych
        db.session.commit()

        flash("Przelew wykonano pomyślnie!", "success")
        return redirect(url_for('payments_own'))

    return render_template('payments_own.html', accounts=accounts)


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