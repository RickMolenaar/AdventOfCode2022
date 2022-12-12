def parse_input(file = 'day12.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day12example.txt')

def format_input(inp):
    heightmap = []
    distance_map = []
    for i, row in enumerate(inp):
        heightmap.append([ord(c) for c in row])
        distance_map.append([9999] * len(row))
        if 'S' in row:
            start = (i, row.index('S'))
            heightmap[-1][start[1]] = ord('a')
            distance_map[-1][start[1]] = 0
        if 'E' in row:
            end = (i, row.index('E'))
            heightmap[-1][end[1]] = ord('z')
    return heightmap, distance_map, start, end

def get_neighbors(point, max_size):
    neighbors = []
    for add in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        neighbor = (point[0] + add[0], point[1] + add[1])
        if 0 <= neighbor[0] < max_size[0] and 0 <= neighbor[1] < max_size[1]:
            neighbors.append(neighbor)
    return neighbors

def solve(inp, debug=False):
    heightmap, distance_map, start, end = format_input(inp)
    size = (len(heightmap), len(heightmap[0]))
    to_update = {start}
    max_iters = 500
    iters = 0
    while to_update and iters < max_iters:
        if iters % 100 == 0:
            print(iters, len(to_update))
        # if iters < 5:
        #     print([(point, distance_map[point[0]][point[1]]) for point in to_update])
        iters += 1
        for point in to_update.copy():
            height = heightmap[point[0]][point[1]]
            distance = distance_map[point[0]][point[1]]
            for neighbor in get_neighbors(point, size):
                n_height = heightmap[neighbor[0]][neighbor[1]]
                if n_height > height + 1:
                    continue
                n_distance = distance_map[neighbor[0]][neighbor[1]]
                if distance + 1 < n_distance:
                    distance_map[neighbor[0]][neighbor[1]] = distance + 1
                    to_update.add(neighbor)
            to_update.remove(point)
    if iters >= max_iters:
        raise ValueError
    if debug:
        print(distance_map[end[0]][end[1]])
    return distance_map[end[0]][end[1]]

def main(debug = False):
    return str(solve(parse_example(), True)) + '\n' + str(solve(parse_input(), debug))
