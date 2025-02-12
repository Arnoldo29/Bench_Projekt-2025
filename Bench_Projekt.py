import streamlit as st
import random
import string

# Klasse zur Generierung von Testdaten
class TestDataGenerator:
    def __init__(self):
        self.products = ['Coffee', 'Espresso', 'Latte', 'Cappuccino', 'Mocha']
        self.last_names = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown']
        self.first_names = ['James', 'Mary', 'John', 'Patricia', 'Robert']
        self.streets = ['Main St', 'High St', 'Broadway', 'Elm St', 'Maple St']
        self.city_postal_code_map = {
            'Berlin': '10115',
            'Hamburg': '20095',
            'München': '80331',
            'Köln': '50667',
            'Frankfurt': '60311'
        }
        self.country = 'Deutschland'

    def generate_username(self):
        """Generiert einen zufälligen Benutzernamen."""
        return ''.join(random.choices(string.ascii_lowercase, k=8))

    def generate_password(self):
        """Generiert ein zufälliges Passwort."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

    def generate_email(self):
        """Generiert eine zufällige E-Mail-Adresse."""
        return self.generate_username() + '@example.com'

    def generate_product(self):
        """Generiert einen zufälligen Produktnamen."""
        return random.choice(self.products)

    def generate_last_name(self):
        """Generiert einen zufälligen Nachnamen."""
        return random.choice(self.last_names)

    def generate_first_name(self):
        """Generiert einen zufälligen Vornamen."""
        return random.choice(self.first_names)

    def generate_street(self):
        """Generiert eine zufällige Straße."""
        return random.choice(self.streets)

    def generate_city(self, selected_city):
        """Generiert die ausgewählte Stadt."""
        return selected_city

    def generate_country(self, selected_country):
        """Generiert das ausgewählte Land."""
        return selected_country

    def generate_phone_number(self):
        """Generiert eine zufällige Telefonnummer."""
        return ''.join(random.choices(string.digits, k=10))

    def generate_postal_code(self, selected_city):
        """Generiert die Postleitzahl basierend auf der ausgewählten Stadt."""
        return self.city_postal_code_map[selected_city]

    def generate_order(self, selected_city, selected_country):
        """Generiert eine zufällige Bestellung."""
        return {
            'username': self.generate_username(),
            'password': self.generate_password(),
            'email': self.generate_email(),
            'last_name': self.generate_last_name(),
            'first_name': self.generate_first_name(),
            'street': self.generate_street(),
            'city': self.generate_city(selected_city),
            'postal_code': self.generate_postal_code(selected_city),
            'country': self.generate_country(selected_country),
            'phone_number': self.generate_phone_number(),
            'product': self.generate_product(),
            'quantity': random.randint(1, 5)
        }

    def generate_order_with_discount(self, selected_city, selected_country):
        """Generiert eine zufällige Bestellung mit Rabatt."""
        order = self.generate_order(selected_city, selected_country)
        order['discount'] = random.choice([0, 5, 10, 15, 20])
        return order

    def generate_order_with_shipping(self, selected_city, selected_country):
        """Generiert eine zufällige Bestellung mit Versandkosten."""
        order = self.generate_order(selected_city, selected_country)
        order['shipping_cost'] = random.uniform(5.0, 20.0)
        return order

    def generate_order_with_gift(self, selected_city, selected_country):
        """Generiert eine zufällige Bestellung mit Geschenkoption."""
        order = self.generate_order(selected_city, selected_country)
        order['gift'] = random.choice([True, False])
        return order

    def export_data(self, data, format='json'):
        """Exportiert die Daten in das angegebene Format."""
        if format == 'json':
            import json
            return json.dumps(data, indent=4)
        elif format == 'csv':
            import csv
            import io
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(data.keys())
            writer.writerow(data.values())
            return output.getvalue()
        else:
            raise ValueError("Unsupported format")

# Streamlit App
st.title('Test Data Generator')  # Titel der Streamlit App

generator = TestDataGenerator()  # Instanziierung des TestDataGenerator

# Auswahlbox zur Auswahl der Stadt
selected_city = st.selectbox('Select City', list(generator.city_postal_code_map.keys()))
selected_country = st.selectbox('Select Country', [generator.country])

# Dynamische Auswahl der Postleitzahl basierend auf der ausgewählten Stadt
selected_postal_code = generator.generate_postal_code(selected_city)

# Auswahlbox zur Auswahl des Datentyps
data_type = st.selectbox('Select data type to generate', ['order', 'order_with_discount', 'order_with_shipping', 'order_with_gift'])
if st.button('Generate Data'):
    if data_type == 'order':
        data = generator.generate_order(selected_city, selected_country)  # Generierung der Bestellung
    elif data_type == 'order_with_discount':
        data = generator.generate_order_with_discount(selected_city, selected_country)  # Generierung der Bestellung mit Rabatt
    elif data_type == 'order_with_shipping':
        data = generator.generate_order_with_shipping(selected_city, selected_country)  # Generierung der Bestellung mit Versandkosten
    elif data_type == 'order_with_gift':
        data = generator.generate_order_with_gift(selected_city, selected_country)  # Generierung der Bestellung mit Geschenkoption
    st.json(data)  # Anzeige der generierten Daten im JSON-Format

# Auswahlbox zur Auswahl des Exportformats
format = st.selectbox('Select export format', ['json', 'csv'])
if st.button('Export Data'):
    if data_type == 'order':
        data = generator.generate_order(selected_city, selected_country)  # Generierung der Bestellung
    elif data_type == 'order_with_discount':
        data = generator.generate_order_with_discount(selected_city, selected_country)  # Generierung der Bestellung mit Rabatt
    elif data_type == 'order_with_shipping':
        data = generator.generate_order_with_shipping(selected_city, selected_country)  # Generierung der Bestellung mit Versandkosten
    elif data_type == 'order_with_gift':
        data = generator.generate_order_with_gift(selected_city, selected_country)  # Generierung der Bestellung mit Geschenkoption
    try:
        exported_data = generator.export_data(data, format)  # Export der Daten
        st.text(exported_data)  # Anzeige der exportierten Daten
    except ValueError as e:
        st.error(f"Error: {str(e)}")  # Anzeige einer Fehlermeldung bei ungültigem Format