import datetime
import sys
import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from Bench_Projekt_API import app, TestDataGenerator
import json
import pandas as pd
from openpyxl import Workbook
import os
from unittest.loader import TestLoader
from unittest.runner import TextTestRunner

class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.wb = Workbook()
        cls.ws = cls.wb.active
        cls.ws.append(["Test Name", "Status", "Error Message"])

    def setUp(self):
        self.client = TestClient(app)
        self.generator = TestDataGenerator()

    def log_result(self, test_name, status, error_message=""):
        self.ws.append([test_name, status, error_message])

    @classmethod
    def tearDownClass(cls):
        # Report speichern
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        project_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(project_dir, f"test_report_{timestamp}.xlsx")
        cls.wb.save(file_path)

    def test_export_functions(self):
        # TestExportFunctions instanziieren
        test_export = unittest.TestLoader().loadTestsFromTestCase(TestExportFunctions)

        # TestRunner verwenden, um Tests auszuführen und die Ergebnisse zu sammeln
        runner = TextTestRunner(verbosity=2)
        result = runner.run(test_export)

        # Fehler und Fehlschläge extrahieren und in den Excel-Bericht schreiben
        for test_case, error in result.errors:
            if test_case is not None:  # Stelle sicher, dass test_case nicht None ist
                test_name = test_case._testMethodName  # Testname
                self.log_result(test_name, "Failed", str(error))  # Fehlernachricht

        for test_case, failure in result.failures:
            if test_case is not None:  # Stelle sicher, dass test_case nicht None ist
                test_name = test_case._testMethodName  # Testname
                self.log_result(test_name, "Failed", str(failure))  # Fehlermeldung

        # Erfolgreiche Tests aufzeichnen
        for test_case in test_export:
            if test_case not in result.errors and test_case not in result.failures:
                if test_case is not None:  # Stelle sicher, dass test_case nicht None ist
                    test_name = test_case._testMethodName  # Testname
                    self.log_result(test_name, "Passed")


    def test_generate_registration(self):
        try:
            response = self.client.get("/generate/registrierung/5")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json()), 5)
            self.log_result("test_generate_registration", "Passed")
        except AssertionError as e:
            self.log_result("test_generate_registration", "Failed", str(e))

    def test_generate_login(self):
        try:
            response = self.client.get("/generate/login/3")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json()), 3)
            self.log_result("test_generate_login", "Passed")
        except AssertionError as e:
            self.log_result("test_generate_login", "Failed", str(e))

    def test_generate_order(self):
        try:
            response = self.client.get("/generate/bestellung/2")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json()), 2)
            self.log_result("test_generate_order", "Passed")
        except AssertionError as e:
            self.log_result("test_generate_order", "Failed", str(e))

    def test_generate_profile(self):
        try:
            response = self.client.get("/generate/profil/4")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json()), 4)
            self.log_result("test_generate_profile", "Passed")
        except AssertionError as e:
            self.log_result("test_generate_profile", "Failed", str(e))


    @patch.object(TestDataGenerator, 'generate_username', return_value='testuser')
    def test_mocked_generate_username(self, mock_username):
        try:
            username = self.generator.generate_username()
            self.assertEqual(username, 'testuser')
            self.log_result("test_mocked_generate_username", "Passed")
        except AssertionError as e:
            self.log_result("test_mocked_generate_username", "Failed", str(e))

    @patch.object(TestDataGenerator, 'generate_product', return_value='Latte')
    def test_mocked_generate_product(self, mock_product):
        try:
            product = self.generator.generate_product()
            self.assertEqual(product, 'Latte')
            self.log_result("test_mocked_generate_product", "Passed")
        except AssertionError as e:
            self.log_result("test_mocked_generate_product", "Failed", str(e))

    @patch.object(TestDataGenerator, 'generate_username', return_value='')
    def test_mocked_generate_empty_username(self, mock_username):
        try:
            username = self.generator.generate_username()
            self.assertEqual(username, '')  # Leerer Benutzername erwartet
            self.log_result("test_mocked_generate_empty_username", "Passed")
        except AssertionError as e:
            self.log_result("test_mocked_generate_empty_username", "Failed", str(e))

    @patch.object(TestDataGenerator, 'generate_email', return_value='invalidemail.com')
    def test_mocked_generate_invalid_email(self, mock_email):
        try:
            email = self.generator.generate_email()
            self.assertEqual(email, 'invalidemail.com')  # Ungültige E-Mail erwartet
            self.log_result("test_mocked_generate_invalid_email", "Passed")
        except AssertionError as e:
            self.log_result("test_mocked_generate_invalid_email", "Failed", str(e))


    def test_generate_invalid_type(self):
        try:
            response = self.client.get("/generate/invalid/5")
            self.assertEqual(response.status_code, 400)
            self.log_result("test_generate_invalid_type", "Passed")
        except AssertionError as e:
            self.log_result("test_generate_invalid_type", "Failed", str(e))

    def test_generate_zero_records(self):
        try:
            response = self.client.get("/generate/order/0")
            self.assertEqual(response.status_code, 400)
            self.log_result("test_generate_zero_records", "Passed")
        except AssertionError as e:
            self.log_result("test_generate_zero_records", "Failed", str(e))

    def test_generate_negative_records(self):
        try:
            response = self.client.get("/generate/order/-3")
            self.assertEqual(response.status_code, 400)
            self.log_result("test_generate_negative_records", "Passed")
        except AssertionError as e:
            self.log_result("test_generate_negative_records", "Failed", str(e))

    def test_export_invalid_format(self):
        try:
            response = self.client.get("/export_data/xml")
            self.assertEqual(response.status_code, 404)  # Wenn der Endpunkt nicht existiert
            self.log_result("test_export_invalid_format", "Passed")
        except AssertionError as e:
            self.log_result("test_export_invalid_format", "Failed", str(e))

    def test_generate_invalid_endpoint(self):
        try:
            response = self.client.get("/generate/unknown/5")
            self.assertEqual(response.status_code, 400)
            self.log_result("test_generate_invalid_endpoint", "Passed")
        except AssertionError as e:
            self.log_result("test_generate_invalid_endpoint", "Failed", str(e))

    def test_large_data_request(self):
        # Test the generation of a large number of records
        try:
            response = self.client.get("/generate/bestellung/10000")
            self.assertEqual(response.status_code, 400)
            self.log_result("test_large_data_request", "Passed")
        except AssertionError as e:
            self.log_result("test_large_data_request", "Failed", str(e))


    def test_generate_invalid_method(self):
        # Test the generation with an invalid method
        try:
            response = self.client.post("/generate/bestellung/5")
            self.assertEqual(response.status_code, 405)
            self.log_result("test_generate_invalid_method", "Passed")
        except AssertionError as e:
            self.log_result("test_generate_invalid_method", "Failed", str(e))

    def test_export_empty_data(self):
        # Test the export of empty data
        try:
            response = self.client.get("/export_data/json")
            self.assertEqual(response.status_code, 404)
            self.log_result("test_export_empty_data", "Passed")
        except AssertionError as e:
            self.log_result("test_export_empty_data", "Failed", str(e))

    def test_generate_non_integer(self):
        # Test the generation with a non-integer number of records
        try:
            response = self.client.get("/generate/bestellung/abc")
            self.assertEqual(response.status_code, 422)
            self.log_result("test_generate_non_integer", "Passed")
        except AssertionError as e:
            self.log_result("test_generate_non_integer", "Failed", str(e))


