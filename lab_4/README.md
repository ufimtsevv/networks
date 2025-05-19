# 4: Book Parser API
Проект для парсинга книг с сайта books.toscrape.com с сохранением в PostgreSQL и REST API интерфейсом на FastAPI.

---
## Зависимости
  ```
  pip install -r requirements.txt
  ```
---

## Настройка базы данных
 1. Создаем базу данных
  ```
  CREATE DATABASE askona_parser;
  ```
 2. Создаем пользователя
  ```
  CREATE USER askona_user WITH PASSWORD 'password';
  ```
 3. Настраиваем права доступа
  ```
  ALTER DATABASE askona_parser OWNER TO askona_user;
  GRANT USAGE, CREATE ON SCHEMA public TO askona_user;
  ALTER DEFAULT PRIVILEGES IN SCHEMA public 
  GRANT ALL PRIVILEGES ON TABLES TO askona_user;
  GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO askona_user;
  ```
 4. Добавляем пользователя в `DATABASE_URL = "postgresql://askona_user:password@localhost/askona_parser"` в файле `database.py`

---
## Использование
 1. Запуск сервера  
  ```
  uvicorn main:app
  ```
 2. Запуск парсера
  ```
  curl "http://localhost:8000/parse?url=https://www.askona.ru/podushki/&count=5"
  ```
 3. Получение данных из БД
  ```
  curl "http://localhost:8000/products?limit=100"
  ```  

 Можно использовать адресную строку вашего браузера.  
 Для дополнительной информации можно перейти по `http://localhost:8000/docs`

---
## Пример данных
| Name                       | Type                  | Price | Rating    | Reviews | Link                                                                                                                       |
| -------------------------- | --------------------- | ----- | --------- | ------- | -------------------------------------------------------------------------------------------------------------------------- |
| Alpha Technology 2.0       | Анатомическая подушка | 6290  | 4.9       | 59      | https://www.askona.ru/podushki/alpha-technology-2.htm?SELECTED_HASH_SIZE=14-949c364bc5a9c58b3890a731dfb1688d               |
| Immuno Technology 2.0      | Анатомическая подушка | 7390  | 5         | 53      | https://www.askona.ru/podushki/immuno-technology-2-0.htm?SELECTED_HASH_SIZE=9-50cc4e3b66ea5c4084650af82e8ee63f             |
| Amma                       | Анатомическая подушка | 3190  | 5         | 12      | https://www.askona.ru/podushki/podushka-amma.htm?SELECTED_HASH_SIZE=60x40-992ec5c1c1b553c7a5d1e195eb53693f                 |
| Balance Basic              | Набивная подушка      | 2190  | 4.9       | 179     | https://www.askona.ru/podushki/balance-basic.htm?SELECTED_HASH_SIZE=70x50-a4b2635c44dc0d09c7b8a26c3bbfaca2                 |
| Omega серия Technology 2.0 |Анатомическая подушка  | 11990 | No rating | 0       | https://www.askona.ru/podushki/podushka-omega-technology-2-0.htm?SELECTED_HASH_SIZE=64x42-b938183c75de78232af997ab9ab77ec0 |