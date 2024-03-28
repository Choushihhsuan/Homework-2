liquidity = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25),
}

import random

liquidity_copy = liquidity.copy()
tokens = ['tokenA', 'tokenB', 'tokenC', 'tokenD', 'tokenE']

def arbitrage(t_in_index, t_out_index, amount_in):
    if t_in_index == t_out_index:
        return amount_in
    
    t_in, t_out = tokens[t_in_index], tokens[t_out_index]
    if t_in_index < t_out_index:
        reserve0, reserve1 = liquidity[(t_in, t_out)][0] * 1E18, liquidity[(t_in, t_out)][1] * 1E18
    else:
        reserve1, reserve0 = liquidity[(t_out, t_in)][0] * 1E18, liquidity[(t_out, t_in)][1] * 1E18
    amount_0 = amount_in * 1E18 * 0.997 + reserve0
    amount_1 = reserve0 * reserve1 / amount_0
    amount_out = reserve1 - amount_1

    if t_in_index < t_out_index:
        liquidity[(t_in, t_out)] = (amount_0 * 1E-18, amount_1 * 1E-18)
    else:
        liquidity[(t_out, t_in)] = (amount_1 * 1E-18, amount_0 * 1E-18)

    return amount_out * 1E-18

def generate_path(length):
    if length < 3:
        print('Path length must be at least 3!')
        exit
    
    path = [1]
    path.extend([random.choice([tokens.index(token) for token in tokens if token != 'tokenB']) for _ in range(length - 2)])
    path.append(1)

    return path

b_init = 5
b_final_expected = 20

for d in range(5, 6):
    while True:
        liquidity = liquidity_copy.copy()
        path = generate_path(d)
        amount = b_init

        for step in range(d - 1):
            amount = arbitrage(path[step], path[step + 1], amount)
        
        if amount > b_final_expected:
            path_str = '->'.join([tokens[i] for i in path])
            print(f'Path: {path_str}, tokenB balance = {amount}')
            break
