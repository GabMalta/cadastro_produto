def commission_marketplace(fixed_cost:list = [4], variable_cost:list = [20]) -> dict:
    cost_f = 0
    cost_v = 0
    
    for x in fixed_cost:
        cost_f += x
        
    for x in variable_cost:
        cost_v += x
        
        
    return {'fixed_cost': cost_f, 'variable_cost': cost_v}