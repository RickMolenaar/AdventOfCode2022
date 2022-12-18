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

def find_total_flow(valves, distances, priorities, time_remaining, cache, debug = False):
    location = 'AA'
    opened = set()
    total_flow = 0
    route = [location]
    step = 0
    while len(opened) < len(valves) and time_remaining > 0:
        to_choose = priorities[step]
        best_valves = [k for k in distances[location] if k not in opened]
        if len(best_valves) - 1 < to_choose:
            return None, None, priorities[:step + 1]
        best_valves = sorted(best_valves, key = lambda v: valves[v] * (time_remaining - distances[location][v] - 1), reverse=True)
        new_loc = best_valves[to_choose]
        time_remaining -= distances[location][new_loc] + 1
        if time_remaining < 0:
            return total_flow, route, None
        opened.add(new_loc)
        total_flow += time_remaining * valves[new_loc]
        if debug:
            print(f'Opening valve {new_loc}, adding {time_remaining * valves[new_loc]} pressure')
        location = new_loc
        route.append(new_loc)
        cache_key = (new_loc, frozenset(route))
        if cache_key in cache and total_flow < cache[cache_key]:
            return None, None, priorities[:step+1]
        else:
            cache[cache_key] = total_flow
        step += 1
    return total_flow, route, None

# def find_total_flow_by_order(valves, distances, order, time_remaining):
#     loc = 'AA'
#     total = 0
#     for valve in order:
#         time_remaining -= distances[loc][valve] + 1
#         if time_remaining <= 0:
#             return total
#         total += valves[valve] * time_remaining
#         loc = valve
#         # print(valve, time_remaining, total)
#     return total

# def randomize_paths():


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
    # distances = build_distance_map(valves, connections)
    # if len(valves) < 10:
    #     print(find_total_flow_by_order(valves, distances, ['DD', 'BB', 'JJ', 'HH', 'EE', 'CC'], 30))
    # return None
    # return find_best_flow(valves, connections, 30)
    min_my_valves = (len(valves) - 1) // 2 + 1
    best = 0
    best_selections = []
    lowest_best_selection = 0
    for my_valve_amount in range(min_my_valves, min_my_valves + 4):
        print(f'Using {my_valve_amount} valves myself')
        for my_valves in itertools.combinations(valves.keys(), my_valve_amount):
            my_flow_rates = {valve: valves[valve] for valve in my_valves}
            f1 = find_best_flow(my_flow_rates, connections, 26)
            # if f1 > lowest_best_selection:
            #     best_selections.append((my_valves, f1))
            #     best_selections = sorted(best_selections)
            #     if len(best_selections) > 30:
            #         best_selections.pop()
            #         lowest_best_selection = best_selections[0][1]
            if f1 < 1000:
                continue
            elephalves = [valve for valve in valves if valve not in my_valves]
            elephant_flow_rates = {valve: valves[valve] for valve in elephalves}
            f2 = find_best_flow(elephant_flow_rates, connections, 26)
            if f1 + f2 > best:
                best = f1 + f2
                print(my_valves, f1, f2, best)
                
    return best

def find_best_flow(valves, connections, time):
    distances = build_distance_map(valves, connections)
    # if debug:
    #     for key in distances:
    #         print(key, distances[key])
    # priorities = [0] * len(valves)
    total_best_flow = 0
    max_prio = max((len(distances[k]) for k in distances))
    bad_starts = set()
    cache = {}
    skipped = 0
    total = 0
    bad_start_length = 0
    for total_deferred_priorities in range(8):
        # print(total_deferred_priorities)
        for separations in separate_number(total_deferred_priorities, min(10, len(valves)), max_prio + 1):
            # print(separations)
            for priorities in distinct_permutations(separations):
                total += 1
                for k in range(2, bad_start_length):
                    if tuple(priorities[:k+1]) in bad_starts:
                        skipped += 1
                        break
                else:
                    best_flow, route, bad_start = find_total_flow(valves, distances, list(priorities), time, cache)
                    if best_flow is not None and best_flow > total_best_flow:
                        total_best_flow = best_flow
                        # find_total_flow(valves, distances, list(priorities), 30, True)
                        # print(route, best_flow)
                    elif bad_start:
                        bad_starts.add(tuple(bad_start))
                        bad_start_length = max(bad_start_length, len(bad_start))
    # print(f"{skipped} skipped out of {total} ({len(bad_starts)} skippable)")
    # print('-'*10)
    # if debug:
    #     print(route)

    return total_best_flow

def main(debug = False):
    return str(solve(parse_example(), True)) + '\n' + str(solve(parse_input(), debug))
