import unittest
import requests
from unittest.mock import patch, MagicMock
from scraper import ProductScraper


class TestProductScraper(unittest.TestCase):

    @patch('scraper.requests.get')
    def test_get_html_success(self, mock_get):
        mock_get.return_value = MagicMock(
            text='<html></html>', status_code=200)
        scraper = ProductScraper("https://goldapple.ru/parfjumerija")
        result = scraper.get_html("https://goldapple.ru/parfjumerija")
        self.assertEqual(result, '<html></html>')

    @patch('scraper.requests.get')
    def test_get_html_failure(self, mock_get):
        mock_get.side_effect = requests.RequestException("Error")
        scraper = ProductScraper("https://example.com")
        result = scraper.get_html("https://example.com")
        self.assertIsNone(result)

    @patch('scraper.webdriver.Chrome')
    def test_get_html_2(self, mock_chrome):
        mock_driver = MagicMock()
        mock_driver.page_source = '<html></html>'
        mock_chrome.return_value = mock_driver
        scraper = ProductScraper("https://example.com")
        result = scraper.get_html_2("https://example.com")
        self.assertEqual(result, '<html></html>')

    def test_parse_product_details(self):
        html = '''
        <span class="u37GV">Product Name</span>
        <div class="VSJl8 EQY7P">1000 ₽</div>
        <div class="_6jySn"><div class="kBgM7">4.5</div></div>
        <div value="Description_0"
        text="описание"><div class="G3Bhc">Description text</div></div>
        <div value="Text_1"
        text="применение">Instructions text</div>
        <div value="Text_4" text="Дополнительная информация">
        <div class="G3Bhc">Country text страна происхождения Country
        </div></div>
        '''
        scraper = ProductScraper("https://example.com")
        result = scraper.parse_product_details(
            html, "https://example.com/product")
        self.assertEqual(result, [{
            'product_url': "https://example.com/product",
            'name': 'Product Name',
            'price': '1000',
            'rate': '4.5',
            'description': 'Description text',
            'instructions': 'Instructions text',
            'country': 'Country'
        }])

    @patch.object(ProductScraper, 'get_html', return_value='<html></html>')
    @patch.object(ProductScraper, 'parse_product_list', return_value=[
        "https://example.com/19000152685-aura-soleil",
        "https://example.com/19000004549-perfume-vanilla-blend"
    ])
    @patch.object(ProductScraper, 'parse_product_details', return_value=[
        {'product_url':
         'https://example.com/19000152685-aura-soleil',
         'name': 'Product Name'},
        {'product_url':
         'https://example.com/19000004549-perfume-vanilla-blend',
         'name': 'Product Name'}
    ])
    def test_scrape(self, mock_parse_details, mock_parse_list, mock_get_html):
        scraper = ProductScraper("https://goldapple.ru/parfjumerija", pages=1)
        result = scraper.scrape()
        self.assertEqual(result, [
            "https://example.com/19000152685-aura-soleil",
            "https://example.com/19000004549-perfume-vanilla-blend"
        ])


if __name__ == '__main__':
    unittest.main()
