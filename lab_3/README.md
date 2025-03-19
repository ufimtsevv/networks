# 3: Парсер сайта Books to Scrape

Этот скрипт предназначен для парсинга данных с сайта http://books.toscrape.com/. Скрипт собирает информацию о книгах (название, цена, рейтинг, ссылка) со всех страниц сайта. Данные сохраняются в CSV-файл.

## Установка

Скачайте или склонируйте этот репозиторий:

```bash
  git clone https://github.com/ufimtsevv/networks.git
  cd lab_3
```
Установите зависимости:

```bash
  pip install -r requirements.txt
```

## Использование

Запустите скрипт:

```bash
  python parser.py
```

После завершения работы скрипта данные будут сохранены в файл `books.csv`.

## Формат выходного файла

Файл `books.csv` будет содержать данные в следующем формате:

| title | price | rating | link |
| ------- | --- | --- | ---------- |
| A Light in the Attic | £51.77 | Three | https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html |
| Tipping the Velvet | £53.74 | One | https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html |
| Soumission | £50.10 | One | https://books.toscrape.com/catalogue/soumission_998/index.html |
| Sharp Objects | £47.82 | Four | https://books.toscrape.com/catalogue/sharp-objects_997/index.html |