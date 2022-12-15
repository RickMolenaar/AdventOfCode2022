import re

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

class Beacon:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other: 'Beacon'):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return 1_000_000_000_000 * self.x + self.y

class Scanner:
    def __init__(self, x, y, beacon: Beacon):
        self.x = x
        self.y = y
        self.beacon = beacon
        self.covered_distance = manhattan_distance(x, y, beacon.x, beacon.y)
        self.min_y = self.y - self.covered_distance
        self.max_y = self.y - self.covered_distance

    def covered_length(self, y):
        dy = abs(self.y - y)
        if dy > self.covered_distance:
            return (None, None)
        min_x = self.x - (self.covered_distance - dy)
        max_x = self.x + (self.covered_distance - dy)
        return (min_x, max_x)

    def print_covered_area(self):
        for dy in range(-self.covered_distance - 1, self.covered_distance + 2):
            min_x, max_x = self.covered_length(self.y + dy)
            if (min_x, max_x) == (None, None):
                print(f'{self.y+dy:>2} ' + '.' * (self.covered_distance * 2 + 3))
                continue
            line = f'{self.y+dy:>2} '
            for dx in range(-self.covered_distance - 1, self.covered_distance + 2):
                if self.beacon.y == self.y + dy and self.beacon.x == self.x + dx:
                    line += 'B'
                elif min_x <= self.x + dx <= max_x:
                    line += '#'
                else:
                    line += '.'
            print(line)


def parse_input(file = 'day15.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day15example.txt')

def format_input(inp) -> tuple[set[Beacon], list[Scanner]]:
    beacons = set()
    scanners = []
    for line in inp:
        sx, sy, bx, by = [int(x) for x in re.findall('[-]?\d+', line)]
        beacon = Beacon(bx, by)
        beacons.add(beacon)
        scanners.append(Scanner(sx, sy, beacon))
    #     print(sx, sy, bx, by, min_x_global, max_x_global)
        
    # print(min_x_global, max_x_global)
    # print('-'*15)
    return beacons, scanners

def solve(inp, search_space, debug=False):
    beacons, scanners = format_input(inp)
    # print(len(beacons), len(scanners))
    # to_check = 9 if debug else 2_000_000
    scanners = sorted(scanners, key = lambda s: s.min_y)
    scanners_to_check = [s for s in scanners if s.min_y <= 0 and s.max_y >= 0]
    unused_scanners = [s for s in scanners if s.min_y > 0]
    for y in range(0, search_space + 1):
        while unused_scanners and unused_scanners[0].min_y == y:
            scanners_to_check.append(unused_scanners.pop())
        scanners_to_check = [s for s in scanners_to_check if s.max_y >= y]
        if y % 10000 == 0:
            print(y / search_space * 100, '%')
        covered_distances = []
        for scanner in scanners:
            dist = scanner.covered_length(y)
            if dist != (None, None) and dist[0] <= search_space and dist[1] >= 0:
                covered_distances.append(dist)
        covered_distances = sorted(covered_distances)
        covered_amount = 0
        # covered = set()
        last_x = 0
        # beacons_to_check = [beacon for beacon in beacons if beacon.y == y]
        for dist in covered_distances:
            x1, x2 = dist
            # if last_x is None:
            #     last_x = x1
            if x1 > last_x:
                assert x1 - last_x == 1
                # print(last_x, y, last_x * 4_000_000 + y)
                return last_x * 4_000_000 + y
            x1 = max(x1, last_x)
            x2 = min(x2, search_space)
            covered_amount += max(x2 + 1 - x1, 0)
            # for beacon in beacons_to_check:
            #     if x1 <= beacon.x <= x2:
            #         covered_amount -= 1
            # if debug:
            #     print(x1, x2, covered_amount)
            last_x = max(x2 + 1, last_x)
            if last_x > search_space:
                break
    return covered_amount

def main(debug = False):
    return str(solve(parse_example(), 20, True)) + '\n' + str(solve(parse_input(), 4_000_000, False))
