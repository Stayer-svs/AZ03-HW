from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import matplotlib.pyplot as plt
import re

# Инициализация Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = 'https://www.divan.ru/category/pryamye-divany'

try:
    driver.get(url)

    # Явное ожидание появления элементов
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.product-card'))
        )
    except TimeoutException:
        print("Элементы не загрузились в течение ожидаемого времени.")
        driver.quit()
        exit()

    time.sleep(5)  # Дополнительное ожидание для полной загрузки

    products = driver.find_elements(By.CSS_SELECTOR, 'div.product-card')

    data = []
    for product in products:
        try:
            name = product.find_element(By.CSS_SELECTOR, 'div.product-card__title').text
            price_text = product.find_element(By.CSS_SELECTOR, 'div.product-card__price').text
            price_numbers = re.findall(r'\d+', price_text)
            if price_numbers:
                price = int(''.join(price_numbers))
                data.append({'name': name, 'price': price})
                print(f"Товар: {name} | Цена: {price}")
        except NoSuchElementException:
            continue

    if data:
        df = pd.DataFrame(data)
        df.to_csv('divans.csv', index=False)
        mean_price = df['price'].mean()
        print(f"Средняя цена дивана: {mean_price:.2f}")

        plt.hist(df['price'], bins=20, color='green', edgecolor='black')
        plt.xlabel('Цены')
        plt.ylabel('Количество диванов')
        plt.title('Гистограмма цен на диваны')
        plt.show()
    else:
        print("Нет данных для анализа.")

finally:
    driver.quit()
