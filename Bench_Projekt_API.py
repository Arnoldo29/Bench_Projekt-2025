import re
import streamlit as st
import random
import pandas as pd
import json
import io
from faker import Faker
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
import uvicorn
from threading import Thread
from fastapi import HTTPException
import requests  # Import the requests module

# Initialize FastAPI
app = FastAPI()

# Klasse zur Generierung von Testdaten / Class for generating test data
class TestDataGenerator:
    def __init__(self):
        # Initialisiere Faker mit verschiedenen Lokalisierungen / Initialize Faker with various localizations
        self.fake = Faker(['de_DE', 'pl_PL', 'de_AT', 'nl_NL', 'de_CH'])
        self.genders = ['Männlich', 'Weiblich', 'Divers', 'Keine Angabe']

    def generate_username(self):
        # Generiere einen Benutzernamen / Generate a username
        username = self.fake.user_name()
        # Überprüfe auf Sonderzeichen / Check for special characters
        if re.search(r'[^a-zA-Z0-9_]', username):
            print(
                "Fehler: Benutzername enthält Sonderzeichen!")  # Fehler anzeigen, wenn Sonderzeichen gefunden werden / Display error if special characters are found
        return username

    def generate_password(self):
        # Generiere ein Passwort / Generate a password
        return self.fake.password()

    def generate_email(self):
        # Generiere eine E-Mail-Adresse / Generate an email address
        return self.fake.email()

    def generate_product(self):
        # Wähle ein Produkt zufällig aus / Randomly select a product
        products = ['Kaffee', 'Espresso', 'Latte', 'Cappuccino', 'Mokka']
        return random.choice(products)

    def generate_last_name(self):
        # Generiere einen Nachnamen / Generate a last name
        return self.fake.last_name()

    def generate_first_name(self, gender):
        # Generiere einen Vornamen basierend auf dem Geschlecht / Generate a first name based on gender
        if gender == 'Männlich':
            return self.fake.first_name_male()
        elif gender == 'Weiblich':
            return self.fake.first_name_female()
        else:
            return self.fake.first_name()

    def generate_street(self):
        # Generiere einen Straßennamen / Generate a street name
        return self.fake.street_name()

    def generate_city(self):
        # Generiere einen Stadtnamen / Generate a city name
        return self.fake.city()

    def generate_country(self):
        # Wähle ein Land zufällig aus / Randomly select a country
        countries = ['Deutschland', 'Polen', 'Österreich', 'Niederlande', 'Schweiz']
        return random.choice(countries)

    def generate_phone_number(self):
        # Generiere eine Telefonnummer / Generate a phone number
        return self.fake.phone_number()

    def generate_postal_code(self):
        # Generiere eine Postleitzahl / Generate a postal code
        return self.fake.postcode()

    def generate_age(self):
        # Generiere ein Alter zwischen 18 und 99 / Generate an age between 18 and 99
        return random.randint(18, 99)

    def generate_gender(self):
        # Wähle ein Geschlecht zufällig aus / Randomly select a gender
        return random.choice(self.genders)

    def generate_bestellung(self, city, country, gender):
        # Generiere eine Bestellung / Generate an order
        product = self.generate_product()
        quantity = random.randint(1, 5)
        price = round(random.uniform(1.0, 10.0) * quantity, 2)  # Generiere einen zufälligen Preis / Generate a random price
        return {
            'produkt': product,
            'menge': quantity,
            'preis': f"{price} €",  # Preis zur Bestellung hinzufügen mit Euro-Symbol / Add price to the order with Euro symbol
        }

    def generate_registration(self):
        # Generiere eine Registrierung / Generate a registration
        password = self.generate_password()
        return {
            'benutzername': self.generate_username(),
            'passwort': password,
            'passwort_wiederholen': password,
            'AGB akzeptieren': self.fake.boolean()
        }

    def generate_login(self):
        # Generiere einen Login / Generate a login
        return {
            'benutzername': self.generate_username(),
            'passwort': self.generate_password()
        }

    def generate_profile(self, city, country):
        # Generiere ein Profil / Generate a profile
        gender = self.generate_gender()
        return {
            'nachname': self.generate_last_name(),
            'vorname': self.generate_first_name(gender),
            'straße': self.generate_street(),
            'stadt': city,
            'postleitzahl': self.generate_postal_code(),
            'land': country,
            'telefonnummer': self.generate_phone_number(),
            'alter': self.generate_age(),
            'geschlecht': gender,
            'email': self.generate_email()
        }

    def export_data(self, data, format='json'):
        # Exportiere die Daten im angegebenen Format / Exports the data in the specified format
        if format == 'json':
            return json.dumps(data.to_dict(orient='records'), indent=4, ensure_ascii=False)
        elif format == 'csv':
            return data.to_csv(index=False)
        elif format == 'xlsx':
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                data.to_excel(writer, index=False, sheet_name='Sheet1')
            return output.getvalue()
        else:
            raise ValueError("Unsupported format")

