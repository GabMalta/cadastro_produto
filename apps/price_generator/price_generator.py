def commission_marketplace(fixed_cost: list = [4], variable_cost: list = [20]) -> dict:
    cost_f = 0
    cost_v = 0

    for x in fixed_cost:
        cost_f += x

    for x in variable_cost:
        cost_v += x

    return {"fixed_cost": cost_f, "variable_cost": cost_v}


def price_generator(
    cost_price: float,
    multiplier: float,
    profit_margin: float,
    discount: float = 23.5,
    tax: float = 5,
    rule_comission: callable = commission_marketplace,
) -> float:

    cost_commission = rule_comission()

    cost = (cost_price - (cost_price * (discount / 100))) * multiplier

    cost_total = cost + cost_commission["fixed_cost"]

    divisor_number = (100 - profit_margin - tax - cost_commission["variable_cost"]) / 100

    price = cost_total / divisor_number

    return rounded_number(price), rounded_number(cost)


def rounded_number(value) -> float:
    # Separar a parte inteira e a parte decimal
    integer_part = int(value)
    decimal_part = value % 1

    # Encontrar a primeira casa decimal
    first_decimal = int(decimal_part * 10) / 10

    # Ajustar o valor com base na parte decimal
    if decimal_part < first_decimal + 0.05:
        return integer_part + first_decimal - 0.01
    else:
        return integer_part + first_decimal + 0.09
