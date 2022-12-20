def parse_input(file = 'day20.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day20example.txt')

def format_input(inp):
    values = [(int(val) * 811589153, i) for i, val in enumerate(inp)]
    zero_index = None
    for val, id in values:
        if val == 0:
            zero_index = id
    return values, zero_index

def solve(inp, debug=False):
    inp, zero_index = format_input(inp)
    decrypted = inp.copy()
    # if debug:
    #     print([val for val, id in inp])
    for i in range(10):
        for val, id in inp:
            index = decrypted.index((val, id))
            new_index = index + val
            if new_index < 0 or new_index > len(inp):
                new_index %= len(inp) - 1
            # if debug:
            #     print(f'Moving {val} from {index} to {new_index}')
            decrypted.pop(index)
            decrypted.insert(new_index, (val, id))
            # if debug:
            #     print([val for val, id in decrypted])
    coords = [decrypted[(decrypted.index((0, zero_index)) + 1000 * i) % len(inp)][0] for i in range(1, 4)]
    # if debug:
    #     print([val for val, id in decrypted])
    print(coords)
    return sum(coords)

def main(debug = False):
    return str(solve(parse_example(), True)) + '\n' + str(solve(parse_input(), debug))
