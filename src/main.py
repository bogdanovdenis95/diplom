from scraper import ProductScraper
from exporter import DataExporter


def main():
    base_url = "https://goldapple.ru/parfjumerija"
    pages_to_scrape = 10

    scraper = ProductScraper(base_url, pages=pages_to_scrape)
    products = scraper.scrape()

    exporter = DataExporter()
    exporter.export_to_csv(products, 'data/products.csv')


if __name__ == "__main__":
    main()
