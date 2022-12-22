import re

def parse_input(file = 'day22.txt') -> list[str]:
    with open(file) as f:
        s = map(lambda l: l.rstrip('\n'), f.readlines())
    return list(s)

def parse_example() -> list[str]:
    return parse_input('day22example.txt')

def format_input(inp: list[str]) -> tuple[list[list[int]], str]:
    jungle_map = []
    values_per_side = 0
    for line_number, line in enumerate(inp):
        if '.' not in line and '#' not in line:
            break
        start_index = min(line.index(c) for c in '.#' if c in line)
        end_index = len(line) - 1
        row = []
        for i, c in enumerate(line):
            if c == '.':
                row.append(1)
            elif c == '#':
                row.append(2)
            elif i < start_index:
                row.append(-1)
            else:
                raise ValueError(i, c, line)
        jungle_map.append(row)
        values_per_side += len([v for v in row if v > 0])
    path = re.findall('\d+[LR]?', inp[line_number + 1])
    cube_size = int((values_per_side // 6) ** 0.5)
    mapping = {}
    for line in inp[line_number + 2:]:
        # print(line)
        p1, p2 = line.split(':')
        gr1, gc1, gr2, gc2 = map(int, re.findall('-?\d+', p1))
        ghost1 = (gr1, gc1)
        ghost2 = (gr2, gc2)
        
        r1, c1, dir1, r2, c2, dir2 = map(int, re.findall('\d+', p2))
        cube1 = (r1, c1)
        cube2 = (r2, c2)
        def check(ghost, cube, direction):
            if direction == 0:
                assert cube == (ghost[0], ghost[1] + 1)
            elif direction == 1:
                assert cube == (ghost[0] + 1, ghost[1])
            elif direction == 2:
                assert cube == (ghost[0], ghost[1] - 1)
            else:
                assert cube == (ghost[0] - 1, ghost[1])
        check(ghost1, cube1, dir1)
        check(ghost2, cube2, dir2)
        mapping[ghost1] = (cube1, dir1, cube2, dir2)
        mapping[ghost2] = (cube1, dir1, cube2, dir2)
    assert cube_size**2 * 6 == values_per_side
    return jungle_map, path, cube_size, mapping

def print_map(map, walked):
    for r, row in enumerate(map):
        for col, v in enumerate(row):
            if (r, col) in walked:
                char = '>V<^'[walked[(r, col)]]
            else:
                if v <= 0:
                    v = 0
                char = ' .#'[v]
            print(char, end='')
        print()

def transform(row, col, direction, cube_size, mappings):
    ghost_face = (row // cube_size, col // cube_size)
    if direction == 0:
        origin = (ghost_face[0], ghost_face[1] - 1)
    elif direction == 1:
        origin = (ghost_face[0] - 1, ghost_face[1])
    elif direction == 2:
        origin = (ghost_face[0], ghost_face[1] + 1)
    elif direction == 3:
        origin = (ghost_face[0] + 1, ghost_face[1])
    if ghost_face == (3, -2):
        print(row, col)
    data = mappings[ghost_face]
    if origin == data[0]:
        assert (direction + 2) % 4 == data[1]
        new_cube = data[2]
        new_direction = data[3]
    else:
        new_cube = data[0]
        new_direction = data[1]
        assert origin == data[2]
        assert (direction + 2) % 4 == data[3]
    d_row = row - origin[0] * cube_size
    d_col = col - origin[1] * cube_size
    dir_diff = (direction - new_direction) % 4
    if dir_diff == 0:
        pass
    elif dir_diff == 1:
        d_row, d_col = -d_col - 1, d_row
    elif dir_diff == 2:
        d_row, d_col = -d_row - 1, -d_col - 1
    else:
        d_row, d_col = d_col, -d_row - 1
    d_row %= cube_size
    d_col %= cube_size
    return new_cube[0] * cube_size + d_row, new_cube[1] * cube_size + d_col, new_direction

def transform_part1(row, col, direction, jungle_map):
    if direction == 0:
        col = 0
        while jungle_map[row][col] < 0:
            col += 1
    elif direction == 1:
        row = 0
        while len(jungle_map[row]) - 1 < col or jungle_map[row][col] < 0:
            row += 1
    elif direction == 2:
        col = len(jungle_map[row]) - 1
    else:
        assert direction == 3
        row = len(jungle_map) - 1
        while len(jungle_map[row]) - 1 < col or jungle_map[row][col] < 0:
            row -= 1
    return row, col

def solve(inp, part, debug=False):
    jungle_map, path, cube_size, mapping = format_input(inp)
    row, col = 0, 0
    direction = 0
    while jungle_map[row][col] < 0:
        col += 1
    walked = {(row, col): direction}
    for i, command in enumerate(path):
        if 'L' in command or 'R' in command:
            amount = int(command[:-1])
        else:
            amount = int(command)
        for _ in range(amount):
            new_r, new_c = row, col
            new_direction = direction
            if direction == 0:
                new_c += 1
            elif direction == 1:
                new_r += 1
            elif direction == 2:
                new_c -= 1
            else:
                new_r -= 1
            in_range = False
            try:
                in_range = new_c >= 0 and jungle_map[new_r][new_c] > 0
            except IndexError:
                pass
            # print(f"Checking {new_r, new_c}")
            if not in_range:
                if part == 1:
                    new_r, new_c = transform_part1(new_r, new_c, direction, jungle_map)
                else:
                    new_r, new_c, new_direction = transform(new_r, new_c, direction, cube_size, mapping)
            if jungle_map[new_r][new_c] == 1:
                row, col, direction = new_r, new_c, new_direction
                walked[(row, col)] = direction
            elif jungle_map[new_r][new_c] == 2:
                # if debug:
                #     print(f"{new_r + 1, new_c + 1} is a wall")
                break
            else:
                print(new_r, new_c)
                raise ValueError(jungle_map[new_r][new_c], jungle_map[new_r])
        # if debug:
        #     print(row + 1, col + 1)
        turn  = command[-1]
        if turn == 'L':
            direction -= 1
        elif turn == 'R':
            direction += 1
        direction %= 4
        walked[(row, col)] = direction
    row += 1
    col += 1
    # print(row, col, direction)
    return 1000 * row + 4 * col + direction

def main(debug = False):
    print("Part 1 (example):", solve(parse_example(), 1))
    print("Part 1 (actual):", solve(parse_input(), 1))
    return str(solve(parse_example(), 2, True)) + '\n' + str(solve(parse_input(), 2, debug))
