from flask import Flask, render_template, request, redirect, url_for, session, flash


app = Flask(__name__)
app.secret_key = "your_secret_key"  # Klucz do sesji


# Wstępnie zdefiniowany użytkownik
LOGIN = "admin"
PASSWORD = "admin"


# Strona logowania
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Weryfikacja użytkownika
        if username == LOGIN and password == PASSWORD:
            # Logowanie udane - zapisanie użytkownika w sesji
            session['username'] = username
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

    return render_template('base.html', content_file="home_page.html", username=session['username'])



# Produkty - Konta
@app.route('/products/accounts')
def products_accounts():
    return render_template('base.html', content_file='products_accounts.html')


# Produkty - Karty
@app.route('/products/cards')
def products_cards():
    return render_template('base.html', content_file='products_cards.html')


# Produkty - Pożyczki
@app.route('/products/loans')
def products_loans():
    return render_template('base.html', content_file='products_loans.html')


# Płatności - Przelew krajowy
@app.route('/payments/domestic')
def payments_domestic():
    return render_template('base.html', content_file='payments_domestic.html')


# Płatności - Przelew własny
@app.route('/payments/own')
def payments_own():
    return render_template('base.html', content_file='payments_own.html')


# Płatności - Przelew zagraniczny
@app.route('/payments/foreign')
def payments_foreign():
    return render_template('base.html', content_file='payments_foreign.html')


# Oferty
@app.route('/offers')
def offers():
    return render_template('base.html', content_file='offers.html')


# Zarządzanie finansami
@app.route('/financial_management')
def financial_management():
    return render_template('base.html', content_file='fin_man.html')


# Wylogowanie
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
