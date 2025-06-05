"""
Test automatici per le funzioni principali di definitions.py
"""
import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from datetime import datetime
import definitions

class TestDefinitions(unittest.TestCase):
    def setUp(self):
        # Setup base per i test
        self.browser = MagicMock()
        self.csv_name = 'test.csv'
        self.label_csv_name = 'labels.csv'
        # Crea un DataFrame di esempio
        self.df = pd.DataFrame({
            'Data': ['2024-06-01 12:00:00'],
            'URL': ['https://test.url'],
            'Beneficiario': ['Test'],
            'Importo': [100.0],
            'Categoria': ['TestCat'],
            'Tags': ['#INCO'],
            'NewTags': ['INCO']
        })
        self.df.to_csv(self.csv_name, index=False)
        pd.DataFrame({'label': ['INCO']}).to_csv(self.label_csv_name, index=False)

    def tearDown(self):
        import os
        if os.path.exists(self.csv_name):
            os.remove(self.csv_name)
        if os.path.exists(self.label_csv_name):
            os.remove(self.label_csv_name)

    def test_get_last_time(self):
        result = definitions.get_last_time(self.csv_name)
        self.assertEqual(result, '2024-06-01 12:00:00')

    def test_get_last_url(self):
        result = definitions.get_last_url(self.csv_name)
        self.assertEqual(result, 'https://test.url')

    def test_get_last_beneficiary(self):
        result = definitions.get_last_beneficiary(self.csv_name)
        self.assertEqual(result, 'Test')

    def test_get_last_import(self):
        result = definitions.get_last_import(self.csv_name)
        self.assertEqual(result, 100.0)

    def test_get_NewTag_string(self):
        tags = '#INCO'
        result = definitions.get_NewTag_string(tags, self.label_csv_name)
        self.assertEqual(result, 'INCO')

    @patch('definitions.WebDriverWait')
    def test_login_exception(self, mock_wait):
        # Simula eccezione
        self.browser.find_element.side_effect = Exception('error')
        with self.assertLogs(level='ERROR') as log:
            definitions.login(self.browser, 'user', 'pass')
        self.assertTrue(any('problem' in str(m).lower() or 'error' in str(m).lower() for m in log.output))
if __name__ == "__main__":
    unittest.main()
