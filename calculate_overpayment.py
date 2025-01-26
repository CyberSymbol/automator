import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
import math

# Параметры для автоматического тестирования
budget_rub = 100000
usd_to_rub = 97.8139
crypto_price_usd = 3338
offered_price_rub = 347462

# Функция для очеловечивания чисел
def human_readable_round(number):
    """
    Округляет число в "человеческом" формате, чтобы оно было легко читаемо.
    Например: 346531 -> 346000, 12345 -> 12000.
    """
    num_digits = len(str(int(number)))
    if num_digits % 2 == 0:
        round_to = 10 ** (num_digits // 2)
    else:
        round_to = 10 ** (num_digits // 2 + 1)
    return math.floor(number / round_to) * round_to

# Генерация списка цен
offered_prices = [
    human_readable_round(offered_price_rub * (1 + i / 200)) if i != 0 else offered_price_rub
    for i in range(-20, 21)
]

# Создание таблицы переплат
def calculate_crypto_overpayment(budget_rub, usd_to_rub, crypto_price_usd, offered_price_rub):
    current_price_rub = crypto_price_usd * usd_to_rub
    crypto_at_offered_price = budget_rub / offered_price_rub
    crypto_at_current_price = budget_rub / current_price_rub
    missed_crypto = crypto_at_current_price - crypto_at_offered_price
    cost_at_current_price = crypto_at_offered_price * current_price_rub
    overpayment_rub = budget_rub - cost_at_current_price
    overpayment_usd = overpayment_rub / usd_to_rub

    return {
        "overpayment_rub": overpayment_rub,
        "overpayment_usd": overpayment_usd,
        "missed_crypto": missed_crypto
    }

table_data = []
for price in offered_prices:
    result = calculate_crypto_overpayment(budget_rub, usd_to_rub, crypto_price_usd, price)
    table_data.append({
        "Цена крипты, rub": int(price),
        "Переплата, rub": int(result['overpayment_rub']),
        "Переплата, usd": int(result['overpayment_usd']),
        "Недостача крипты": round(result['missed_crypto'], 3)
    })

# Создание DataFrame
table = pd.DataFrame(table_data)

# Настройка отображения таблицы
fig, ax = plt.subplots(figsize=(10, len(table) * 0.5))
ax.axis('tight')
ax.axis('off')

# Преобразование данных таблицы
formatted_data = table.copy()
formatted_data["Цена крипты, rub"] = formatted_data["Цена крипты, rub"].apply(lambda x: f"{int(x)}")
formatted_data["Переплата, rub"] = formatted_data["Переплата, rub"].apply(lambda x: f"{int(x)}")
formatted_data["Переплата, usd"] = formatted_data["Переплата, usd"].apply(lambda x: f"{int(x)}")

table_plot = ax.table(
    cellText=formatted_data.values,
    colLabels=formatted_data.columns,
    cellLoc='center',
    loc='center'
)

# Выделение строк
nearest_zero_row_idx = (table["Недостача крипты"].abs()).idxmin()
user_price_row_idx = table[table["Цена крипты, rub"] == offered_price_rub].index

for (row, col), cell in table_plot.get_celld().items():
    if row == 0:
        continue
    if row - 1 == nearest_zero_row_idx:
        cell.set_facecolor("lightgreen")
    if row - 1 in user_price_row_idx:
        cell.set_facecolor("lightcoral")

# Генерация имени файла
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_path = f"/home/vladimir/Документы/Crypto/таблицы рублёвых переплат/overpayment_{current_time}.pdf"

# Сохранение таблицы
with PdfPages(output_path) as pdf:
    pdf.savefig(fig, bbox_inches='tight')

plt.close()
