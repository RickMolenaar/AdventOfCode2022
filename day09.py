def parse_input(file = 'day09.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day09example.txt')

def format_input(inp):
    return inp

def move_tail(tail, head):
    if abs(tail[0] - head[0]) <= 1 and abs(tail[1] - head[1]) <= 1:
        return tail
    new_tail = list(tail)
    if tail[0] != head[0]:
        new_tail[0] -= (tail[0] - head[0]) / abs(tail[0] - head[0])
    if tail[1] != head[1]:
        new_tail[1] -= (tail[1] - head[1]) / abs(tail[1] - head[1])
    return tuple(new_tail)

def solve(inp, debug=False):
    inp = format_input(inp)
    tail = head = (0, 0)
    visited = {tail}
    for command in inp:
        direction, amount = command.split()
        if direction == 'R':
            to_add = (1, 0)
        elif direction == 'L':
            to_add = (-1, 0)
        elif direction == 'U':
            to_add = (0, 1)
        elif direction == 'D':
            to_add = (0, -1)
        else:
            raise ValueError(f'Couldn\'t read {direction}')
        for i in range(int(amount)):
            head = (head[0] + to_add[0], head[1] + to_add[1])
            tail = move_tail(tail, head)
            visited.add(tail)
        # if debug:
        #     print(head, tail)
    return len(visited)

def main(debug = False):
    return str(solve(parse_example(), True)) + '\n' + str(solve(parse_input(), debug))
