import streamlit as st
import random
import string
import pandas as pd
import json
import io
from faker import Faker  # Import the Faker library

# Klasse zur Generierung von Testdaten / Class for generating test data
class TestDataGenerator:
    def __init__(self):
        self.fake = Faker(['de_DE', 'pl_PL', 'de_AT', 'nl_NL', 'de_CH'])  # Initialisiert Faker mit den angegebenen Ländern / Initialize Faker with the specified countries
        self.genders = ['Männlich', 'Weiblich', 'Divers', 'Keine Angabe']  # Definiert die Geschlechter / Define the genders

    def generate_username(self):
        """Generiert einen zufälligen Benutzernamen / Generates a random username."""
        return self.fake.user_name()  # Verwendet Faker zur Generierung eines Benutzernamens / Use Faker to generate a username

    def generate_password(self):
        """Generiert ein zufälliges Passwort / Generates a random password."""
        return self.fake.password()  # Verwendet Faker zur Generierung eines Passworts / Use Faker to generate a password

    def generate_email(self):
        """Generiert eine zufällige E-Mail-Adresse / Generates a random email address."""
        return self.fake.email()  # Verwendet Faker zur Generierung einer E-Mail-Adresse / Use Faker to generate an email address

    def generate_product(self):
        """Generiert einen zufälligen Produktnamen / Generates a random product name."""
        products = ['Kaffee', 'Espresso', 'Latte', 'Cappuccino', 'Mokka']  # Definiert eine Liste von Produkten / Define a list of products
        return random.choice(products)  # Wählt zufällig ein Produkt aus der Liste / Randomly select a product from the list

    def generate_last_name(self):
        """Generiert einen zufälligen Nachnamen / Generates a random last name."""
        return self.fake.last_name()  # Verwendet Faker zur Generierung eines Nachnamens / Use Faker to generate a last name

    def generate_first_name(self, gender):
        """Generiert einen zufälligen Vornamen basierend auf dem Geschlecht / Generates a random first name based on gender."""
        if gender == 'Männlich':
            return self.fake.first_name_male()  # Verwendet Faker zur Generierung eines männlichen Vornamens / Use Faker to generate a male first name
        elif gender == 'Weiblich':
            return self.fake.first_name_female()  # Verwendet Faker zur Generierung eines weiblichen Vornamens / Use Faker to generate a female first name
        else:
            return self.fake.first_name()  # Verwendet Faker zur Generierung eines Vornamens ohne Geschlechtsspezifikation / Use Faker to generate a gender-neutral first name

    def generate_street(self):
        """Generiert eine zufällige Straße / Generates a random street."""
        return self.fake.street_name()  # Verwendet Faker zur Generierung eines Straßennamens / Use Faker to generate a street name

    def generate_city(self):
        """Generiert eine zufällige Stadt / Generates a random city."""
        return self.fake.city()  # Verwendet Faker zur Generierung eines Stadtnamens / Use Faker to generate a city name

    def generate_country(self):
        """Generiert ein zufälliges Land / Generates a random country."""
        countries = ['Deutschland', 'Polen', 'Österreich', 'Niederlande', 'Schweiz']  # Definiert eine Liste von Ländern / Define a list of countries
        return random.choice(countries)  # Wählt zufällig ein Land aus der Liste / Randomly select a country from the list

    def generate_phone_number(self):
        """Generiert eine zufällige Telefonnummer / Generates a random phone number."""
        return self.fake.phone_number()  # Verwendet Faker zur Generierung einer Telefonnummer / Use Faker to generate a phone number

    def generate_postal_code(self):
        """Generiert eine zufällige Postleitzahl / Generates a random postal code."""
        return self.fake.postcode()  # Verwendet Faker zur Generierung einer Postleitzahl / Use Faker to generate a postal code

    def generate_age(self):
        """Generiert ein zufälliges Alter / Generates a random age."""
        return random.randint(18, 99)  # Generiert ein zufälliges Alter zwischen 18 und 99 / Generate a random age between 18 and 99

    def generate_gender(self):
        """Generiert ein zufälliges Geschlecht / Generates a random gender."""
        return random.choice(self.genders)  # Wählt zufällig ein Geschlecht aus der Liste / Randomly select a gender from the list

    def generate_order(self, selected_city, selected_country, gender):
        """Generiert eine zufällige Bestellung / Generates a random order."""
        first_name = self.generate_first_name(gender)  # Generiert einen Vornamen basierend auf dem Geschlecht / Generate a first name based on gender
        last_name = self.generate_last_name()  # Generiert einen Nachnamen / Generate a last name
        return {
            'benutzername': self.generate_username(),  # Generiert einen Benutzernamen / Generate a username
            'passwort': self.generate_password(),  # Generiert ein Passwort / Generate a password
            'email': self.generate_email(),  # Generiert eine E-Mail-Adresse / Generate an email address
            'nachname': last_name,  # Fügt den Nachnamen hinzu / Add the last name
            'vorname': first_name,  # Fügt den Vornamen hinzu / Add the first name
            'straße': self.generate_street(),  # Generiert eine Straße / Generate a street
            'stadt': selected_city,  # Fügt die ausgewählte Stadt hinzu / Add the selected city
            'postleitzahl': self.generate_postal_code(),  # Generiert eine Postleitzahl / Generate a postal code
            'land': selected_country,  # Fügt das ausgewählte Land hinzu / Add the selected country
            'telefonnummer': self.generate_phone_number(),  # Generiert eine Telefonnummer / Generate a phone number
            'produkt': self.generate_product(),  # Generiert ein Produkt / Generate a product
            'menge': random.randint(1, 5),  # Generiert eine zufällige Menge zwischen 1 und 5 / Generate a random quantity between 1 and 5
            'alter': self.generate_age(),  # Generiert ein Alter / Generate an age
            'geschlecht': gender  # Fügt das Geschlecht hinzu / Add the gender
        }

    def generate_registration(self):
        """Generiert Registrierungsdaten / Generates registration data."""
        password = self.generate_password()  # Generiert ein Passwort / Generate a password
        return {
            'benutzername': self.generate_username(),  # Generiert einen Benutzernamen / Generate a username
            'passwort': password,  # Fügt das Passwort hinzu / Add the password
            'passwort_wiederholen': password,  # Wiederholt das Passwort / Repeat the password
            'AGB akzeptieren': self.fake.boolean()  # Setzt den Wert für AGB akzeptieren zufällig / Randomly set the value for AGB akzeptieren
        }

    def generate_login(self):
        """Generiert Login-Daten / Generates login data."""
        return {
            'benutzername': self.generate_username(),  # Generiert einen Benutzernamen / Generate a username
            'passwort': self.generate_password()  # Generiert ein Passwort / Generate a password
        }

    def generate_profile(self, selected_city, selected_country):
        """Generiert Profildaten / Generates profile data."""
        gender = self.generate_gender()  # Generiert ein Geschlecht / Generate a gender
        first_name = self.generate_first_name(gender)  # Generiert einen Vornamen basierend auf dem Geschlecht / Generate a first name based on gender
        last_name = self.generate_last_name()  # Generiert einen Nachnamen / Generate a last name
        return {
            'nachname': last_name,  # Fügt den Nachnamen hinzu / Add the last name
            'vorname': first_name,  # Fügt den Vornamen hinzu / Add the first name
            'straße': self.generate_street(),  # Generiert eine Straße / Generate a street
            'stadt': selected_city,  # Fügt die ausgewählte Stadt hinzu / Add the selected city
            'postleitzahl': self.generate_postal_code(),  # Generiert eine Postleitzahl / Generate a postal code
            'land': selected_country,  # Fügt das ausgewählte Land hinzu / Add the selected country
            'telefonnummer': self.generate_phone_number(),  # Generiert eine Telefonnummer / Generate a phone number
            'alter': self.generate_age(),  # Generiert ein Alter / Generate an age
            'geschlecht': gender,  # Fügt das Geschlecht hinzu / Add the gender
            'email': self.generate_email()  # Generiert eine E-Mail-Adresse / Generate an email address
        }

    def export_data(self, data, format='json'):
        """Exportiert die Daten in das angegebene Format / Exports the data in the specified format."""
        if format == 'json':
            return json.dumps(data.to_dict(orient='records'), indent=4, ensure_ascii=False)  # Exportiert die Daten als JSON und stellt sicher, dass deutsche Buchstaben korrekt dargestellt werden / Export the data as JSON and ensure German characters are correctly displayed
        elif format == 'csv':
            return data.to_csv(index=False)  # Exportiert die Daten als CSV / Export the data as CSV
        elif format == 'xlsx':
            output = io.BytesIO()  # Erstellt einen BytesIO-Stream / Create a BytesIO stream
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                data.to_excel(writer, index=False, sheet_name='Sheet1')  # Exportiert die Daten als Excel / Export the data as Excel
            return output.getvalue()  # Gibt den Wert des Streams zurück / Return the value of the stream
        else:
            raise ValueError("Unsupported format")  # Wirft einen Fehler bei einem nicht unterstützten Format / Raise an error for an unsupported format

    def apply_css(self):
        """Wendet eine CSS-Datei an, um das Design der Webseite zu verbessern / Applies a CSS file to improve the website design."""
        css = """
        <style>
        body {
            background-color: #add8e6;  /* Hellblauer Hintergrund / Light blue background */
            font-family: 'Arial', sans-serif;
            color: #add8e6;  /* Hellblaue Schriftfarbe / Light blue text color */
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
        st.markdown(css, unsafe_allow_html=True)  # Wendet das CSS auf die Streamlit-App an / Apply the CSS to the Streamlit app

def generate_data(generator, data_type, num_records):
    """Generiert die Daten basierend auf dem ausgewählten Datentyp und der Anzahl der Datensätze / Generates the data based on the selected data type and number of records."""
    data_list = []  # Erstellt eine leere Liste für die Daten / Create an empty list for the data
    for _ in range(num_records):
        selected_country = generator.generate_country()  # Generiert ein Land / Generate a country
        selected_city = generator.generate_city()  # Generiert eine Stadt / Generate a city
        if data_type == 'order':
            gender = generator.generate_gender()  # Generiert ein Geschlecht / Generate a gender
            data = generator.generate_order(selected_city, selected_country, gender)  # Generiert eine Bestellung / Generate an order
        elif data_type == 'registrierung':
            data = generator.generate_registration()  # Generiert Registrierungsdaten / Generate registration data
        elif data_type == 'login':
            data = generator.generate_login()  # Generiert Login-Daten / Generate login data
        elif data_type == 'profil':
            data = generator.generate_profile(selected_city, selected_country)  # Generiert Profildaten / Generate profile data
        else:
            st.error("Ungültiger Datentyp ausgewählt.")  # Zeigt eine Fehlermeldung an / Display an error message
        data_list.append(data)  # Fügt die generierten Daten zur Liste hinzu / Add the generated data to the list
    return data_list  # Gibt die Liste der generierten Daten zurück / Return the list of generated data

# Streamlit App
st.title('Testdaten-Generator')  # Titel der Streamlit App / Title of the Streamlit app
st.subheader('Willkommen beim Testdaten-Generator für einen Coffeeshop!')  # Untertitel der Streamlit App / Subtitle of the Streamlit app

generator = TestDataGenerator()  # Instanziierung des TestDataGenerator / Instantiate the TestDataGenerator

# Wendet das CSS-Design an / Apply the CSS design
generator.apply_css()

# Auswahlbox zur Auswahl des Datentyps / Select box to choose the data type
data_type = st.selectbox('Datentyp zum Generieren auswählen',
                         ['registrierung', 'login', 'profil'])

# Auswahlbox zur Auswahl der Anzahl der zu generierenden Daten / Select box to choose the number of records to generate
num_records = st.number_input('Anzahl der zu generierenden Datensätze auswählen', min_value=1, max_value=1000, value=100)

if st.button('Daten generieren'):
    data_list = generate_data(generator, data_type, num_records)  # Generiert die Daten / Generate the data
    df = pd.DataFrame(data_list)  # Erstellt ein DataFrame aus den generierten Daten / Create a DataFrame from the generated data
    st.subheader('**Generierte Daten**')  # Fügt einen mittleren großen Titel in Bolt hinzu / Add a medium-sized title in bold
    st.dataframe(df)  # Anzeige der generierten Daten in tabellarischer Form / Display the generated data in tabular form

# Auswahlbox zur Auswahl des Exportformats / Select box to choose the export format
st.subheader('**Exportieren Sie die Daten**')  # Fügt einen mittleren großen Titel in Bolt hinzu / Add a medium-sized title in bold
format = st.selectbox('Exportformat auswählen', ['json', 'csv', 'xlsx'])
if st.button('Daten exportieren'):
    data_list = generate_data(generator, data_type, num_records)  # Generiert die Daten / Generate the data
    df = pd.DataFrame(data_list)  # Erstellt ein DataFrame aus den generierten Daten / Create a DataFrame from the generated data
    try:
        exported_data = generator.export_data(df, format)  # Exportiert die Daten im ausgewählten Format / Export the data in the selected format
        if format == 'json':
            st.download_button(label='Download JSON', data=exported_data, file_name='data.json', mime='application/json')  # Download-Button für JSON-Datei / Download button for JSON file
        elif format == 'csv':
            st.download_button(label='Download CSV', data=exported_data, file_name='data.csv', mime='text/csv')  # Download-Button für CSV-Datei / Download button for CSV file
        elif format == 'xlsx':
            st.download_button(label='Download XLSX', data=exported_data, file_name='data.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')  # Download-Button für Excel-Datei / Download button for Excel file
    except ValueError as e:
        st.error(f"Fehler: {str(e)}")  # Anzeige einer Fehlermeldung bei ungültigem Format / Display an error message for an invalid format