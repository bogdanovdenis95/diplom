from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import requests


class ProductScraper:
    def __init__(self, base_url, pages=1):
        self.base_url = base_url
        self.pages = pages
        self.max_retries = 3  # Максимальное количество попыток поиска

    def get_html(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            print(f"Successfully fetched URL: {url}")  # Отладочное сообщение
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def get_html_2(self, url):
        options = Options()
        options.headless = False

        driver_path = "/opt/chromedriver"  # Укажите путь к веб-драйверу

        driver = webdriver.Chrome(
            service=Service(driver_path),  # Явное указание пути
            options=options
        )

        driver.set_window_size(120, 800)
        driver.get(url)
        html = driver.page_source
        driver.quit()
        return html

    def parse_product_list(self, html):
        if not html:
            print("No HTML content to parse.")  # Отладочное сообщение
            return []

        print("Parsing product list...")  # Отладочное сообщение
        soup = BeautifulSoup(html, 'lxml')
        products = []

        div_tags = soup.find_all('a', class_='_2inst yLDf5 RmO7n')

        for div_tag in div_tags:
            href = div_tag.get('href')
            if href:
                product_url = f"https://goldapple.ru{href}"
                products.append(product_url)
            else:
                print(f"Missing href in tag: {div_tag}")

        all_product_details = []
        for product_url in products:
            html = self.get_html_2(product_url)
            if html:
                details = self.parse_product_details(html, product_url)
                all_product_details.extend(details)
            else:
                print(f"Skipping product URL {product_url} due to error.")

        return all_product_details

    def parse_product_details(self, html, product_url):
        if not html:
            print("No HTML content to parse for product details.")
            return []

        attempts = 0
        product_details = []

        while attempts < self.max_retries:
            soup = BeautifulSoup(html, 'lxml')
            name_elements = soup.find_all('span', class_="u37GV")
            price_elements = soup.find('div', class_="VSJl8 EQY7P")
            rate_elements = soup.find('div', class_="_6jySn")
            description_element = soup.find(
                lambda tag: (
                    tag.name == 'div' and tag.get('value') == 'Description_0'
                    and tag.get('text') == 'описание'
                )
            )
            instruction_element = soup.find(
                lambda tag: (
                    tag.name == 'div' and tag.get('value') == 'Text_1'
                    and tag.get('text') == 'применение'
                )
            )
            country_element = soup.find(
                lambda tag: (
                    tag.name == 'div' and tag.get('value') == 'Text_4'
                    and tag.get('text') == 'Дополнительная информация'
                )

            )

            if len(name_elements) > 0:
                for name_elem in name_elements:
                    product_name = name_elem.get_text(strip=True)

                    # Инициализируем значения по умолчанию
                    product_price = "N/A"  # Если цена не найдена
                    product_rate = "N/A"   # Если рейтинг не найден
                    product_description = "N/A"   # Если описание не найдено
                    product_instructions = "N/A"  # Если инструкция не найдена
                    product_country = "N/A"  # Если страна не найдена

                    # Получаем цену, если элемент существует
                    if price_elements:
                        product_price = price_elements.get_text(
                            strip=True).replace('₽', '').strip()

                    # Получаем рейтинг, если элемент существует
                    if rate_elements:
                        rate_element = rate_elements.find(
                            'div', class_="kBgM7")
                        if rate_element:
                            product_rate = rate_element.get_text(strip=True)

                    # Получаем описание, если элемент существует
                    if description_element:
                        description_text = description_element.find(
                            'div', class_='G3Bhc')
                        if description_text:
                            product_description = description_text.get_text(
                                strip=True)

                    # Получаем инструкцию, если элемент существует
                    if instruction_element:
                        product_instructions = instruction_element.get_text(
                            strip=True)

                    # Получаем страну происхождения, если элемент существует
                    if country_element:
                        country_text = country_element.find(
                            'div', class_='G3Bhc')
                        if country_text:
                            text = country_text.get_text(
                                separator=' ', strip=True)
                            # Разбиваем текст на строки и находим нужную
                            lines = text.split('страна происхождения')
                            if len(lines) > 1:
                                # Получаем текст после 'страна происхождения'
                                country_info = lines[1].split('<')[0].strip()
                                country_info = BeautifulSoup(
                                    country_info, 'lxml').text
                                country_info = country_info.split()[0]
                                product_country = country_info
                            else:
                                print(
                                    "Информация о стране не найдена.")
                        else:
                            print("Не удалось найти информацию о стране")

                    # Добавляем информацию о продукте в список
                    product_details.append({
                        'product_url': product_url,
                        'name': product_name,
                        'price': product_price,
                        'rate': product_rate,
                        'description': product_description,
                        'instructions': product_instructions,
                        'country': product_country
                    })
                break
            else:
                print("No product names found, retrying")
                attempts += 1
                time.sleep(1)  # Подождите 1 секунду перед повторной попыткой

        if len(product_details) == 0:
            print("Failed to find product details after several attempts.")

        return product_details

    def scrape(self):
        all_products = []
        for page in range(1, self.pages + 1):
            url = f"{self.base_url}?p={page}"
            print(f"Scraping page {page}: {url}")
            html = self.get_html(url)
            if html:
                products = self.parse_product_list(html)
                all_products.extend(products)
            else:
                print(f"Skipping page {page} due to error.")

        print(f"Scraping completed. Total products found: {len(all_products)}")
        return all_products
