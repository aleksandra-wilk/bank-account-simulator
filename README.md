# bank-account-simulator

Instrukcja uruchomienia: 

1. Najpierw uruchomić plik models.py, który utworzy baze danych
2. Uruchomić program plikiem app.py 

W celu weryfikacji funkcjonalności należy:
1. Utworzyć nowe konto bieżące w zakładce Produkty - Nowe konto
2. Utworzyć nowe konto oszczędnościowe w zakładce Produkty - Nowe konto
+ jeśli konto zostanie założone bez karty można ją utworzyć w zakładce Produkty - Nowa karta

3. W celu sprawdzenia działania funkcji przelewów, trzeba najpierw doładować konto.
Aby to zrobić należy użyć pliku db_queries_temporary/query.py i wybrać opcję 
1 (dodawnie do tabeli) - 6 (doładuj konto). 
Konto zostanie zasilone kwota 100 PLN. 
Po tej operacji można wykonywać przelewy

4. Wykonane przelewy pojawią się w histori transakcji w zakłdace Strona główna