class TestExportFunctions(unittest.TestCase):
    def setUp(self):
        # Setup für die Testumgebung
        self.generator = TestDataGenerator()
        self.sample_data = [
            {
                'produkt': 'Kaffee',
                'menge': 2,
                'preis': '4.00 €',
            },
            {
                'produkt': 'Espresso',
                'menge': 1,
                'preis': '2.00 €',
            },
        ]
        self.df = pd.DataFrame(self.sample_data)

    def log_result(self, test_name, status, error_message=""):
        # Verwende die log_result Methode der TestAPI-Klasse, um den Teststatus zu protokollieren
        # Da wir von außen darauf zugreifen müssen, sollte log_result hier über `TestAPI` erfolgen
        TestAPI().log_result(test_name, status, error_message)

    def test_export_json(self):
        try:
            # Test export to JSON
            json_data = self.generator.export_data(self.df, format='json')
            expected_json = '[\n    {\n        "produkt": "Kaffee",\n        "menge": 2,\n        "preis": "4.00 €"\n    },\n    {\n        "produkt": "Espresso",\n        "menge": 1,\n        "preis": "2.00 €"\n    }\n]'
            self.assertEqual(json_data.strip(), expected_json)
            self.log_result("test_export_json", "Passed")
        except AssertionError as e:
            self.log_result("test_export_json", "Failed", str(e))

    def test_export_csv(self):
        try:
            # Exportiere die Daten im CSV-Format
            csv_data = self.generator.export_data(self.df, format='csv')
            csv_data = csv_data.replace('\r\n', '\n')  # Setze Zeilenumbrüche auf \n
            expected_csv = 'produkt,menge,preis\nKaffee,2,4.00 €\nEspresso,1,2.00 €\n'
            self.assertEqual(csv_data.strip(), expected_csv.strip())
            self.log_result("test_export_csv", "Passed")
        except AssertionError as e:
            self.log_result("test_export_csv", "Failed", str(e))

    def test_export_xlsx(self):
        try:
            # Test export to XLSX
            xlsx_data = self.generator.export_data(self.df, format='xlsx')
            self.assertGreater(len(xlsx_data), 0)
            self.log_result("test_export_xlsx", "Passed")
        except AssertionError as e:
            self.log_result("test_export_xlsx", "Failed", str(e))



if __name__ == "__main__":
    unittest.main()
