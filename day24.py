from collections import defaultdict

def parse_input(file = 'day24.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day24example.txt')

def format_input(inp):
    expedition = (0, inp[0].index('.'))
    target = (len(inp) - 1, inp[-1].index('.'))
    blizzards = set()
    for row, line in enumerate(inp[:-1]):
        if row == 0:
            continue
        for col, c in enumerate(line):
            if c in '>v<^':
                blizzards.add((row, col, c))
    return expedition, target, frozenset(blizzards), len(inp[0]) - 1, len(inp) - 1

def get_next_blizzard_pos(blizzard, max_x, max_y):
    row, col, dir = blizzard
    if dir == '>':
        new_r, new_c = row, col + 1
    elif dir == 'v':
        new_r, new_c = row + 1, col
    elif dir == '<':
        new_r, new_c = row, col - 1
    else:
        new_r, new_c = row - 1, col
    if new_r == 0:
        new_r = max_y - 1
    if new_c == 0:
        new_c = max_x - 1
    if new_r == max_y:
        new_r = 1
    if new_c == max_x:
        new_c = 1
    return (new_r, new_c, dir)

def find_possible_locations(loc, target, blizzards, max_x, max_y):
    possible_moves = [(loc[0] + dr, loc[1] + dc) for (dr, dc) in ((-1, 0), (1, 0), (0, -1), (0, 1), (0, 0))]
    possible_moves = [(r, c) for (r, c) in possible_moves if (r, c) == (0, 1) or (r, c) == target or (0 < r < max_y and 0 < c < max_x)]
    for row, col, dir in blizzards:
        if (row, col) in possible_moves:
            possible_moves.remove((row, col))
            if not possible_moves:
                break
    
    return possible_moves

def get_new_blizzards(blizzards, max_x, max_y):
    new_blizzards = set()
    for blizz in blizzards:
        new_r, new_c, dir = get_next_blizzard_pos(blizz, max_x, max_y)
        new_blizzards.add((new_r, new_c, dir))
    return frozenset(new_blizzards)

def print_blizzards(blizzards, max_x, max_y):
    print('#.' + '#' * (max_x - 1))
    for row in range(1, max_y):
        print('#', end = '' )
        for col in range(1, max_x):
            blizzes = [direc for r, c, direc in blizzards if (r, c) == (row, col)]
            if len(blizzes) > 1:
                print(len(blizzes), end = '')
            elif len(blizzes) == 1:
                print(blizzes[0], end = '')
            else:
                print('.', end = '')
        print('#')
    print('#' * (max_x - 1) + '.#')

def solve(inp, debug=False):
    expedition, target, blizzards, max_x, max_y = format_input(inp)
    assert target[0] == max_y and target[1] == max_x - 1
    max_time = 950
    min_time = 0
    possible_states = defaultdict(set)
    possible_states[0].add((expedition, 0))
    distance_cutoff = -30
    max_distance = {0: 0, 1: 0, 2: 0}
    while min_time < max_time:
        print(min_time)
        # if debug:
        #     print(sorted(possible_states[min_time]))
        #     print_blizzards(blizzards, max_x, max_y)
        blizzards = get_new_blizzards(blizzards, max_x, max_y)
        for loc, goals_reached in possible_states[min_time]:
            if goals_reached < 2 and max_distance[goals_reached + 1] > -distance_cutoff:
                continue
            if goals_reached == 0 or goals_reached == 2:
                distance = loc[0] + loc[1] - 1
            else:
                distance = max_y - loc[0] + max_x - 1 - loc[1]
            # if goals_reached == 1:
            #     print(distance)
            if distance > max_distance[goals_reached]:
                max_distance[goals_reached] = distance
            elif distance - max_distance[goals_reached] < distance_cutoff:
                continue
            for move in find_possible_locations(loc, target, blizzards, max_x, max_y):
                if move == target and goals_reached == 2:
                    return min_time + 1
                elif move == target:
                    new_goals = 1
                elif move == (0, 1) and goals_reached == 1:
                    new_goals = 2
                else:
                    new_goals = goals_reached
                possible_states[min_time + 1].add((move, new_goals))
        min_time += 1
    print(max_distance)
    return -1

def main(debug = False):
    return str(solve(parse_example(), True)) + '\n' + str(solve(parse_input(), debug))