# API-Endpunkt zur Generierung von Testdaten / API endpoint for generating test data
@app.get("/generate/{data_type}/{num_records}")
def generate_data_api(data_type: str, num_records: int):
    generator = TestDataGenerator()
    data_list = []
    for _ in range(num_records):
        city = generator.generate_city()
        country = generator.generate_country()
        if data_type == 'bestellung':
            gender = generator.generate_gender()
            data = generator.generate_bestellung(city, country, gender)
        elif data_type == 'registrierung':
            data = generator.generate_registration()
        elif data_type == 'login':
            data = generator.generate_login()
        elif data_type == 'profil':
            data = generator.generate_profile(city, country)
        else:
            return JSONResponse(status_code=400, content={"error": "Ungültiger Datentyp"})
        data_list.append(data)
    return data_list

@app.post("/login")
async def login(username: str, password: str):
    try:
        if re.search(r'[^a-zA-Z0-9_]', username):
            raise ValueError("Benutzername enthält Sonderzeichen!")
        return JSONResponse({"Benutzername": username, "passwort": password})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Streamlit UI
st.title('Testdaten-Generator')
st.subheader('Willkommen beim Testdaten-Generator für einen Coffeeshop!')

generator = TestDataGenerator()

# Dropdowns für den Benutzer / Dropdowns for user
data_type = st.selectbox('Datentyp wählen', ['registrierung', 'login', 'profil', 'bestellung'])
num_records = st.number_input('Anzahl der Datensätze', min_value=1, max_value=1000, value=100)

# Button zum Generieren von Daten / Button to generate data
if st.button('🛠️ Daten generieren'):
    try:
        data_list = generate_data_api(data_type, num_records)  # Daten abrufen / Fetch data
        df = pd.DataFrame(data_list)  # In DataFrame umwandeln / Convert to DataFrame
        st.session_state['generated_data'] = df  # Für spätere Verwendung speichern / Save for later use
        st.success(f"{num_records} Datensätze generiert!")

        # Daten im DataFrame-Format anzeigen, wenn "Bestellung" ausgewählt ist / Display data in DataFrame format if "Bestellung" is selected
        if data_type == 'bestellung':
            st.subheader("📦 Bestelldetails")
            st.dataframe(df)  # Als DataFrame anzeigen / Display as DataFrame
        elif data_type == 'registrierung':
            st.subheader("📋 Registrierungsdetails")
            st.dataframe(df)  # Als DataFrame anzeigen / Display as DataFrame

        elif data_type == 'login':
            st.subheader("🔑 Login-Details")
            st.dataframe(df)  # Als DataFrame anzeigen / Display as DataFrame
        elif data_type == 'profil':
            st.subheader("👤 Profildetails")
            st.dataframe(df)  # Als DataFrame anzeigen / Display as DataFrame
    except ValueError as e:
        st.error(str(e))

# Wenn Daten bereits generiert wurden, anzeigen / If data has already been generated, display it
#if 'generated_data' in st.session_state:
   # st.subheader("📊 Generierte Daten")
   # st.dataframe(st.session_state['generated_data'])

# Exportfunktion / Export function
st.subheader('**📤 Exportieren Sie die Daten**')
format = st.selectbox('Exportformat auswählen', ['json', 'csv', 'xlsx'])
if st.button('💾 Daten exportieren'):
    if 'generated_data' in st.session_state:
        try:
            exported_data = generator.export_data(st.session_state['generated_data'], format)
            if format == 'json':
                st.download_button(label='📥 Download JSON', data=exported_data, file_name='data.json', mime='application/json')
            elif format == 'csv':
                st.download_button(label='📥 Download CSV', data=exported_data, file_name='data.csv', mime='text/csv')
            elif format == 'xlsx':
                st.download_button(label='📥 Download XLSX', data=exported_data, file_name='data.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        except ValueError as e:
            st.error(f"Fehler: {str(e)}")
    else:
        st.warning("⚠️ Bitte zuerst Daten generieren!")

# API in einem separaten Thread starten / Start API in a separate thread
def run_api():
    uvicorn.run(app, host='0.0.0.0', port=8000)

thread = Thread(target=run_api, daemon=True)
thread.start()