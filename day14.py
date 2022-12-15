def parse_input(file = 'day14.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day14example.txt')

def format_input(inp):
    rocks = []
    min_x = 500
    max_x = 500
    max_y = 0
    for line in inp:
        structure = []
        coords = line.split('->')
        for coord in coords:
            x, y = list(map(int, coord.split(',')))
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
            structure.append((x, y))
        rocks.append(structure)
    min_x = min(min_x, 500 - (max_y + 1))
    max_x = max(max_x, 500 + max_y + 1)
    max_y = max_y + 2
    rocks.append([(min_x - 2, max_y), (max_x + 2, max_y)])
    grid = {x: [False] * (max_y + 1) for x in range(min_x - 2, max_x + 3)}
    for structure in rocks:
        for i, start in enumerate(structure[:-1]):
            end = structure[i+1]
            for x in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
                for y in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                    grid[x][y] = 1
    return grid, min_x, max_x, max_y

def print_grid(grid, min_x, max_x, max_y):
    for y in range(0, max_y + 1):
        print(''.join('.#0'[grid[x][y]] for x in range(min_x, max_x + 1)))
    print()

def solve(inp, debug=False):
    grid, min_x, max_x, max_y = format_input(inp)
    if debug:
        print_grid(grid, min_x, max_x, max_y)
    amount = 0
    part1done = False
    MAX_ITERS = max_y**2        # Area of filled triangle
    while True:
        if amount > MAX_ITERS:
            raise ValueError
        sx, sy = 500, 0
        possible_moves = [(sx + dx, sy + 1) for dx in (0, -1, 1) if not grid[sx+dx][sy+1]]
        if not possible_moves:
            print_grid(grid, min_x, max_x, max_y)
            return amount + 1
        while possible_moves:
            sx, sy = possible_moves[0]
            if sy == max_y - 2 and not part1done:
                print(f"Part 1: {amount}")
                print_grid(grid, min_x, max_x, max_y)
                part1done = True
            possible_moves = [(sx + dx, sy + 1) for dx in (0, -1, 1) if not grid[sx+dx][sy+1]]
        grid[sx][sy] = 2
        amount += 1
        # if debug:
        #     print_grid(grid, min_x, max_x, max_y)

def main(debug = False):
    return str(solve(parse_example(), True)) + '\n' + str(solve(parse_input(), debug))
