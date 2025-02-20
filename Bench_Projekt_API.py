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
import requests  # Import the requests module

# Initialize FastAPI
app = FastAPI()

# Class for generating test data
class TestDataGenerator:
    def __init__(self):
        # Initialize Faker with various localizations
        self.fake = Faker(['de_DE', 'pl_PL', 'de_AT', 'nl_NL', 'de_CH'])
        self.genders = ['Männlich', 'Weiblich', 'Divers', 'Keine Angabe']

    def generate_username(self):
        # Generate a username
        username = self.fake.user_name()
        # Check for special characters
        if re.search(r'[^a-zA-Z0-9_]', username):
            raise ValueError("Benutzername enthält Sonderzeichen!")  # Raise error if special characters are found
        return username

    def generate_password(self):
        # Generate a password
        return self.fake.password()

    def generate_email(self):
        # Generate an email address
        return self.fake.email()

    def generate_product(self):
        # Randomly select a product
        products = ['Kaffee', 'Espresso', 'Latte', 'Cappuccino', 'Mokka']
        return random.choice(products)

    def generate_last_name(self):
        # Generate a last name
        return self.fake.last_name()

    def generate_first_name(self, gender):
        # Generate a first name based on gender
        if gender == 'Männlich':
            return self.fake.first_name_male()
        elif gender == 'Weiblich':
            return self.fake.first_name_female()
        else:
            return self.fake.first_name()

    def generate_street(self):
        # Generate a street name
        return self.fake.street_name()

    def generate_city(self):
        # Generate a city name
        return self.fake.city()

    def generate_country(self):
        # Randomly select a country
        countries = ['Deutschland', 'Polen', 'Österreich', 'Niederlande', 'Schweiz']
        return random.choice(countries)

    def generate_phone_number(self):
        # Generate a phone number
        return self.fake.phone_number()

    def generate_postal_code(self):
        # Generate a postal code
        return self.fake.postcode()

    def generate_age(self):
        # Generate an age between 18 and 99
        return random.randint(18, 99)

    def generate_gender(self):
        # Randomly select a gender
        return random.choice(self.genders)

    def generate_bestellung(self, city, country, gender):
        # Generate an order
        product = self.generate_product()
        quantity = random.randint(1, 5)
        price = round(random.uniform(1.0, 10.0) * quantity, 2)  # Generate a random price
        return {
            'produkt': product,
            'menge': quantity,
            'preis': f"{price} €",  # Add price to the order with Euro symbol
        }

    def generate_registration(self):
        # Generate a registration
        password = self.generate_password()
        return {
            'benutzername': self.generate_username(),
            'passwort': password,
            'passwort_wiederholen': password,
            'AGB akzeptieren': self.fake.boolean()
        }

    def generate_login(self):
        # Generate a login
        return {
            'benutzername': self.generate_username(),
            'passwort': self.generate_password()
        }

    def generate_profile(self, city, country):
        # Generate a profile
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
        # Exports the data in the specified format
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

# API endpoint for generating test data
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
    return JSONResponse({"Benutzername": username, "passwort": password})

# Streamlit UI
st.title('Testdaten-Generator')
st.subheader('Willkommen beim Testdaten-Generator für einen Coffeeshop!')

generator = TestDataGenerator()

# Dropdowns for user
data_type = st.selectbox('Datentyp wählen', ['registrierung', 'login', 'profil', 'bestellung'])
num_records = st.number_input('Anzahl der Datensätze', min_value=1, max_value=1000, value=100)

# Button to generate data
if st.button('🛠️ Daten generieren'):
    try:
        data_list = generate_data_api(data_type, num_records)  # Fetch data
        df = pd.DataFrame(data_list)  # Convert to DataFrame
        st.session_state['generated_data'] = df  # Save for later use
        st.success(f"{num_records} Datensätze generiert!")

        # Display data in DataFrame format if "Bestellung" is selected
        if data_type == 'bestellung':
            st.subheader("📦 Bestelldetails")
            st.dataframe(df)  # Display as DataFrame
        elif data_type == 'registrierung':
            st.subheader("📋 Registrierungsdetails")
            st.dataframe(df)  # Display as DataFrame
    except ValueError as e:
        st.error(str(e))

# If data has already been generated, display it
if 'generated_data' in st.session_state:
    st.subheader("📊 Generierte Daten")
    st.dataframe(st.session_state['generated_data'])

# Export function
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

# Start API in a separate thread
def run_api():
    uvicorn.run(app, host='0.0.0.0', port=8000)

thread = Thread(target=run_api, daemon=True)
thread.start()