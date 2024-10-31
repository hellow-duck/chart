import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

path_to_terminal = r'C:\Program Files\MetaTrader 5\terminal64.exe'

# Инициализация MetaTrader 5
if not mt5.initialize(path_to_terminal):
    print("Не удалось инициализировать MetaTrader 5:", mt5.last_error())
    exit()

# Указываем символ и временной диапазон
symbol = "USDSGD"
timeframe = mt5.TIMEFRAME_H1
from_date = datetime(2024, 1, 1)
to_date = datetime(2024, 2, 1)

# Проверка доступности символа
if not mt5.symbol_select(symbol, True):
    print(f"Не удалось выбрать символ {symbol}: {mt5.last_error()}")
    mt5.shutdown()
    exit()

# Получение исторических данных
rates = mt5.copy_rates_range(symbol, timeframe, from_date, to_date)

# Проверка на наличие данных
if rates is None:
    print("Не удалось получить данные:", mt5.last_error())
else:
    rates_df = pd.DataFrame(rates)
    rates_df['time'] = pd.to_datetime(rates_df['time'], unit='s')

    print(rates_df)

    min_value = rates_df['low'].min()
    max_value = rates_df['high'].max()
    # rates_df = pd.read_excel('./history.xlsx')
    plt.figure(figsize=(12, 6))
    plt.plot(rates_df['time'], rates_df['open'], marker='o', label='Open Price', color='blue')
    # plt.plot(rates_df['time'], rates_df['high'], marker='^', label='High Price', color='green')
    # plt.plot(rates_df['time'], rates_df['low'], marker='v', label='Low Price', color='red')
    plt.title(f'Price level {symbol} from {from_date.date()} to {to_date.date()}')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.ylim(min_value, max_value)
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

    # rates_df.to_excel('./history.xlsx')

# Завершение работы с MetaTrader 5
mt5.shutdown()
