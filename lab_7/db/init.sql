DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'book_user') THEN
        CREATE USER book_user WITH PASSWORD 'password';
    END IF;
END
$$;

CREATE DATABASE book_parser;
GRANT ALL PRIVILEGES ON DATABASE book_parser TO book_user;