import functools

def parse_input(file = 'day13.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day13example.txt')

def format_input(inp):
    packets = []
    for i in range(0, len(inp), 3):
        packets.extend((eval(inp[i]), eval(inp[i+1])))
    return packets

def compare(left, right, debug, level = 0):
    if debug:
        print('\t' * level, f'Comparing {left} vs {right}')
    if type(left) == int and type(right) == int:
        return -1 if left == right else left < right
    if type(left) == int:
        left = [left]
    if type(right) == int:
        right = [right]
    if len(left) == 0 and len(right) == 0:
        return -1
    try:
        l0 = left[0]
    except IndexError:
        return True
    try:
        r0 = right[0]
    except IndexError:
        return False
    c0 = compare(l0, r0, debug, level + 1)
    if c0 == -1:
        return compare(left[1:], right[1:], debug, level)
    else:
        return c0

def key_compare(packet1, packet2):
    return -1 if compare(packet1, packet2, False) else 1

def solve(inp, debug=False):
    # pairs = format_input(inp)
    # ordered_pairs = [i+1 for i, pair in enumerate(pairs) if compare(pair[0], pair[1], False) is True]
    # if debug:
    #     print(ordered_pairs)
    # return sum(ordered_pairs)
    packets = format_input(inp)
    packets.append([[2]])
    packets.append([[6]])
    packets = sorted(packets, key=functools.cmp_to_key(key_compare))
    if debug:
        for p in packets:
            print(p)
    return (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)

def main(debug = False):
    return str(solve(parse_example(), True)) + '\n' + str(solve(parse_input(), debug))
