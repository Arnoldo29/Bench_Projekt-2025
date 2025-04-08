import re
import streamlit as st
import random
import pandas as pd
import json
import io
import os
from faker import Faker
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse
import uvicorn
from threading import Thread
import tempfile
import dicttoxml

# Initialisiere FastAPI
app = FastAPI()

# Klasse zur Generierung von Testdaten
class TestDataGenerator:
    def __init__(self):
        self.fake = Faker(['de_DE', 'pl_PL', 'de_AT', 'nl_NL', 'de_CH'])
        self.genders = ['Männlich', 'Weiblich', 'Divers', 'Keine Angabe']

    def generate_username(self, valid=True):
        if valid:
            while True:
                username = re.sub(r'[^a-zA-Z0-9ÄÖÜäöü]', '', self.fake.user_name())
                if 4 <= len(username) <= 12:
                    return username
        else:
            return self.fake.user_name() + '@#'

    def generate_password(self, valid=True):
        if valid:
            while True:
                password = self.fake.password(
                    length=random.randint(8, 20),
                    special_chars=True,
                    digits=True,
                    upper_case=True,
                    lower_case=True
                )
                # Nur erlaubte Zeichen + Länge + mindestens ein Zeichen jeder Kategorie
                if (
                        8 <= len(password) <= 20 and
                        re.match(r'^[a-zA-Z0-9@$!%*?]+$', password) and
                        re.search(r'[a-z]', password) and
                        re.search(r'[A-Z]', password) and
                        re.search(r'\d', password) and
                        re.search(r'[@$!%*?]', password)
                ):
                    return password
        else:
            return 'abc'  # Ungültig: zu kurz, keine Sonderzeichen etc.

    def generate_email(self):
        return self.fake.email()

    def generate_bestellung(self):
        products = ['Kaffee', 'Espresso', 'Latte', 'Cappuccino', 'Mokka']
        quantity = random.randint(1, 5)
        price = round(random.uniform(1.0, 10.0) * quantity, 2)
        return {'produkt': random.choice(products), 'menge': quantity, 'preis': price, 'währung': 'EUR'}



    def generate_registration(self, valid=True):
        password = self.generate_password(valid)
        return {'benutzername': self.generate_username(valid), 'passwort': password, 'passwort_wiederholen': password, 'AGB akzeptieren': self.fake.boolean()}

    def generate_login(self, valid=True):
        return {'benutzername': self.generate_username(valid), 'passwort': self.generate_password(valid)}

    def generate_profile(self):
        gender = random.choice(self.genders)
        return {
            'nachname': self.fake.last_name(),
            'vorname': self.fake.first_name(),
            'straße': self.fake.street_name(),
            'stadt': self.fake.city(),
            'postleitzahl': self.fake.postcode(),
            'land': self.fake.country(),
            'telefonnummer': self.fake.phone_number(),
            'alter': random.randint(18, 99),
            'geschlecht': gender,
            'email': self.fake.email()
        }

    def export_data(self, df, format):
        if format == 'json':
            return df.to_json(orient='records', indent=4).encode('utf-8')
        elif format == 'csv':
            return df.to_csv(index=False).encode('utf-8')
        elif format == 'xlsx':
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Daten')
            return output.getvalue()
        elif format == 'xml':
            xml_data = dicttoxml.dicttoxml(df.to_dict(orient='records'), custom_root='daten', attr_type=False)
            return xml_data
        else:
            raise ValueError('Ungültiges Exportformat')

