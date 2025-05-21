from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import matplotlib.pyplot as plt
import re

# Инициализация Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = 'https://www.divan.ru/category/pramye-divany'

try:
    driver.get(url)
    time.sleep(5)

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