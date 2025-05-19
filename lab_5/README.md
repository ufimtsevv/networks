
# 5: Book URL Saver with Docker
Простое приложение на FastAPI для сохранения и получения URL из PostgreSQL, развернутое в двух Docker-контейнерах.

---
## Запуск
  ```
docker network create book_network
docker run -d --name db --network book_network -e POSTGRES_USER=book_user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=book_parser -v ${PWD}/db/init.sql:/docker-entrypoint-initdb.d/init.sql -p 5432:5432 postgres:13
cd app
docker build -t url_saver_app .
docker run -d --name app --network book_network -p 5000:5000 url_saver_app
  ```
---
## Использование API
Сохранение URL:  
  ```
  GET /save_url?url=<your_url>
  ```
  - Пример: 
    ```
    curl "http://localhost:5000/save_url?url=http://example.com"
    ```
Получение все URL:
  ```
  GET /get_urls
  ```
  - Пример: 
    ```
    curl "http://localhost:5000/get_urls"
    ```
Документация: http://localhost:5000/docs

---