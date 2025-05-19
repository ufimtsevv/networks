
# 4: Book Parser API
Проект для парсинга книг с сайта `books.toscrape.com` с сохранением в PostgreSQL и REST API интерфейсом на FastAPI.

---
## Установка
Установите зависимости:
  ```
  pip install -r requirements.txt
  ```
Создайте БД и пользователя в PostgreSQL:
  ```
  CREATE DATABASE book_parser;
  CREATE USER book_user WITH PASSWORD 'password'; 
  ALTER DATABASE book_parser OWNER TO book_user;
  GRANT ALL PRIVILEGES ON DATABASE book_parser TO book_user;
  ```
Настройте подключение в файле `.env`:
  ```
  DATABASE_URL=postgresql://book_user:password@localhost/book_parser
  ```
---
## Использование
Запуск сервера:  
  ```
  uvicorn main:app --reload
  ```
---
## API Endpoints
Основные методы:
- `GET \` - информация о API
- `GET /parse` - запуск парсера
    - Параметры:
        - `url` - URL для парсинга
        - `count` - количество книг (по умолчанию 5)
- `GET /books` - получение книг из БД
    - Параметры:
        - `limit` - лимит записей (по умолчанию 100)

Документация API:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---
## Структура данных
| title                      | price                 | rating | link                                                                                                                  |
| -------------------------- | --------------------- | ----- | --------- |
| A Light in the Attic       | 51.77 | Three | https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html             |
| Tipping the Velvet      | 53.74 | One  | https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html            |
| Soumission                      | 50.1 | One  | https://books.toscrape.com/catalogue/soumission_998/index.html              |
