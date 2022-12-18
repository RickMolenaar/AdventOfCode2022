from more_itertools import distinct_permutations

class Rock:
    def __init__(self, shape: list[tuple[int, int]], y: int, initial_movements: dict[str, int] = None, initial_command: str = None):
        if initial_command is not None:
            dx = initial_movements[initial_command]
            dy = -len(initial_command) + 1
        else:
            dx = 0
            dy = 0
        self.y = y + dy
        self.points = [(3 + sx + dx, self.y + sy) for (sx, sy) in shape]

    def move(self, command, rocks, max_y):
        if command == '<':
            to_check = [(x - 1, y) for (x, y) in self.points if (x - 1, y) not in self.points]
        elif command == '>':
            to_check = [(x + 1, y) for (x, y) in self.points if (x + 1, y) not in self.points]
        elif command == 'v':
            to_check = [(x, y - 1) for (x, y) in self.points if (x, y - 1) not in self.points]
        if any(x == 0 or x == 8 for (x, _) in to_check):
            return True
        if any(y == 0 for (_, y) in to_check):
            return False
        if self.y <= max_y + 1:
            for rock in rocks:
                if rock.y + 4 < self.y:
                    continue
                for p in rock.points:
                    if p in to_check:
                        return command != 'v'
        if command == '<':
            self.points = [(x - 1, y) for (x, y) in self.points]
        elif command == '>':
            self.points = [(x + 1, y) for (x, y) in self.points]
        elif command == 'v':
            self.points = [(x, y - 1) for (x, y) in self.points]
            self.y -= 1
        if self.y < 0:
            raise ValueError
        return True

shapes = [
    ['horizontal', ((0, 0), (1, 0), (2, 0), (3, 0))],
    ['cross', ((0, 1), (1, 0), (1, 1), (1, 2), (2, 1))],
    ['inverse_l', ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2))],
    ['vertical', ((0, 0), (0, 1), (0, 2), (0, 3))],
    ['block', ((0, 0), (1, 0), (0, 1), (1, 1))],
]

command_sets = []
for lefts in range(5):
    commands = '<' * lefts + '>' * (4 - lefts)
    for p in distinct_permutations(commands):
        command_sets.append(''.join(p))

for item in shapes:
    name, shape = item
    movements = {}
    for commands in command_sets:
        rock = Rock(shape, 4)
        for c in commands:
            rock.move(c, [], 0)
        dx = rock.points[0][0]
        movements[commands] = dx - 3
    item.append(movements)

def parse_input(file = 'day17.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day17example.txt')

def format_input(inp):
    return inp[0]

def print_rocks(rocks, max_y, falling_rock = None, min_y = 0):
    print()
    grid = [[0] * 7 for _ in range(max_y + 6)]
    if falling_rock is not None:
        for x, y in falling_rock.points:
            grid[y - 1][x - 1] = 2
    for rock in rocks:
        for x, y in rock.points:
            grid[y - 1][x - 1] = 1
    for y in range(max_y + 5, min_y - 1, -1):
        print('|' + ''.join('.#@'[grid[y][x]] for x in range(7)) + '|')
    print('+' + '-' * 7 + '+')

def solve(inp, debug=False):
    inp = format_input(inp)
    # print(inp)
    step = -1
    rock = None
    rock_factories = []
    for name, shape, movements in shapes:
        # print(name, shape)
        rock_factories.append(lambda y, initial_command, shape=shape, movements=movements: Rock(shape, y, movements, initial_command))
    # print(rock_factories)
    max_y = 0
    delta_max_y = None
    stable_delta = None
    last_max_y = 0
    last_blocks = 0
    delta_blocks = None
    rocks = []
    MAX_ROCKS = 1_000_000_000_000

    FANCY = True
    required = MAX_ROCKS
    while len(rocks) < required:
        step += 1
        step %= len(inp)
        if step == 0:
            if stable_delta is None:
                if max_y - last_max_y == delta_max_y:
                    stable_delta = delta_max_y
                    delta_blocks = len(rocks) - last_blocks
                    calculated_steps = (MAX_ROCKS - len(rocks)) // delta_blocks
                    required -= calculated_steps * delta_blocks
                    calculated_max_y = calculated_steps * stable_delta
                    # print(calculated_steps, required, delta_blocks)
            else:
                assert max_y - last_max_y == stable_delta
                assert len(rocks) - last_blocks == delta_blocks
            last_blocks = len(rocks)
            delta_max_y = max_y - last_max_y
            last_max_y = max_y

        if rock is None:
            if FANCY:
                # if debug and len(rocks) < 5:
                #     print(f"Using {inp[step:step + 4]} (step: {step})")
                commands = inp[step:step + 4]
                if len(commands) < 4:
                    commands += inp[:4 - len(commands)]
                rock = rock_factories[len(rocks) % 5](max_y + 4, commands)
                step += 4
                result = rock.move('v', rocks[-30:], max_y)
                if not result:
                    max_y = max(max_y, max(y for (_, y) in rock.points))
                    rocks.append(rock)
                    rock = None
                    step -= 1
                    continue
            else:
                rock = rock_factories[len(rocks) % 5](max_y + 4, None)
        command = inp[step % len(inp)]
        rock.move(command, rocks, max_y)
        result = rock.move('v', rocks[-30:], max_y)
        if not result:
            max_y = max(max_y, max(y for (_, y) in rock.points))
            rocks.append(rock)
            rock = None
        if step > 1000000:
            raise ValueError(len(rocks), max_y)
    return max_y + calculated_max_y

def main(debug = False):
    return str(solve(parse_example(), True)) + '\n' + str(solve(parse_input(), debug))
