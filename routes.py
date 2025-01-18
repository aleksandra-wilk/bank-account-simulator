from flask import redirect, render_template, request, session, url_for, flash
from app import app, db
from models import Client, Account, Card, Credit, Transaction
from models import create_account_db, create_card_db, create_client_db, create_credit_db, create_transaction_db
import math import pow

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

        if account:  
            account_type = account.account_type
            balance = account.balance

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
@app.route('/offers', methods=['GET'])
def offers():
    return render_template('offers.html')

# Pożyczka
@app.route('/loan', methods=['GET', 'POST'])
def loan():
    if request.method == 'POST':
        # Pobranie danych z formularza
        amount = float(request.form.get('amount'))
        months = int(request.form.get('months'))
        insurance = 'insurance' in request.form  # Checkbox dla ubezpieczenia

        # Stałe parametry
        annual_interest_rate = 0.05  # Roczna stopa procentowa (5%)
        monthly_interest_rate = annual_interest_rate / 12

        # Prowizja (założmy 3% kwoty pożyczki)
        commission_rate = 0.03
        commission_amount = amount * commission_rate

        # Koszt ubezpieczenia (opcjonalny 2% kwoty pożyczki)
        insurance_cost = amount * 0.02 if insurance else 0

        # Obliczenie raty miesięcznej (formuła annuitetowa)
        monthly_payment = (amount * monthly_interest_rate) / (1 - pow(1 + monthly_interest_rate, -months))

        # Całkowity koszt odsetek
        total_cost = monthly_payment * months

        # Całkowity koszt z wszystkimi opłatami
        total_cost_with_fees = total_cost + insurance_cost + commission_amount

        # Obliczenie RRSO iteracyjnie
        def calculate_rrso(amount, monthly_payment, months, insurance_cost, commission_amount):
            guess_rate = 0.1  
            tolerance = 1e-7  
            max_iterations = 100  

            for _ in range(max_iterations):

                npv = sum([monthly_payment / pow(1 + guess_rate, n) for n in range(1, months + 1)])
                npv += (insurance_cost + commission_amount) / (1 + guess_rate)
                npv -= amount

                derivative = sum([-n * monthly_payment / pow(1 + guess_rate, n + 1) for n in range(1, months + 1)])
                derivative += -(insurance_cost + commission_amount) / pow(1 + guess_rate, 2)

                if abs(derivative) < 1e-10:  
                    break
                new_guess_rate = guess_rate - npv / derivative

                if abs(new_guess_rate - guess_rate) < tolerance:
                    guess_rate = new_guess_rate
                    break

                guess_rate = new_guess_rate

            return guess_rate * 12 * 100

        rrso = calculate_rrso(amount, monthly_payment, months, insurance_cost, commission_amount)

        # Dane pożyczki
        loan_data = {
            'amount': amount,
            'months': months,
            'monthly_payment': monthly_payment,
            'total_cost': total_cost,
            'insurance_cost': insurance_cost,
            'commission_amount': commission_amount,
            'total_cost_with_fees': total_cost_with_fees,
            'rrso': rrso
        }

        # Wyświetlenie wyników w loan_confirmation.html
        return render_template('loan_confirmation.html', loan_data=loan_data)

    return render_template('loan.html')


# Zarządzanie finansami
@app.route('/financial_management')
def financial_management():
    return render_template('fin_man.html')


# Wylogowanie
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
