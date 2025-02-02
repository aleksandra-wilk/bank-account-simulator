from flask import redirect, render_template, request, session, url_for, flash, jsonify
from decimal import Decimal
from app import app, db
from models import Client, Account, Card, Credit, Transaction
from models import create_account_db, create_card_db, create_client_db, create_credit_db, create_transaction_db
from math import pow
import random
import pandas as pd
from datetime import datetime, timedelta


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
@app.route('/home', methods=['GET'])
def home():
    user_id = session.get('client_id')

    # Pobranie wszystkich kont użytkownika
    accounts = Account.query.filter_by(client_id=user_id).all()

    # Mapa nazw typów kont
    account_type_map = {
        'current': 'Konto Bieżące',
        'savings': 'Konto Oszczędnościowe',
        'currency_eur': 'Konto Walutowe (EUR)',
        'currency_usd': 'Konto Walutowe (USD)'
    }

    # Wybór konta domyślnego (konto bieżące) lub pierwsze dostępne konto
    selected_account = next((acc for acc in accounts if acc.account_type == 'current'), accounts[0]) if accounts else None

    # Pobranie historii transakcji dla użytkownika (ostatnie 10 transakcji)
    transactions = Transaction.query.filter(Transaction.account_nr.in_([acc.account_nr for acc in accounts])).order_by(Transaction.date.desc()).limit(10).all() if accounts else []

    # Obsługa zmiany konta przez użytkownika
    selected_account_nr = request.args.get('account_nr')
    if selected_account_nr:
        selected_account = Account.query.filter_by(account_nr=selected_account_nr, client_id=user_id).first()

    return render_template('home_page.html', accounts=accounts, selected_account=selected_account, transactions=transactions, account_type_map=account_type_map)


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

        if account and account.card_nr is None: 
            account_type = account.account_type
            balance = account.balance
            new_card = create_card_db(account_nr, account_type, balance)
            account.card_nr = new_card.card_nr

            flash("Karta założona pomyślnie.", "success")
            return redirect(url_for('create_card'))

    accounts = db.session.query(Account).filter(Account.card_nr == None).all()
    return render_template('create_card.html', accounts=accounts)


# Oferty - Dodanie kredytu
@app.route('/products/loan/new', methods=['GET', 'POST'])
def create_credit():
    if request.method == 'POST':
        amount = request.form.get('amount', type=float)  

        account = db.session.query(Account).filter(Account.card_nr != None).first()

        if not account:
            flash("Nie znaleziono dostępnego konta do przypisania kredytu.", "danger")
            return redirect(url_for('create_credit'))

        create_credit_db(account.account_nr, amount) 

        flash("Kredyt został pomyślnie założony.", "success")
        return redirect(url_for('loan'))

    return render_template('loan.html')



# Produkty - Pożyczki
@app.route('/products/loans')
def products_loans():

    credits = db.session.query(Credit).all()

    for credit in credits:
        credit.account_nr = str(credit.account_nr)
        credit.account_nr = f"{credit.account_nr[:2]} {credit.account_nr[2:6]} {credit.account_nr[6:10]} {credit.account_nr[10:14]} {credit.account_nr[14:18]}"

    return render_template('products_loans.html', credits=credits)

# Kursy walutowe
def get_exchange_rate(from_currency, to_currency):
    if from_currency == to_currency:
        return Decimal(1.0)

    exchange_rates = {
        ('PLN', 'EUR'): Decimal('0.24'),
        ('EUR', 'PLN'): Decimal('4.2'),
        ('USD', 'PLN'): Decimal('4.0'),
        ('PLN', 'USD'): Decimal('0.25'),
        ('EUR', 'USD'): Decimal('1.1'),
        ('USD', 'EUR'): Decimal('0.91')
    }

    exchange_rate = exchange_rates.get((from_currency, to_currency))
    return exchange_rate


