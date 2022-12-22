import doctest
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
        # row.append(-start_index)
        jungle_map.append(row)
        values_per_side += len([v for v in row if v > 0])
    path = re.findall('\d+[LR]?', inp[line_number + 1])
    cube_size = int((values_per_side // 6) ** 0.5)
    for line in inp[line_number + 2:]:
        p1, p2 = line.split(':')
        gr1, gc1, gr2, gc2
    assert cube_size**2 * 6 == values_per_side
    return jungle_map, path, cube_size

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

# def find_cube_mapping(jungle_map, cube_size):
#     face_locations = []
#     for y in range(6):
#         if y * cube_size > len(jungle_map):
#             break
#         for x in range(6):
#             try:
#                 v = jungle_map[y * cube_size][x * cube_size]
#                 if v > 0:
#                     face_locations.append((x, y))
#             except IndexError:
#                 break
#     assert len(face_locations) == 6
#     mapping = {}
#     return face_locations

def transform(row, col, direction, cube_size, mappings):
    """
    >>> transform(2, 7, 2, 4)
    (4, 6, 1)
    >>> transform(3, 12, 0, 4)
    (8, 15, 2)
    >>> transform(-1, 9, 3, 4)
    (11, 9, 3)
    >>> transform(3, 6, 3, 4)
    (2, 8, 0)
    >>> transform(3, 1, 3, 4)
    (0, 10, 1)
    >>> transform(7, -1, 2, 4)
    (11, 12, 3)
    >>> transform(8, 1, 1, 4)
    (11, 10, 3)
    >>> transform(8, 4, 1, 4)
    (11, 8, 0)
    >>> transform(9, 7, 2, 4)
    (7, 6, 3)
    >>> transform(12, 10, 1, 4)
    (7, 1, 3)
    >>> transform(12, 13, 1, 4)
    (6, 0, 0)
    >>> transform(8, 16, 0, 4)
    (3, 11, 2)
    >>> transform(7, 15, 3, 4)
    (4, 11, 2)
    >>> transform(6, 12, 0, 4)
    (8, 13, 1)"""
    ghost_face = (row // cube_size, col // cube_size)
    if direction == 0:
        origin = (ghost_face[0], ghost_face[1] - 1)
    elif direction == 1:
        origin = (ghost_face[0] - 1, ghost_face[1])
    elif direction == 2:
        origin = (ghost_face[0], ghost_face[1] + 1)
    elif direction == 3:
        origin = (ghost_face[0] + 1, ghost_face[1])

    matches = mappings[ghost_face]
    if origin == matches[0]:
        assert (direction + 2) % 4 == matches[1]
        new_cube = matches[2]
        new_direction = matches[3]
    else:
        new_cube = matches[0]
        new_direction = matches[1]
        assert origin == matches[2]
        assert (direction + 2) % 4 == matches[3]
    d_row = row - origin[0]
    d_col = col - origin[1]


def transform_v1(row, col, direction, cube_size):
    if row == -1:
        assert direction == 3
        new_row = 3 * cube_size - 1
        new_col = col
        new_direction = direction
    elif row < 1 * cube_size and direction == 2:
        assert col < 2 * cube_size
        offset = 1 * cube_size - row
        new_row = 1 * cube_size
        new_col = 2 * cube_size - offset
        new_direction = 1
    elif row < 1 * cube_size and direction == 0:
        assert col >= 3 * cube_size
        offset = 1 * cube_size - row
        new_row = 2 * cube_size - 1 + offset
        new_col = 4 * cube_size - 1
        new_direction = 2
    elif row == 1 * cube_size - 1 and col < 1 * cube_size:
        assert direction == 3
        offset = 1 * cube_size - col
        new_row = 0
        new_col = 2 * cube_size - 1 + offset
        new_direction = 1
    elif row == 1 * cube_size - 1 and col < 2 * cube_size:
        assert direction == 3
        offset = 2 * cube_size - col
        new_row = 1 * cube_size - offset
        new_col = 2 * cube_size
        new_direction = 0
    elif row < 2 * cube_size and direction == 2:
        assert col == -1
        offset = 2 * cube_size - row
        new_row = 3 * cube_size - 1
        new_col = 3 * cube_size - 1 + offset
        new_direction = 3
    elif row < 2 * cube_size and direction == 0:
        assert col == 3 * cube_size
        offset = 2 * cube_size - row
        new_row = 2 * cube_size
        new_col = 3 * cube_size - 1 + offset
        new_direction = 1
    elif row == 2 * cube_size - 1 and direction == 3:
        assert 3 * cube_size <= col < 4 * cube_size
        offset = col - 3 * cube_size
        new_row = 2 * cube_size - 1 - offset
        new_col = 3 * cube_size - 1
        new_direction = 2
    elif row == 2 * cube_size and col < 1 * cube_size:
        assert direction == 1
        offset = 1 * cube_size - col
        new_row = 3 * cube_size - 1
        new_col = 2 * cube_size - 1 + offset
        new_direction = 3
    elif row == 2 * cube_size and col < 2 * cube_size:
        assert direction == 1
        offset = 2 * cube_size - col
        new_row = 2 * cube_size - 1 + offset
        new_col = 8
        new_direction = 0
    elif direction == 2:
        assert col == 2 * cube_size - 1 and 2 * cube_size <= row < 3 * cube_size
        offset = row - 2 * cube_size
        new_row = 2 * cube_size - 1
        new_col = 2 * cube_size - 1 - offset
        new_direction = 3
    elif direction == 0:
        assert col == 4 * cube_size and 2 * cube_size <= row < 3 * cube_size
        offset = row - 2 * cube_size
        new_row = 1 * cube_size - 1 - offset
        new_col = 3 * cube_size - 1
        new_direction = 2
    elif row == 3 * cube_size and col < 3 * cube_size:
        assert direction == 1
        offset = 3 * cube_size - col
        new_row = 2 * cube_size - 1
        new_col = offset - 1
        new_direction = 3
    elif row == 3 * cube_size and col < 4 * cube_size:
        assert direction == 1
        offset = 4 * cube_size - 1 - col
        new_row = 1 * cube_size + offset
        new_col = 0
        new_direction = 0
    else:
        raise ValueError(f"Unhandled coordinates/direction: {row, col, direction}")
    # elif case == 'actual':
    #     pass
    # else:
    #     raise ValueError(f"Unrecognized case: {case}")
    return new_row, new_col, new_direction

def solve(inp, debug=False):
    jungle_map, path, cube_size = format_input(inp)
    # if debug:
    #     print(path)
    #     for row in jungle_map:
    #         print(row)
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
                # if new_c == len(jungle_map[new_r]):
                #     new_c = 0
            elif direction == 1:
                new_r += 1
                # if new_r == len(jungle_map):
                #     new_r = 0
            elif direction == 2:
                new_c -= 1
                # if new_c == -1 or jungle_map[new_r][new_c] == -1:
                #     new_c = len(jungle_map[new_r]) - 1
            else:
                new_r -= 1
            # if debug:
            #     print(f"Attempting {new_r + 1, new_c + 1}, direction {direction}")
            in_range = False
            try:
                in_range = jungle_map[new_r][new_c] > 0
            except IndexError:
                pass
            if not in_range:
                if debug:
                    print(f"{new_r, new_c} not in range")
                new_r, new_c, new_direction = transform(new_r, new_c, direction, cube_size)
            # if new_c >= len(jungle_map[new_r]) or jungle_map[new_r][new_c] < 0:
            #     # if debug:
            #     #     print(f"{new_r + 1, new_c + 1} is out of bounds")
            #     # if direction in (0, 2):
            #     #     # if debug:
            #     #     #     print(f"{new_r+1, new_c+1} out of map, wrapping to {new_r+1, -jungle_map[new_r][new_c] + 1}")
            #     #     new_c = -jungle_map[new_r][new_c]
            #     if direction == 0:
            #         while jungle_map[new_r][new_c] < 0:
            #             new_c += 1
            #         # if debug:
            #         #     print(f"Updated to {new_r + 1, new_c + 1}")
            #     elif direction == 2:
            #         while new_c >= len(jungle_map[new_r]):
            #             new_c -= 1
            #         # if debug:
            #         #     print(f"Updated to {new_r + 1, new_c + 1}")
            #     elif direction == 1:
            #         new_r = 0
            #         while len(jungle_map[new_r]) <= new_c or jungle_map[new_r][new_c] <= 0:
            #             new_r += 1
            #         # if debug:
            #         #     print(f"Updated to {new_r + 1, new_c + 1}")
            #     else:
            #         new_r = len(jungle_map) - 1
            #         while len(jungle_map[new_r]) <= new_c or jungle_map[new_r][new_c] <= 0:
            #             new_r -= 1
            #         # if debug:
            #         #     print(f"Updated to {new_r + 1, new_c + 1}")
            if debug:
                print(f'Checking {new_r + 1, new_c + 1}, direction = {direction}')
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
        # if i % 20 == 0:
        #     print_map(jungle_map, walked)
        #     input()
        #     walked = {(row, col): direction}
    if debug:
        print_map(jungle_map, walked)
    row += 1
    col += 1
    print(row, col, direction)
    return 1000 * row + 4 * col + direction

def main(debug = False):
    return str(solve(parse_example(), True)) + '\n' + str(solve(parse_input(), debug))

if __name__=='__main__':
    doctest.testmod()
