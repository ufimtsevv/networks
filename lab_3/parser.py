from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import time
import csv


def init_driver():
    """Инициализирует драйвер Selenium. Если драйвер не найден, автоматически скачивает его."""
    try:
        driver = webdriver.Chrome(options=options)
        return driver
    except WebDriverException:
        print("Драйвер не найден. Автоматическая загрузка и установка...")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        print("Драйвер успешно установлен.")
        return driver

def parse_books(driver):
    """Парсит книги на текущей странице."""
    books = []
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ol.row li.col-xs-6"))
    )
    book_elements = driver.find_elements(By.CSS_SELECTOR, "ol.row li.col-xs-6")
    for book in book_elements:
        try:
            title = book.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("title")
            price = book.find_element(By.CSS_SELECTOR, "div.product_price p.price_color").text
            rating = book.find_element(By.CSS_SELECTOR, "p.star-rating").get_attribute("class").split()[-1]
            link = book.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("href")
            books.append({"title": title, "price": price, "rating": rating, "link": link})
        except Exception as e:
            print(f"Ошибка при парсинге книги: {e}")
    return books

def go_to_next_page(driver):
    """Переходит на следующую страницу, если она существует."""
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, "li.next a")
        next_button.click()
        time.sleep(2)
        return True
    except Exception as e:
        print(f"Пагинация завершена: {e}")
        return False

def save_to_csv(data, filename="data/books.csv"):
    """Сохраняет данные в CSV-файл."""
    keys = data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = init_driver()
    driver.get("http://books.toscrape.com/")
    time.sleep(2)

    all_books = []
    while True:
        books = parse_books(driver)
        all_books.extend(books)
        print(f"Парсинг страницы завершён. Найдено книг: {len(books)}")
        if not go_to_next_page(driver):
            break

    save_to_csv(all_books)
    print(f"Всего найдено книг: {len(all_books)}. Данные сохранены в books.csv")
    driver.quit()