# API-Endpoints
@app.get("/generate/{data_type}/{num_records}")
def generate_data_api(data_type: str, num_records: int):
    if num_records <= 0:
        raise HTTPException(status_code=400, detail="Keine Datensätze generiert! Die Anzahl der Datensätze muss größer als 0 sein.")
    if num_records > 10000:
        raise HTTPException(status_code=400, detail="Number of records too large")

    generator = TestDataGenerator()
    valid_list = []
    invalid_list = []

    for _ in range(num_records):
        if data_type == 'bestellung':
            valid_list.append(generator.generate_bestellung())
            invalid_list.append(generator.generate_bestellung())
        elif data_type == 'registrierung':
            valid_list.append(generator.generate_registration(valid=True))
            invalid_list.append(generator.generate_registration(valid=False))
        elif data_type == 'login':
            valid_list.append(generator.generate_login(valid=True))
            invalid_list.append(generator.generate_login(valid=False))
        elif data_type == 'profil':
            valid_list.append(generator.generate_profile())
            invalid_list.append(generator.generate_profile())
        else:
            raise HTTPException(status_code=404, detail="Ungültiger Datentyp")

    return JSONResponse(content={"gültige_daten": valid_list, "ungültige_daten": invalid_list})




# Streamlit UI
st.title('Testdaten-Generator')

generator = TestDataGenerator()

data_type = st.selectbox('Datentyp wählen', ['registrierung', 'login', 'profil', 'bestellung'])
num_records = st.number_input('Anzahl der Datensätze', min_value=1, max_value=10000, value=1)

if 'valid_data' not in st.session_state:
    st.session_state['valid_data'] = None
if 'invalid_data' not in st.session_state:
    st.session_state['invalid_data'] = None

if st.button('🛠️ Gültige Daten generieren'):
    data_list = [
        generator.generate_registration(valid=True) if data_type == 'registrierung' else
        generator.generate_login(valid=True) if data_type == 'login' else
        generator.generate_profile() if data_type == 'profil' else
        generator.generate_bestellung()
        for _ in range(num_records)
    ]
    df = pd.DataFrame(data_list)
    st.session_state['valid_data'] = df
    st.success(f'{num_records} gültige Datensätze generiert!')
    st.dataframe(df)

if st.button('❌ Ungültige Daten generieren'):
    data_list = [
        generator.generate_registration(valid=False) if data_type == 'registrierung' else
        generator.generate_login(valid=False) if data_type == 'login' else
        generator.generate_profile() if data_type == 'profil' else
        generator.generate_bestellung()
        for _ in range(num_records)
    ]
    df = pd.DataFrame(data_list)
    st.session_state['invalid_data'] = df
    st.warning(f'{num_records} ungültige Datensätze generiert!')
    st.dataframe(df)

st.subheader('📤 Daten exportieren')
format = st.selectbox('Exportformat', ['json', 'csv', 'xlsx', 'xml'])
if st.button('💾 Exportieren'):
    if st.session_state['valid_data'] is not None:
        exported_data = generator.export_data(st.session_state['valid_data'], format)
        st.download_button(label=f'📥 Download {format.upper()} (gültig)', data=exported_data,
                           file_name=f'valid_data.{format}', mime=f'application/{format}')
    if st.session_state['invalid_data'] is not None:
        exported_data = generator.export_data(st.session_state['invalid_data'], format)
        st.download_button(label=f'📥 Download {format.upper()} (ungültig)', data=exported_data,
                           file_name=f'invalid_data.{format}', mime=f'application/{format}')
    if st.session_state['valid_data'] is None and st.session_state['invalid_data'] is None:
        st.warning('⚠️ Keine generierten Daten zum Exportieren!')

# Starte FastAPI-Server in einem Thread
#def run_api():
    # Run the FastAPI server
    # Starte den FastAPI-Server
    #uvicorn.run(app, host='127.0.0.1', port=8000, log_level="info")

@app.get("/")
def read_root():
    return {"message": "Willkommen zur Testdaten-API! Verfügbare Endpunkte: /generate/{data_type}/{num_records}"}

if __name__ == "__main__":
    thread = Thread(target=uvicorn.run, args=("API_Neu:app",), kwargs={"host": "127.0.0.1", "port": 8001})
    thread.start()
    #uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    st.write("API gestartet auf http://localhost:8001")
