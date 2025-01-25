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

    # Получение входных данных
    budget_rub = float(input("Введите сумму в рублях для покупки: "))
    usd_to_rub = float(input("Введите курс рубля к доллару: "))
    crypto_price_usd = float(input("Введите текущую цену криптовалюты в долларах: "))
    offered_price_rub = float(input("Введите предложенную цену криптовалюты в рублях: "))

    # Генерация списка цен с шагом 1% (10 значений)
    offered_prices = [offered_price_rub * (1 + i / 100) for i in range(11)]

    # Создание таблицы переплат
    table_data = []
    for price in offered_prices:
        result = calculate_crypto_overpayment(budget_rub, usd_to_rub, crypto_price_usd, price)
        table_data.append({
            "Price": round(price),
            "-RUB": round(result['overpayment_rub']),
            "-USD": round(result['overpayment_usd']),
            "-Crypto": round(result['missed_crypto'], 3)
        })

    # Вывод таблицы
    table = pd.DataFrame(table_data)
    print(table.to_string(index=False))
