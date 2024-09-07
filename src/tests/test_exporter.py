import unittest
from unittest.mock import patch
from exporter import DataExporter
import os


class TestDataExporter(unittest.TestCase):

    @patch('exporter.pd.DataFrame.to_csv')
    @patch('exporter.os.makedirs')
    def test_export_to_csv(self, mock_makedirs, mock_to_csv):
        data = [{'name': 'Product', 'price': '1000'}]
        file_path = 'data/products.csv'
        exporter = DataExporter()
        exporter.export_to_csv(data, file_path)
        mock_makedirs.assert_called_once_with(
            os.path.dirname(file_path), exist_ok=True
         )
        mock_to_csv.assert_called_once_with(
            file_path, index=False, encoding='utf-8'
         )
        print("Export to CSV was successful.")

    @patch('exporter.pd.DataFrame.to_csv', side_effect=Exception(
            "Error exporting data"))
    def test_export_to_csv_failure(self, mock_to_csv):
        data = [{'name': 'Product', 'price': '1000'}]
        file_path = 'data/products.csv'
        exporter = DataExporter()
        with self.assertRaises(Exception):
            exporter.export_to_csv(data, file_path, raise_exception=True)


if __name__ == '__main__':
    unittest.main()