# Płatności - Przelew Krajowy
@app.route('/payments/domestic', methods=['GET', 'POST'])
def payments_domestic():
    if request.method == 'POST':
        # Pobranie danych wpisanych przez użytkownika
        sender_account_nr = request.form.get('sender_account').replace(' ', '')
        receiver_account_nr = request.form.get('receiver_account').replace(' ', '')
        receiver_name = request.form.get('receiver_name')
        amount = float(request.form.get('amount', 0))
        title = request.form.get('title', "Przelew krajowy")

        # Weryfikacja istnienia konta nadawcy
        sender = db.session.query(Account).filter_by(account_nr=sender_account_nr).first()
        if not sender:
            flash("Podane konto nadawcy nie istnieje.", "danger")
            return redirect(url_for('payments_domestic'))

        # Sprawdzenie czy na koncie znajdują się wystarczające środki
        if sender.balance < amount:
            flash("Brak wystarczających środków na koncie.", "danger")
            return redirect(url_for('payments_domestic'))

        # Zmniejszenie salda
        amount = Decimal(amount)
        sender.balance -= amount

        # Dodanie transakcji do bazy danych
        new_transaction = (Transaction
            (
            account_nr = sender.account_nr,
            amount = amount,
            currency = sender.currency,
            receiver_name = receiver_name,
            receiver_account = receiver_account_nr,
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
    user_id = session.get('client_id') #identyfikator zalogowanego użytkownika
    accounts = Account.query.filter_by(client_id=user_id).all() #Szukamy kont powiązanch

    if request.method == 'POST':
        sender_account_nr = request.form.get('sender_account')
        receiver_account_nr = request.form.get('receiver_account')
        amount = Decimal(request.form.get('amount', 0))
        title = request.form.get('title', 'Przelew Własny')

        #Sprawdzenie czy nie przelewamy na to samo konto
        if sender_account_nr == receiver_account_nr:
            flash("Nie można wysłać przelewu na to samo konto.", "danger")
            return render_template('payments_own.html', accounts=accounts)

        #Pobranie konta odbiorcy i nadawcy oraz sprawdzenie czy należą do zalogowanego użytkownika
        sender_account = Account.query.filter_by(account_nr=sender_account_nr, client_id=user_id).first()
        receiver_account = Account.query.filter_by(account_nr=receiver_account_nr, client_id=user_id).first()

        #Sprawdzenie salda
        if sender_account.balance < amount:
            flash("Brak wystarczających środków na koncie nadawcy.", "danger")
            return render_template('payments_own.html', accounts=accounts)

        #Pobranie walut jakie są przypisane do konta
        sender_currency = sender_account.currency
        receiver_currency = receiver_account.currency

        # Jeśli waluty są różne, robimy przewalutowanie
        if sender_currency != receiver_currency:
            exchange_rate = get_exchange_rate(sender_currency, receiver_currency)

            if exchange_rate is None:
                flash("Błąd: nie można pobrać kursu wymiany dla podanej pary walut.", "danger")
                return render_template('payments_own.html', accounts=accounts)

            converted_amount = (amount * exchange_rate).quantize(Decimal('0.01')) #Przewalutowanie i zaokrąglenie
        else:
            converted_amount = amount

        # Przetwarzanie przelewu
        sender_account.balance -= amount
        receiver_account.balance += converted_amount

        # Dodanie transakcji do bazy danych
        new_transaction = Transaction(
            account_nr=sender_account_nr,
            amount=amount,
            currency=sender_currency,
            receiver_name="Przelew Własny",
            receiver_account=receiver_account_nr,
            transfer_title=title
        )
        db.session.add(new_transaction)
        db.session.commit()

        flash(f"Przelew wykonano pomyślnie! Przeliczona kwota: {converted_amount} {receiver_currency}", "success")
        return redirect(url_for('payments_own'))

    return render_template('payments_own.html', accounts=accounts)

# Płatności - Przelew zagraniczny
@app.route('/payments/foreign', methods=['GET', 'POST'])
def payments_foreign():
    if request.method == 'POST':
        sender_account_nr = request.form.get('sender_account')
        receiver_account_nr = request.form.get('receiver_account')
        receiver_name = request.form.get('receiver_name')
        amount = float(request.form.get('amount', 0))
        currency = request.form.get('currency')
        title = request.form.get('title', "Przelew Zagraniczny")

        #Pobranie informacji o walucie, z którego wysyłamy przelew
        sender = db.session.query(Account).filter_by(account_nr=sender_account_nr).first()
        sender_account = sender.currency

        # odjęcię kwoty z konta nadawcy
        exchange_rate = get_exchange_rate(sender_account, currency)  # Kurs walut
        amount = Decimal(amount)
        converted_amount = amount / exchange_rate
        sender.balance -= converted_amount

        #Sprawdzanie salda nadawcy (uwzględniając przewalutowanie)
        if sender.balance < amount:
            flash("Brak wystarczających środków na koncie.", "danger")
            return redirect(url_for('payments_foreign'))

        #Zapisanie transakcji w bazie danych
        new_transaction = Transaction(
            account_nr=sender.account_nr,
            amount=amount,
            currency=currency,
            receiver_name=receiver_name,
            receiver_account=receiver_account_nr,
            transfer_title=title
        )

        db.session.add(new_transaction)
        db.session.commit()

        flash("Przelew zagraniczny wykonano pomyślnie.", "success")
        return redirect(url_for('payments_foreign'))

    accounts = db.session.query(Account).filter_by(client_id=session.get('client_id')).all()
    return render_template('payments_foreign.html', accounts=accounts, currencies=['PLN', 'EUR', 'USD'])


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


def add_sample_transactions():
    if Transaction.query.count() == 0:
        categories = [
            ("Biedronka", "Zakupy spożywcze"),
            ("Media Markt", "Sprzęt elektroniczny"),
            ("Rossmann", "Kosmetyki"),
            ("Netflix", "Subskrypcja"),
            ("Orlen", "Paliwo"),
            ("KFC", "Jedzenie"),
            ("Empik", "Książki"),
            ("Spotify", "Muzyka"),
        ]
        incomes = [
            ("Pracodawca", "Wypłata"),
            ("Freelance", "Zlecenie")
        ]

        sample_transactions = []

        for month in range(1, 13):  # 12 ostatnich miesięcy
            for i in range(8):  # 8 wydatków
                days_offset = random.randint(0, 29)  # Losowy dzień w miesiącu
                amount = round(random.uniform(10, 500), 2)  # Zakres wydatków 10 - 500 
                
                sample_transactions.append(Transaction(
                    account_nr=10000 + i + month,
                    amount=Decimal(-amount), 
                    currency='PLN',
                    date=datetime.now() - timedelta(days=days_offset + (month - 1) * 30),
                    receiver_name=categories[i % len(categories)][0],
                    receiver_account=random.randint(10000, 99999),
                    transfer_title=categories[i % len(categories)][1]
                ))

            for i in range(2):  # 2 przychody
                amount = round(random.uniform(7000, 11000), 2)  # Zakres przychodów 7000 - 11 000
                
                sample_transactions.append(Transaction(
                    account_nr=20000 + i + month,
                    amount=Decimal(amount),  
                    currency='PLN',
                    date=datetime.now() - timedelta(days=random.randint(0, 29) + (month - 1) * 30),
                    receiver_name=incomes[i][0],
                    receiver_account=random.randint(10000, 99999),
                    transfer_title=incomes[i][1]
                ))

        db.session.bulk_save_objects(sample_transactions)
        db.session.commit()

        print("Dodano przykładowe transakcje.")


# Route do analizy finansowej
@app.route('/financial_management', methods=['GET'])
def financial_management():
    add_sample_transactions()
    return render_template('fin_man.html')


# API do pobierania analizy finansowej
@app.route('/get_financial_data', methods=['POST'])
def get_financial_data():
    try:
        months = int(request.json.get('months', 3)) 
        start_date = datetime.now() - timedelta(days=months * 30)
        transactions = Transaction.query.filter(Transaction.date >= start_date).all()

        # Konwersja do DataFrame
        df = pd.DataFrame([
            {
                'date': t.date,
                'amount': float(t.amount),  # Konwersja Decimal - float
                'currency': t.currency
            } for t in transactions
        ])

        if df.empty:
            return jsonify({'income': 0, 'expenses': 0})

        # Oblicza sumę przychodów (amount > 0) i wydatków (amount < 0)
        total_income = df[df['amount'] > 0]['amount'].sum()
        total_expenses = df[df['amount'] < 0]['amount'].sum()

        return jsonify({'income': total_income, 'expenses': abs(total_expenses)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Wylogowanie
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
