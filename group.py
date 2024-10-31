from datetime import datetime
# import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
from collections import defaultdict
import MetaTrader5 as mt5
import sys
import json
import os

register_matplotlib_converters()  # Регистрация конвертеров для корректной работы с датами в графиках

# Очистка консоли (для Windows)
os.system('cls')

path_to_terminal = r'C:\Program Files\MetaTrader 5\terminal64.exe'
# Инициализация MetaTrader5
if not mt5.initialize(path_to_terminal):
    print("Ошибка инициализации MetaTrader5")
    sys.exit()

# Получение доступных символов
symbols = mt5.symbols_get()
mt5.shutdown()

# Проверка наличия символов
if not symbols:
    print("Нет доступных символов.")
    sys.exit()

# Словари для группировки символов
grouped_symbls = defaultdict(list)  # Использование defaultdict для автоматической инициализации списков
stocks_symbls = []

# Разделение символов по группам
for symbol in symbols:
    name = symbol.name.replace('.', '')  # Удаление точек из имени символа
    if len(name) == 6:
        if name.endswith('JPY'):
            grouped_symbls['JPY'].append(name)
        group = name[:3]  # Определение группы по первым трем символам
        grouped_symbls[group].append(name)
    else:
        stocks_symbls.append(name)  # Добавление акций в отдельный список

# Удаление групп с менее чем двумя символами и сохранение их в акции
keys_to_remove = [key for key, values in grouped_symbls.items() if len(values) < 2]
for key in keys_to_remove:
    stocks_symbls.append(grouped_symbls[key][-1])  # Добавление последнего символа в список акций
    del grouped_symbls[key]

# Определение ресурсов и акций
resource_symbls = [stock for stock in stocks_symbls if stock[-3:] in grouped_symbls]
stocks_symbls = [stock for stock in stocks_symbls if stock[-3:] not in grouped_symbls]

# Удаление некорректных ресурсов из списка ресурсов
wrong_resource = set(stock for stock in resource_symbls if any(stock in values for values in grouped_symbls.values()))
resource_symbls = [stock for stock in resource_symbls if stock not in wrong_resource]

# Добавление ресурсов и акций в общий словарь групп
grouped_symbls['resource'] = resource_symbls
grouped_symbls['stocks'] = stocks_symbls

# Вывод групп символов на экран
for keyd, values in grouped_symbls.items():
    print(f'{keyd}')
    for value in values:
        print(f'    {value}')

# Сохранение групп символов в файл JSON
with open('grouped_symbols.json', 'w') as json_file:
    json.dump(grouped_symbls, json_file, indent=4)
