import re

def parse_input(file = 'day22.txt') -> list[str]:
    with open(file) as f:
        s = map(lambda l: l.rstrip('\n'), f.readlines())
    return list(s)

def parse_example() -> list[str]:
    return parse_input('day22example.txt')

def format_input(inp: list[str]) -> tuple[list[list[int]], str]:
    jungle_map = []
    for line in inp[:-2]:
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
    path = re.findall('\d+[LR]?', inp[-1])
    # print(len(path))
    return jungle_map, path

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

def solve(inp, debug=False):
    jungle_map, path = format_input(inp)
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
            if direction == 0:
                new_c += 1
                if new_c == len(jungle_map[new_r]):
                    new_c = 0
            elif direction == 1:
                new_r += 1
                if new_r == len(jungle_map):
                    new_r = 0
            elif direction == 2:
                new_c -= 1
                if new_c == -1 or jungle_map[new_r][new_c] == -1:
                    new_c = len(jungle_map[new_r]) - 1
            else:
                new_r -= 1
            # if debug:
            #     print(f"Attempting {new_r + 1, new_c + 1}, direction {direction}")
            if new_c >= len(jungle_map[new_r]) or jungle_map[new_r][new_c] < 0:
                # if debug:
                #     print(f"{new_r + 1, new_c + 1} is out of bounds")
                # if direction in (0, 2):
                #     # if debug:
                #     #     print(f"{new_r+1, new_c+1} out of map, wrapping to {new_r+1, -jungle_map[new_r][new_c] + 1}")
                #     new_c = -jungle_map[new_r][new_c]
                if direction == 0:
                    while jungle_map[new_r][new_c] < 0:
                        new_c += 1
                    # if debug:
                    #     print(f"Updated to {new_r + 1, new_c + 1}")
                elif direction == 2:
                    while new_c >= len(jungle_map[new_r]):
                        new_c -= 1
                    # if debug:
                    #     print(f"Updated to {new_r + 1, new_c + 1}")
                elif direction == 1:
                    new_r = 0
                    while len(jungle_map[new_r]) <= new_c or jungle_map[new_r][new_c] <= 0:
                        new_r += 1
                    # if debug:
                    #     print(f"Updated to {new_r + 1, new_c + 1}")
                else:
                    new_r = len(jungle_map) - 1
                    while len(jungle_map[new_r]) <= new_c or jungle_map[new_r][new_c] <= 0:
                        new_r -= 1
                    # if debug:
                    #     print(f"Updated to {new_r + 1, new_c + 1}")
            # if debug:
            #     print(f'Checking {new_r + 1, new_c + 1}, direction = {direction}')
            if jungle_map[new_r][new_c] == 1:
                row, col = new_r, new_c
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
    # print_map(jungle_map, walked)
    row += 1
    col += 1
    print(row, col, direction)
    return 1000 * row + 4 * col + direction

def main(debug = False):
    return str(solve(parse_example(), True)) + '\n' + str(solve(parse_input(), debug))
