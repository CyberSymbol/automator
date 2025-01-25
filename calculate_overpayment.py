def calculate_crypto_overpayment(budget_rub, usd_to_rub, crypto_price_usd, offered_price_rub):
    """
    Рассчитывает переплату и недополученную криптовалюту при покупке по предложенной цене.

    Аргументы:
        budget_rub (float): Сумма в рублях, доступная для покупки.
        usd_to_rub (float): Курс рубля к доллару.
        crypto_price_usd (float): Текущая цена криптовалюты в долларах.
        offered_price_rub (float): Предложенная цена криптовалюты в рублях.

    Возвращает:
        dict: Содержит переплату в рублях, переплату в долларах и недополученную криптовалюту.
    """
    # Переводим цену криптовалюты из долларов в рубли
    current_price_rub = crypto_price_usd * usd_to_rub

    # Вычисляем количество криптовалюты, которое можно купить по предложенной цене
    crypto_at_offered_price = budget_rub / offered_price_rub

    # Вычисляем количество криптовалюты, которое можно купить по текущей цене
    crypto_at_current_price = budget_rub / current_price_rub

    # Рассчитываем недополученное количество криптовалюты
    missed_crypto = crypto_at_current_price - crypto_at_offered_price

    # Рассчитываем переплату в рублях
    cost_at_current_price = crypto_at_offered_price * current_price_rub
    overpayment_rub = budget_rub - cost_at_current_price

    # Конвертируем переплату в доллары
    overpayment_usd = overpayment_rub / usd_to_rub

    return {
        "overpayment_rub": round(overpayment_rub, 2),
        "overpayment_usd": round(overpayment_usd, 2),
        "missed_crypto": round(missed_crypto, 6),
    }

if __name__ == "__main__":
    import pandas as pd  # Импорт библиотеки для работы с таблицами
    import matplotlib.pyplot as plt # Импорт модуля для работы с PDF
    from matplotlib.backends.backend_pdf import PdfPages
    from datetime import datetime

    # Получение входных данных
    budget_rub = float(input("Введите сумму в рублях для покупки: ").replace(',', '.'))
    usd_to_rub = float(input("Введите курс рубля к доллару: ").replace(',', '.'))
    crypto_price_usd = float(input("Введите текущую цену криптовалюты в долларах: ").replace(',', '.'))
    offered_price_rub = float(input("Введите предложенную цену криптовалюты в рублях: ").replace(',', '.'))

    # Генерация списка цен с шагом 1% (10 значений)
    def human_readable_round(number):
        """
        Округляет число в "человеческом" формате, чтобы оно было легко читаемо.
        Например: 346531 -> 346000, 12345 -> 12000.

        Args:
            number (float): Число для округления.

        Returns:
            float: Округленное число.
        """
        import math
        num_digits = len(str(int(number)))  # Количество цифр в числе
        if num_digits % 2 == 0:
            round_to = 10 ** (num_digits // 2)  # Округляем до половины цифр
        else:
            round_to = 10 ** (num_digits // 2 + 1)  # Ещё одна значимая цифра
        return math.floor(number / round_to) * round_to

    offered_prices = [
        human_readable_round(offered_price_rub * (1 - i / 200)) for i in range(20, 0, -1)
    ] + [
        offered_price_rub
    ] + [
        human_readable_round(offered_price_rub * (1 + i / 200)) for i in range(1, 21)
    ]

# Создание таблицы переплат
table_data = []
for price in offered_prices:
    result = calculate_crypto_overpayment(budget_rub, usd_to_rub, crypto_price_usd, price)
    table_data.append({
        "Цена крипты, rub": round(price),
        "Переплата, rub": round(result['overpayment_rub']),
        "Переплата, usd": round(result['overpayment_usd']),
        "Недостача крипты": round(result['missed_crypto'], 3)
    })

# Создание DataFrame
table = pd.DataFrame(table_data)

# Настройка отображения таблицы
fig, ax = plt.subplots(figsize=(10, len(table) * 0.5))  # Размер фигуры зависит от количества строк
ax.axis('tight')
ax.axis('off')
table_plot = ax.table(cellText=table.values, colLabels=table.columns, cellLoc='center', loc='center')

# Генерация имени файла с датой и временем
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_path = f"/home/vladimir/Документы/Crypto/таблицы рублёвых переплат/overpayment_{current_time}.pdf"

# Сохранение таблицы в PDF
with PdfPages(output_path) as pdf:
    pdf.savefig(fig, bbox_inches='tight')

plt.close()
