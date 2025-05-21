import numpy as np
import matplotlib.pyplot as plt

# Генерируем два набора случайных данных
x = np.random.rand(50)
y = np.random.rand(50)

# Создаем диаграмму рассеяния
plt.scatter(x, y)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Диаграмма рассеяния двух наборов случайных данных')
plt.show()