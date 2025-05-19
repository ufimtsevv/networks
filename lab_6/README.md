
# 6: Book URL Saver with Nginx Proxy
Простое приложение на FastAPI с PostgreSQL и Nginx в Docker-контейнерах.

---
## Запуск
  ```
docker network create book_network
docker run -d --name db --network book_network -e POSTGRES_USER=book_user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=book_parser -v ${PWD}/db/init.sql:/docker-entrypoint-initdb.d/init.sql -p 5432:5432 postgres:13
cd app
docker build -t url_saver_app .
docker run -d --name app --network book_network url_saver_app
cd ..
docker run -d --name nginx --network book_network -p 80:80 -v ${PWD}/nginx/nginx.conf:/etc/nginx/conf.d/default.conf nginx:alpine
  ```
---
## Использование API
Сохранение URL:  
  ```
  GET /save_url?url=<your_url>
  ```
  - Пример: 
    ```
    curl "http://localhost/save_url?url=http://example.com"
    ```
Получение все URL:
  ```
  GET /get_urls
  ```
  - Пример: 
    ```
    curl "http://localhost/get_urls"
    ```
Документация: http://localhost/docs

---