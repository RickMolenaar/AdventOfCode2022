from collections import defaultdict

def parse_input(file = 'day23.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day23example.txt')

def format_input(inp):
    elves = set()
    for row, value in enumerate(inp):
        for col, c in enumerate(value):
            if c == '#':
                elves.add((row, col))
    return elves

def print_elves(elves):
    min_row = min(elf[0] for elf in elves)
    max_row = max(elf[0] for elf in elves)
    min_col = min(elf[1] for elf in elves)
    max_col = max(elf[1] for elf in elves)
    for row in range(min_row, max_row + 1):
        for col in range(min_col, max_col + 1):
            print('#' if (row, col) in elves else '.', end='')
        print()
    print()

def solve(inp, debug=False):
    elves = format_input(inp)
    looks = [((-1, -1), (-1, 0), (-1, 1)), ((1, -1), (1, 0), (1, 1)), ((-1, -1), (0, -1), (1, -1)), ((-1, 1), (0, 1), (1, 1))]
    if debug:
        print_elves(elves)
    for round in range(1000):
        moves = []
        claimed_positions = defaultdict(int)
        for elf in sorted(elves):
            needs_move = False
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    if (elf[0] + dx, elf[1] + dy) in elves:
                        needs_move = True
                        break
                if needs_move:
                    break
            if not needs_move:
                continue
            for look in looks:
                for (lr, lc) in look:
                    if (elf[0] + lr, elf[1] + lc) in elves:
                        break
                else:
                    target = (elf[0] + look[1][0], elf[1] + look[1][1])
                    moves.append((elf, target))
                    claimed_positions[target] += 1
                    break
        if not moves:
            return round + 1
        for elf, target in moves:
            if claimed_positions[target] == 1:
                assert target not in elves
                elves.remove(elf)
                elves.add(target)
        looks.append(looks.pop(0))
        if debug:
            print_elves(elves)
    min_row = min(elf[0] for elf in elves)
    max_row = max(elf[0] for elf in elves)
    min_col = min(elf[1] for elf in elves)
    max_col = max(elf[1] for elf in elves)
    print(min_row, max_row, min_col, max_col)
    return (max_row - min_row + 1) * (max_col - min_col + 1) - len(elves)

def main(debug = False):
    return str(solve(parse_example(), True)) + '\n' + str(solve(parse_input(), debug))
