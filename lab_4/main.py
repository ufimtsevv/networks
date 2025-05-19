import logging
import os
import time
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Book Parser API")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://book_user:password@localhost/book_parser"
)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(Float)
    rating = Column(String)
    link = Column(String)


class BookResponse(BaseModel):
    title: str
    price: float
    rating: str
    link: str

    class Config:
        from_attributes = True


Base.metadata.create_all(bind=engine)

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")


def init_driver():
    try:
        return webdriver.Chrome(options=options)
    except WebDriverException:
        return webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )


def parse_books(driver, url: str, count: int = 5):
    driver.get(url)
    time.sleep(3)
    books = []

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ol.row li.col-xs-6"))
        )
        
        book_elements = driver.find_elements(By.CSS_SELECTOR, "ol.row li.col-xs-6")[:count]
        
        for book in book_elements:
            try:
                title = book.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("title")
                price = float(
                    book.find_element(
                        By.CSS_SELECTOR, "div.product_price p.price_color"
                    ).text.replace("£", "")
                )
                rating = book.find_element(
                    By.CSS_SELECTOR, "p.star-rating"
                ).get_attribute("class").split()[-1]
                link = book.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("href")
                
                books.append({
                    "title": title,
                    "price": price,
                    "rating": rating,
                    "link": link
                })
            except Exception as e:
                logger.error(f"Error parsing book: {e}")
    except Exception as e:
        logger.error(f"Page parsing error: {e}")
    
    return books


def save_to_db(books: List[dict]):
    db = SessionLocal()
    try:
        for book in books:
            db_book = Book(**book)
            db.add(db_book)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        db.close()


@app.get("/parse")
async def parse_books_endpoint(
    url: str = "http://books.toscrape.com/",
    count: int = 5
):
    try:
        driver = init_driver()
        books = parse_books(driver, url, count)
        save_to_db(books)
        driver.quit()
        return {"status": "success", "books_parsed": len(books)}
    except Exception as e:
        logger.error(f"Parsing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/books", response_model=List[BookResponse])
async def get_books(limit: int = 100):
    db = SessionLocal()
    try:
        books = db.query(Book).limit(limit).all()
        return books
    except Exception as e:
        logger.error(f"Database query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Book Parser API. Use /parse?url=... to parse books."}