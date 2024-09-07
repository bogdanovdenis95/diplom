# Product Scraper

## Описание

Этот проект представляет собой скрипт для скрейпинга данных о продуктах с веб-сайта и их экспорта в CSV-файл. Он использует библиотеку `Selenium` для извлечения динамически загружаемых данных и `BeautifulSoup` для парсинга HTML. Собранные данные сохраняются в CSV-файл с помощью `pandas`.

## Файлы

1. **`scraper.py`** - содержит класс `ProductScraper`, который выполняет скрейпинг продуктов с указанного веб-сайта. Он извлекает данные о продуктах, включая название, цену, рейтинг, описание, инструкции и страну происхождения.
2. **`exporter.py`** - содержит класс `DataExporter`, который экспортирует собранные данные в CSV-файл.
3. **`main.py`** - основной файл, который запускает процесс скрейпинга и экспорта данных.

## Установка

1. Убедитесь, что у вас установлен Python 3.11 или выше.
2. Установите необходимые зависимости:

   **`pip install -r requirements.txt`**

3. Установите веб-драйвер для Selenium (например, ChromeDriver). Убедитесь, что он доступен в PATH или укажите путь в scraper.py.

## Использование
1. Настройте параметры в main.py, если необходимо. Укажите базовый URL для скрейпинга и количество страниц для обработки.

2. Запустите скрипт main.py:

**`python main.py`**

Скрипт выполнит скрейпинг и сохранит данные в файл data/products.csv.

## Примеры использования
Для скрейпинга данных о продуктах с сайта goldapple.ru и сохранения в CSV-файл, просто запустите основной скрипт:

**`python main.py`**

После выполнения скрипта, файл data/products.csv будет содержать собранные данные о продуктах.

## Тестирование
Для запуска тестов используйте unittest и coverage:

**`coverage run -m unittest discover -s tests`**
**`coverage report`**

Тесты находятся в папке tests. Они проверяют корректность работы методов скрейпера.

### Примечания

1. **Настройка драйвера:** Убедитесь, что путь к веб-драйверу (`driver_path`) в `scraper.py` правильно указан. Если вы используете другой драйвер или установили его в другой директории, отредактируйте путь соответственно.
2. **Тестирование:** Если у вас есть отдельные тестовые скрипты или дополнительные инструкции по запуску тестов, не забудьте включить их в раздел `Тестирование`.
3. **CSV-файл:** products.csv файл в директории проекта является примером выполнения кода и содержит информацию о данных продуктов за первые 10 страниц. Количество страниц для обработки можно указать в файле **`main.py`**
