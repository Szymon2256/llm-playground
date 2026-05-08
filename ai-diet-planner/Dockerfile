# Używamy lekkiego obrazu Pythona
FROM python:3.12-slim

# Ustawiamy katalog roboczy wewnątrz kontenera
WORKDIR /app

# Kopiujemy plik z listą bibliotek
COPY requirements.txt .

# Instalujemy zależności
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy całą zawartość projektu do kontenera
COPY . .

# Informujemy, że aplikacja działa na porcie 8000
EXPOSE 8000

# Komenda startowa uruchamiająca serwer
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]