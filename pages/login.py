import streamlit as st
import requests
import json

st.title("🔐 Login Seite")

# Eingabefelder für Benutzername und Passwort
username = st.text_input("👤 Benutzername", key="username")
password = st.text_input("🔑 Passwort", type="password", key="password")

# Login-Button
if st.button("Anmelden"):
    # Ausgabe von Benutzername und Passwort im JSON-Format
    st.json({"Benutzername": username, "passwort": password})

    # API-Anfrage senden
    api_url = "http://127.0.0.1:8000/login"
    response = requests.post(api_url, json={"Benutzername": username, "passwort": password})