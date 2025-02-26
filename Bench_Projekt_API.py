import re
import streamlit as st
import random
import pandas as pd
import json
import io
from faker import Faker
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse
import uvicorn
from threading import Thread
import tempfile
import dicttoxml

# Initialize FastAPI
app = FastAPI()

# Class for generating test data
class TestDataGenerator:
    def __init__(self):
        self.fake = Faker(['de_DE', 'pl_PL', 'de_AT', 'nl_NL', 'de_CH'])
        self.genders = ['Männlich', 'Weiblich', 'Divers', 'Keine Angabe']

    def generate_username(self):
        username = self.fake.user_name()
        if re.search(r'[^a-zA-Z0-9_]', username):
            print("Fehler: Benutzername enthält Sonderzeichen!")
        return username

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

    def generate_bestellung(self, city, country, gender):
        product = self.generate_product()
        quantity = random.randint(1, 5)
        price = round(random.uniform(1.0, 10.0) * quantity, 2)
        return {
            'produkt': product,
            'menge': quantity,
            'preis': f"{price} €",
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
        if format == 'json':
            return json.dumps(data.to_dict(orient='records'), indent=4, ensure_ascii=False)
        elif format == 'csv':
            return data.to_csv(index=False)
        elif format == 'xlsx':
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                data.to_excel(writer, index=False, sheet_name='Sheet1')
            return output.getvalue()
        elif format == 'xml':
            return dicttoxml.dicttoxml(data.to_dict(orient='records'), custom_root='data', attr_type=False).decode()
        elif format == 'txt':
            return data.to_string(index=False)
        else:
            raise ValueError("Unsupported format")

@app.get("/generate/{data_type}/{num_records}")
def generate_data_api(data_type: str, num_records: int):
    if num_records <= 0:
        raise HTTPException(status_code=400, detail="Der eingegebene Datensatz stimmt nicht überein! Der soll ab 1 beginnen")
    if num_records > 10000:
        raise HTTPException(status_code=400, detail="Number of records too large")

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
            raise HTTPException(status_code=404, detail="Invalid data type")
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

data = pd.DataFrame({
    'name': ['Alice', 'Bob'],
    'age': [25, 30]
})

@app.get("/export_data/json")
def export_data_json():
    json_data = data.to_json(orient='records')
    return JSONResponse(content=json_data)

@app.get("/export_data/xlsx")
def export_data_xlsx():
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        data.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        tmp.write(output.read())
        tmp_path = tmp.name
    return FileResponse(tmp_path, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename="data.xlsx")

# Streamlit UI
st.title('Testdaten-Generator')
st.subheader('Willkommen beim Testdaten-Generator für einen Coffeeshop!')

generator = TestDataGenerator()

data_type = st.selectbox('Datentyp wählen', ['registrierung', 'login', 'profil', 'bestellung'])
num_records = st.number_input('Anzahl der Datensätze', min_value=1, max_value=10000, value=1)

if st.button('🛠️ Daten generieren'):
    if num_records <= 0:
        st.error("Der eingegebene Datensatz stimmt nicht überein! Der soll ab 1 beginnen")
    else:
        try:
            data_list = generate_data_api(data_type, num_records)
            df = pd.DataFrame(data_list)
            st.session_state['generated_data'] = df
            st.success(f"{num_records} Datensätze generiert!")

            if data_type == 'bestellung':
                st.subheader("📦 Bestelldetails")
                st.dataframe(df)
            elif data_type == 'registrierung':
                st.subheader("📋 Registrierungsdaten")
                st.dataframe(df)
            elif data_type == 'login':
                st.subheader("🔑 Login-Daten")
                st.dataframe(df)
            elif data_type == 'profil':
                st.subheader("👤 Profildaten")
                st.dataframe(df)
        except ValueError as e:
            st.error(str(e))

st.subheader('**📤 Exportieren Sie die Daten**')
format = st.selectbox('Exportformat auswählen', ['json', 'csv', 'xlsx', 'xml', 'txt'])
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
            elif format == 'xml':
                st.download_button(label='📥 Download XML', data=exported_data, file_name='data.xml', mime='application/xml')
            elif format == 'txt':
                st.download_button(label='📥 Download TXT', data=exported_data, file_name='data.txt', mime='text/plain')
        except ValueError as e:
            st.error(f"Fehler: {str(e)}")
    else:
        st.warning("⚠️ Bitte zuerst Daten generieren!")

def run_api():
    uvicorn.run(app, host='0.0.0.0', port=8000)

thread = Thread(target=run_api, daemon=True)
thread.start()

if __name__ == "__main__":
    st.write("API gestartet auf http://localhost:8000")