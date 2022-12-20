def parse_input(file = 'day18.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day18example.txt')

def format_input(inp):
    rocks = set()
    min_x = min_y = min_z = max_x = max_y = max_z = 0
    for line in inp:
        rock = tuple(map(int, line.split(',')))
        rocks.add(rock)
        min_x = min(min_x, rock[0])
        min_y = min(min_y, rock[1])
        min_z = min(min_z, rock[2])
        max_x = max(max_x, rock[0])
        max_y = max(max_y, rock[1])
        max_z = max(max_z, rock[2])
    return rocks, min_x - 1, min_y - 1, min_z - 1, max_x + 1, max_y + 1, max_z + 1

def solve(inp, debug=False):
    rocks, min_x, min_y, min_z, max_x, max_y, max_z = format_input(inp)
    # total_sides = 0
    # for rock in rocks:
    #     for d in (-1, 1):
    #         for dir in range(3):
    #             to_check = list(rock)
    #             to_check[dir] += d
    #             if tuple(to_check) not in rocks:
    #                 total_sides += 1
    blocks_to_check = set()
    blocks_to_check.add((min_x, min_y, min_z))
    checked = set()
    total_sides = 0
    while blocks_to_check:
        # print(blocks_to_check)
        (x, y, z) = blocks_to_check.pop()
        for d in (-1, 1):
            for dir in range(3):
                to_check = [x, y, z]
                to_check[dir] += d
                to_check = tuple(to_check)
                if to_check in rocks:
                    total_sides += 1
                    continue
                if to_check in checked:
                    continue
                if min_x <= to_check[0] <= max_x and min_y <= to_check[1] <= max_y and min_z <= to_check[2] <= max_z:
                    blocks_to_check.add(to_check)
        checked.add((x, y, z))
    return total_sides

def main(debug = False):
    return str(solve(parse_example(), True)) + '\n' + str(solve(parse_input(), debug))
