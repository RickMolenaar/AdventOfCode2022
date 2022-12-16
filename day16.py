import itertools
import re

from more_itertools import distinct_permutations

def parse_input(file = 'day16.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day16example.txt')

def format_input(inp):
    valves = {}
    connections = {}
    for line in inp:
        flowrate = int(re.findall('\d+', line)[0])
        caps = re.findall('[A-Z][A-Z]', line)
        valve, tunnels = caps[0], caps[1:]
        if flowrate > 0:
            valves[valve] = flowrate
        connections[valve] = tunnels
    return valves, connections

def build_distance_map(valves, tunnels):
    distances = {t_start: {t_end: 9999 for t_end in tunnels} for t_start in tunnels}
    # print([t for t in tunnels])
    # print(distances)
    for t_start in tunnels:
        for t_end in tunnels[t_start]:
            distances[t_start][t_end] = 1
            distances[t_end][t_start] = 1
    # print(distances)
    to_update = set(tunnels)
    iters = 0
    while to_update:
        iters += 1
        if iters > 10000:
            raise ValueError
        t_start = to_update.pop()
        dists = distances[t_start]
        for c1 in dists:
            if dists[c1] == 1:
                for c2 in dists:
                    if dists[c2] + 1 < distances[c1][c2]:
                        to_update.add(c1)
                        distances[c1][c2] = dists[c2] + 1
    for k in distances:
        del distances[k][k]
        for tunnel in tunnels:
            if tunnel not in valves and tunnel != k:
                del distances[k][tunnel]
    return {valve: distances[valve] for valve in ['AA'] + list(valves.keys())}

def find_total_flow(valves, distances, priorities, time_remaining, debug = False):
    location = 'AA'
    opened = set()
    total_flow = 0
    route = [location]
    used_priorities = []
    while len(opened) < len(valves) and time_remaining > 0:
        to_choose = priorities.pop()
        best_valves = [k for k in distances[location] if k not in opened]
        if len(best_valves) - 1 < to_choose:
            return None, None, used_priorities
        best_valves = sorted(best_valves, key = lambda v: valves[v] * (time_remaining - distances[location][v] - 1), reverse=True)
        new_loc = best_valves[to_choose]
        time_remaining -= distances[location][new_loc] + 1
        if time_remaining < 0:
            return total_flow, route, used_priorities
        opened.add(new_loc)
        total_flow += time_remaining * valves[new_loc]
        if debug:
            print(f'Opening valve {new_loc}, adding {time_remaining * valves[new_loc]} pressure')
        location = new_loc
        route.append(new_loc)
        used_priorities.append(to_choose)
    return total_flow, route, used_priorities

def separate_number(number, partitions, max_partition = None):
    if max_partition is None:
        max_partition = number
    if partitions == 1 and max_partition >= number:
        yield [number]
    elif partitions > 1:
        for i in range(min(max_partition, number) + 1):
            for separation in separate_number(number - i, partitions - 1, i):
                yield [i] + separation

def solve(inp, debug=False):
    valves, connections = format_input(inp)
    distances = build_distance_map(valves, connections)
    print(len(valves))
    # if debug:
    #     for key in distances:
    #         print(key, distances[key])
    # priorities = [0] * len(valves)
    total_best_flow = 0
    max_prio = max((len(distances[k]) for k in distances))
    previous = [999] * len(valves)
    for total_deferred_priorities in range(20):
        print(total_deferred_priorities)
        for separations in separate_number(total_deferred_priorities, min(10, len(valves)), max_prio + 1):
            # print(separations)
            for priorities in distinct_permutations(separations):
                # print(priorities)
                if priorities[:len(previous)] == previous:
                    continue
                best_flow, route, previous = find_total_flow(valves, distances, list(priorities), 30)
                if route == ['AA', 'DD', 'BB', 'JJ', 'HH', 'EE', 'CC']:
                    print(route, best_flow, priorities)
                if best_flow is not None and best_flow > total_best_flow:
                    total_best_flow = best_flow
                    # find_total_flow(valves, distances, list(priorities), 30, True)
                    print(route, best_flow)
    print('-'*10)
    # if debug:
    #     print(route)
    return total_best_flow

def main(debug = False):
    return str(solve(parse_example(), True)) + '\n' + str(solve(parse_input(), debug))
