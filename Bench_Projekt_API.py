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

# Initialisiere FastAPI
app = FastAPI()

# Klasse zur Generierung von Testdaten
class TestDataGenerator:
    def __init__(self):
        self.fake = Faker(['de_DE', 'pl_PL', 'de_AT', 'nl_NL', 'de_CH'])
        self.genders = ['Männlich', 'Weiblich', 'Divers', 'Keine Angabe']

    def generate_username(self):
        return self.fake.user_name()

    def generate_password(self):
        return self.fake.password()

    def generate_email(self):
        return self.fake.email()

    def generate_product(self):
        products = ['Kaffee', 'Espresso', 'Latte', 'Cappuccino', 'Mokka']
        return random.choice(products)

    def generate_last_name(self):
        return self.fake.last_name()

    def generate_first_name(self, gender):
        if gender == 'Männlich':
            return self.fake.first_name_male()
        elif gender == 'Weiblich':
            return self.fake.first_name_female()
        else:
            return self.fake.first_name()

    def generate_street(self):
        return self.fake.street_name()

    def generate_city(self):
        return self.fake.city()

    def generate_country(self):
        countries = ['Deutschland', 'Polen', 'Österreich', 'Niederlande', 'Schweiz']
        return random.choice(countries)

    def generate_phone_number(self):
        return self.fake.phone_number()

    def generate_postal_code(self):
        return self.fake.postcode()

    def generate_age(self):
        return random.randint(18, 99)

    def generate_gender(self):
        return random.choice(self.genders)

    def generate_order(self, city, country, gender):
        return {
            'benutzername': self.generate_username(),
            'passwort': self.generate_password(),
            'email': self.generate_email(),
            'nachname': self.generate_last_name(),
            'vorname': self.generate_first_name(gender),
            'straße': self.generate_street(),
            'stadt': city,
            'postleitzahl': self.generate_postal_code(),
            'land': country,
            'telefonnummer': self.generate_phone_number(),
            'produkt': self.generate_product(),
            'menge': random.randint(1, 5),
            'alter': self.generate_age(),
            'geschlecht': gender
        }

    def generate_registration(self):
        password = self.generate_password()
        return {
            'benutzername': self.generate_username(),
            'passwort': password,
            'passwort_wiederholen': password,
            'AGB akzeptieren': self.fake.boolean()
        }

    def generate_login(self):
        return {
            'benutzername': self.generate_username(),
            'passwort': self.generate_password()
        }

    def generate_profile(self, city, country):
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
        """Exportiert die Daten in das angegebene Format."""
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

# API-Endpunkt zur Generierung von Testdaten
@app.get("/generate/{data_type}/{num_records}")
def generate_data_api(data_type: str, num_records: int):
    generator = TestDataGenerator()
    data_list = []
    for _ in range(num_records):
        city = generator.generate_city()
        country = generator.generate_country()
        if data_type == 'order':
            gender = generator.generate_gender()
            data = generator.generate_order(city, country, gender)
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
async def login(request: Request):
    data = await request.json()
    username = data.get('Benutzername')
    password = data.get('passwort')

    if username == "admin" and password == "password123":
        return JSONResponse({"message": "Login erfolgreich!", "Benutzername": username})
    else:
        return JSONResponse({"message": "Falsche Anmeldedaten"}, status_code=401)

# Streamlit UI
st.title('Testdaten-Generator')
st.subheader('Willkommen beim Testdaten-Generator für einen Coffeeshop!')

generator = TestDataGenerator()

# Dropdowns für Benutzer
data_type = st.selectbox('Datentyp wählen', ['registrierung', 'login', 'profil', 'order'])
num_records = st.number_input('Anzahl der Datensätze', min_value=1, max_value=1000, value=100)

# 🆕 Button zum Generieren der Daten
if st.button('🛠️ Daten generieren'):
    data_list = generate_data_api(data_type, num_records)  # Daten abrufen
    df = pd.DataFrame(data_list)  # In DataFrame umwandeln
    st.session_state['generated_data'] = df  # Speichern für spätere Nutzung
    st.success(f"{num_records} Datensätze generiert!")

# Falls Daten bereits generiert wurden, anzeigen
if 'generated_data' in st.session_state:
    st.subheader("📊 Generierte Daten")
    st.dataframe(st.session_state['generated_data'])

# Export-Funktion
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

# API in separatem Thread starten
def run_api():
    uvicorn.run(app, host='0.0.0.0', port=8000)

thread = Thread(target=run_api, daemon=True)
thread.start()
