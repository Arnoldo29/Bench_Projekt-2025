import streamlit as st
import random
import string
import pandas as pd
import json
import io
from faker import Faker  # Importiert die Faker-Bibliothek

# Klasse zur Generierung von Testdaten
class TestDataGenerator:
    def __init__(self):
        self.fake = Faker(['de_DE', 'pl_PL', 'de_AT', 'nl_NL', 'de_CH'])  # Initialisiert Faker mit den angegebenen Ländern
        self.genders = ['Männlich', 'Weiblich', 'Divers', 'Keine Angabe']  # Definiert die Geschlechter

    def generate_username(self):
        """Generiert einen zufälligen Benutzernamen."""
        return self.fake.user_name()  # Verwendet Faker zur Generierung eines Benutzernamens

    def generate_password(self):
        """Generiert ein zufälliges Passwort."""
        return self.fake.password()  # Verwendet Faker zur Generierung eines Passworts

    def generate_email(self):
        """Generiert eine zufällige E-Mail-Adresse."""
        return self.fake.email()  # Verwendet Faker zur Generierung einer E-Mail-Adresse

    def generate_product(self):
        """Generiert einen zufälligen Produktnamen."""
        products = ['Kaffee', 'Espresso', 'Latte', 'Cappuccino', 'Mokka']  # Definiert eine Liste von Produkten
        return random.choice(products)  # Wählt zufällig ein Produkt aus der Liste

    def generate_last_name(self):
        """Generiert einen zufälligen Nachnamen."""
        return self.fake.last_name()  # Verwendet Faker zur Generierung eines Nachnamens

    def generate_first_name(self, gender):
        """Generiert einen zufälligen Vornamen basierend auf dem Geschlecht."""
        if gender == 'Männlich':
            return self.fake.first_name_male()  # Verwendet Faker zur Generierung eines männlichen Vornamens
        elif gender == 'Weiblich':
            return self.fake.first_name_female()  # Verwendet Faker zur Generierung eines weiblichen Vornamens
        else:
            return self.fake.first_name()  # Verwendet Faker zur Generierung eines Vornamens ohne Geschlechtsspezifikation

    def generate_street(self):
        """Generiert eine zufällige Straße."""
        return self.fake.street_name()  # Verwendet Faker zur Generierung eines Straßennamens

    def generate_city(self):
        """Generiert eine zufällige Stadt."""
        return self.fake.city()  # Verwendet Faker zur Generierung eines Stadtnamens

    def generate_country(self):
        """Generiert ein zufälliges Land."""
        countries = ['Deutschland', 'Polen', 'Österreich', 'Niederlande', 'Schweiz']  # Definiert eine Liste von Ländern
        return random.choice(countries)  # Wählt zufällig ein Land aus der Liste

    def generate_phone_number(self):
        """Generiert eine zufällige Telefonnummer."""
        return self.fake.phone_number()  # Verwendet Faker zur Generierung einer Telefonnummer

    def generate_postal_code(self):
        """Generiert eine zufällige Postleitzahl."""
        return self.fake.postcode()  # Verwendet Faker zur Generierung einer Postleitzahl

    def generate_age(self):
        """Generiert ein zufälliges Alter."""
        return random.randint(18, 99)  # Generiert ein zufälliges Alter zwischen 18 und 99

    def generate_gender(self):
        """Generiert ein zufälliges Geschlecht."""
        return random.choice(self.genders)  # Wählt zufällig ein Geschlecht aus der Liste

    def generate_order(self, selected_city, selected_country, gender):
        """Generiert eine zufällige Bestellung."""
        first_name = self.generate_first_name(gender)  # Generiert einen Vornamen basierend auf dem Geschlecht
        last_name = self.generate_last_name()  # Generiert einen Nachnamen
        return {
            'benutzername': self.generate_username(),  # Generiert einen Benutzernamen
            'passwort': self.generate_password(),  # Generiert ein Passwort
            'email': self.generate_email(),  # Generiert eine E-Mail-Adresse
            'nachname': last_name,  # Fügt den Nachnamen hinzu
            'vorname': first_name,  # Fügt den Vornamen hinzu
            'straße': self.generate_street(),  # Generiert eine Straße
            'stadt': selected_city,  # Fügt die ausgewählte Stadt hinzu
            'postleitzahl': self.generate_postal_code(),  # Generiert eine Postleitzahl
            'land': selected_country,  # Fügt das ausgewählte Land hinzu
            'telefonnummer': self.generate_phone_number(),  # Generiert eine Telefonnummer
            'produkt': self.generate_product(),  # Generiert ein Produkt
            'menge': random.randint(1, 5),  # Generiert eine zufällige Menge zwischen 1 und 5
            'alter': self.generate_age(),  # Generiert ein Alter
            'geschlecht': gender  # Fügt das Geschlecht hinzu
        }

    def generate_registration(self):
        """Generiert Registrierungsdaten."""
        password = self.generate_password()  # Generiert ein Passwort
        return {
            'benutzername': self.generate_username(),  # Generiert einen Benutzernamen
            'passwort': password,  # Fügt das Passwort hinzu
            'passwort_wiederholen': password,  # Wiederholt das Passwort
            'AGB akzeptieren': False  # Setzt den Wert für AGB akzeptieren auf False
        }

    def generate_login(self):
        """Generiert Login-Daten."""
        return {
            'benutzername': self.generate_username(),  # Generiert einen Benutzernamen
            'passwort': self.generate_password()  # Generiert ein Passwort
        }

    def generate_profile(self, selected_city, selected_country):
        """Generiert Profildaten."""
        gender = self.generate_gender()  # Generiert ein Geschlecht
        first_name = self.generate_first_name(gender)  # Generiert einen Vornamen basierend auf dem Geschlecht
        last_name = self.generate_last_name()  # Generiert einen Nachnamen
        return {
            'nachname': last_name,  # Fügt den Nachnamen hinzu
            'vorname': first_name,  # Fügt den Vornamen hinzu
            'straße': self.generate_street(),  # Generiert eine Straße
            'stadt': selected_city,  # Fügt die ausgewählte Stadt hinzu
            'postleitzahl': self.generate_postal_code(),  # Generiert eine Postleitzahl
            'land': selected_country,  # Fügt das ausgewählte Land hinzu
            'telefonnummer': self.generate_phone_number(),  # Generiert eine Telefonnummer
            'alter': self.generate_age(),  # Generiert ein Alter
            'geschlecht': gender,  # Fügt das Geschlecht hinzu
            'email': self.generate_email()  # Generiert eine E-Mail-Adresse
        }

    def export_data(self, data, format='json'):
        """Exportiert die Daten in das angegebene Format."""
        if format == 'json':
            return json.dumps(data.to_dict(orient='records'), indent=4)  # Exportiert die Daten als JSON
        elif format == 'csv':
            return data.to_csv(index=False)  # Exportiert die Daten als CSV
        elif format == 'xlsx':
            output = io.BytesIO()  # Erstellt einen BytesIO-Stream
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                data.to_excel(writer, index=False, sheet_name='Sheet1')  # Exportiert die Daten als Excel
            return output.getvalue()  # Gibt den Wert des Streams zurück
        else:
            raise ValueError("Unsupported format")  # Wirft einen Fehler bei einem nicht unterstützten Format

    def apply_css(self):
        """Wendet eine CSS-Datei an, um das Design der Webseite zu verbessern."""
        css = """
        <style>
        body {
            background-color: #add8e6;  /* Hellblauer Hintergrund */
            font-family: 'Arial', sans-serif;
            color: #add8e6;  /* Hellblaue Schriftfarbe */
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 8px;
        }
        .stSelectbox {
            font-size: 16px;
        }
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)  # Wendet das CSS auf die Streamlit-App an

def generate_data(generator, data_type, num_records):
    """Generiert die Daten basierend auf dem ausgewählten Datentyp und der Anzahl der Datensätze."""
    data_list = []  # Erstellt eine leere Liste für die Daten
    for _ in range(num_records):
        selected_country = generator.generate_country()  # Generiert ein Land
        selected_city = generator.generate_city()  # Generiert eine Stadt
        if data_type == 'order':
            gender = generator.generate_gender()  # Generiert ein Geschlecht
            data = generator.generate_order(selected_city, selected_country, gender)  # Generiert eine Bestellung
        elif data_type == 'registrierung':
            data = generator.generate_registration()  # Generiert Registrierungsdaten
        elif data_type == 'login':
            data = generator.generate_login()  # Generiert Login-Daten
        elif data_type == 'profil':
            data = generator.generate_profile(selected_city, selected_country)  # Generiert Profildaten
        else:
            st.error("Ungültiger Datentyp ausgewählt.")  # Zeigt eine Fehlermeldung an
        data_list.append(data)  # Fügt die generierten Daten zur Liste hinzu
    return data_list  # Gibt die Liste der generierten Daten zurück

# Streamlit App
st.title('Testdaten-Generator')  # Titel der Streamlit App
st.subheader('Willkommen beim Testdaten-Generator für einen Coffeeshop!')  # Untertitel der Streamlit App

generator = TestDataGenerator()  # Instanziierung des TestDataGenerator

# Wendet das CSS-Design an
generator.apply_css()

# Auswahlbox zur Auswahl des Datentyps
data_type = st.selectbox('Datentyp zum Generieren auswählen',
                         ['registrierung', 'login', 'profil'])

# Auswahlbox zur Auswahl der Anzahl der zu generierenden Daten
num_records = st.number_input('Anzahl der zu generierenden Datensätze auswählen', min_value=1, max_value=1000, value=100)

if st.button('Daten generieren'):
    data_list = generate_data(generator, data_type, num_records)  # Generiert die Daten
    df = pd.DataFrame(data_list)  # Erstellt ein DataFrame aus den generierten Daten
    st.subheader('**Generierte Daten**')  # Fügt einen mittleren großen Titel in Bolt hinzu
    if data_type == 'registrierung':
        if 'AGB akzeptieren' not in df.columns:
            df['AGB akzeptieren'] = False  # Fügt die Spalte 'AGB akzeptieren' hinzu, falls nicht vorhanden
        for i in range(len(df)):
            df.at[i, 'AGB akzeptieren'] = st.checkbox('', value=df.at[i, 'AGB akzeptieren'], key=f'agb_checkbox_{i}')  # Fügt Checkboxen hinzu
    st.dataframe(df)  # Anzeige der generierten Daten in tabellarischer Form

# Auswahlbox zur Auswahl des Exportformats
st.subheader('**Exportieren Sie die Daten**')  # Fügt einen mittleren großen Titel in Bolt hinzu
format = st.selectbox('Exportformat auswählen', ['json', 'csv', 'xlsx'])
if st.button('Daten exportieren'):
    data_list = generate_data(generator, data_type, num_records)  # Generiert die Daten
    df = pd.DataFrame(data_list)  # Erstellt ein DataFrame aus den generierten Daten
    try:
        exported_data = generator.export_data(df, format)  # Exportiert die Daten im ausgewählten Format
        if format == 'json' or format == 'csv':
            st.text(exported_data)  # Anzeige der exportierten Daten
        elif format == 'xlsx':
            st.download_button(label='Download XLSX', data=exported_data, file_name='data.xlsx')  # Download-Button für Excel-Datei
    except ValueError as e:
        st.error(f"Fehler: {str(e)}")  # Anzeige einer Fehlermeldung bei ungültigem Format