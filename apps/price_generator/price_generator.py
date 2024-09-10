from apps.price_generator.commissions import commission_marketplace

def price_generator(cost_price:float, multiplier:float, profit_margin:float, discount:float = 23.5, tax:float = 5, rule_comission:callable= commission_marketplace) -> float:
    
    cost_commission = rule_comission()
    
    cost = (cost_price - (cost_price * (discount/100))) * multiplier
    
    cost += cost_commission['fixed_cost']
    
    divisor_number = (100 - profit_margin - tax - cost_commission['variable_cost']) / 100
    
    price = cost / divisor_number
    
    return rounded_number(price)

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
    
