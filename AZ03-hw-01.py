import numpy as np
import matplotlib.pyplot as plt

# Параметры нормального распределения
mean = 0
std_dev = 1
num_samples = 1000

# Генерация случайных чисел
data = np.random.normal(mean, std_dev, num_samples)

# Построение гистограммы
plt.hist(data, bins=30, edgecolor='black')
plt.title('Гистограмма случайных данных')
plt.xlabel('Значение')
plt.ylabel('Частота')
plt.show()