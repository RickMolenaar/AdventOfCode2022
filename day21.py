import re
def parse_input(file = 'day21.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day21example.txt')

def format_input(inp):
    evaluated = {}
    actions = {}
    for line in inp:
        monkey, action = line.split(':')
        try:
            number = int(action)
            evaluated[monkey] = number
        except ValueError:
            required = re.findall('[a-z]{4}', action)
            operator = re.findall('[+*/-]', action)[0]
            actions[monkey] = (operator, required)
    return evaluated, actions

def get_value(monkey, evaluated, actions):
    try:
        return evaluated[monkey]
    except KeyError:
        evaluated = evaluated.copy()
        try:
            operator, required = actions[monkey]
            v1, v2 = [get_value(m, evaluated, actions) for m in required]
            if v1 is None or v2 is None:
                return None
            evaluated[monkey] = eval(str(v1) + operator + str(v2))
            return evaluated[monkey]
        except KeyError:
            assert monkey == 'humn'
            return None

def find_number(evaluated, actions):
    g1, g2 = 1, 2
    MAX_ITERS = 1000
    for iter in range(MAX_ITERS):
        print(f'Trying {g1}, {g2}')
        evaluated['humn'] = g1
        r1 = get_value('root', evaluated.copy(), actions)
        if r1 == 0:
            return g1
        evaluated['humn'] = g2
        r2 = get_value('root', evaluated.copy(), actions)
        if r2 == 0:
            return g2
        if r1 * r2 < 0:
            diff = abs(r2 - r1)
            progress = abs(r1) / diff
            new_guess = g1 + int(progress * (r2 - r1))
            if new_guess == g1:
                new_guess += 1
            evaluated['humn'] = new_guess
            new_result = get_value('root', evaluated.copy(), actions)
            if r1 * new_result < 0:
                g1, g2 = g1, new_guess
            else:
                g1, g2 = new_guess, g2
        else:
            diff = r1 - r2
            expected = int(g1 + int((r1 / diff) * (g2 - g1)))
            if expected >= g2:
                expected = max(expected, g2 + 1)
                g1, g2 = g2, expected
            else:
                assert expected < g1
                expected = min(expected, g1 - 1)
                g1, g2 = expected, g1
    raise ValueError(f'Could not find an answer in {MAX_ITERS} iterations')

def solve(inp, debug=False):
    evaluated, actions = format_input(inp)
    print('Part 1:', get_value('root', evaluated, actions))

    actions['root'] = ('-', actions['root'][1])
    return find_number(evaluated, actions)

def main(debug = False):
    return str(solve(parse_example(), True)) + '\n' + str(solve(parse_input(), debug))
