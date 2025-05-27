from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import matplotlib.pyplot as plt
import re

# Инициализация Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
url = 'https://www.divan.ru/category/pramye-divany'

# driver.set_window_size(600, 800)

try:
    driver.get(url)
    wait = WebDriverWait(driver, 20)

    # Ожидание загрузки карточек товаров

    products = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="product-card"]')))



    data = []
    for product in products:
        try:
            # Повторный запрос элементов, чтобы избежать "устаревшей ссылки"
            name_element = product.find_element(By.CSS_SELECTOR, '[itemprop="name"]')
            name = name_element.text

            price_text_element = product.find_element(By.CSS_SELECTOR, '[data-testid="price"]')
            price_text = price_text_element.text

            price_numbers = re.findall(r'\d+', price_text)
            if price_numbers:
                price = int(''.join(price_numbers))
                data.append({'name': name, 'price': price})

            # Ограниченный вывод первых 10 товаров для проверки
            if len(data) <= 10:
                print(f"Товар: {name} | Цена: {price}")

        except (NoSuchElementException, StaleElementReferenceException):
            continue

    if data:
        # Создание DataFrame и запись в CSV
        df = pd.DataFrame(data)
        df.to_csv('divans.csv', index=False, encoding='utf-8')

        # Запись всех данных в текстовый файл
        with open("divans_log.txt", "w", encoding="utf-8") as f:
            for item in data:
                f.write(f"{item['name']} - {item['price']}\n")

        # Вычисление средней цены
        mean_price = df['price'].mean()
        print(f"Средняя цена дивана: {mean_price:.2f}")

        # Построение гистограммы
        plt.hist(df['price'], bins=20, color='green', edgecolor='black')
        plt.xlabel('Цены')
        plt.ylabel('Количество диванов')
        plt.title('Гистограмма цен на диваны')
        plt.show()
    else:
        print("Нет данных для анализа.")

finally:
    driver.quit()
