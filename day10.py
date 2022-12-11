def parse_input(file = 'day10.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return s

def parse_example():
    return parse_input('day10example.txt')

def format_input(inp):
    return inp

def generate_screen(screen):
    screen_str = ''
    for i, c in enumerate(screen):
        screen_str += '#' if c else '.'
        if i % 40 == 39:
            screen_str += '\n'
    return screen_str

def display_screen(screen):
    rows = [screen[x:x+41] for x in range(0, 201, 40)]
    screen_str = ''
    for row in rows:
        for c in row:
            print('#' if c else '.', end='')
        print()
    print()

def solve(inp, debug=False):
    inp = format_input(inp)
    current_command = None
    tot = 0
    cycle = 0
    X = 1
    screen = [0] * 240
    while cycle < 240:
        if X-1 <= cycle % 40 <= X+1:
            screen[cycle] = 1
        cycle += 1
        if cycle < 20 and debug:
            display_screen(screen)
        # if cycle % 40 == 20:
        #     # if debug:
        #     #     print(cycle, X)
        #     tot += cycle * X
        if current_command is not None:
            command, value = current_command
            current_command = None
            X += int(value)
            continue
        command = next(inp)
        if command != 'noop':
            current_command = command.split()
    return generate_screen(screen)

def main(debug = False):
    return str(solve(parse_example(), True)) + '\n' + str(solve(parse_input(), debug))
