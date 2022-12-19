import re

def parse_input(file = 'day19.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)[:3]

def parse_example():
    return parse_input('day19example.txt')

def format_input(inp):
    costs = []
    for line in inp:
        costs.append(list(re.findall('\d+', line)))
    return costs

def critical_resource(costs, production, produced):
    r1, r2 = costs.keys()
    required = { r1: costs[r1] - produced[r1], r2: costs[r2] - produced[r2] }
    if production[r1] == 0 and production[r2] == 0:
        return r1 if costs[r1] > costs[r2] else r2
    if production[r1] == 0:
        return r1
    if production[r2] == 0:
        return r2
    if required[r1] / production[r1] > required[r2] / production[r2]:
        return r2
    if required[r1] / production[r1] < required[r2] / production[r2]:
        return r1
    if production[r1] > production[r2]:
        return r2
    return r1

def affordable(cost, produced):
    for resource in cost:
        if produced[resource] < cost[resource]:
            return False
    return True

def format_costs(ore_cost, clay_cost, obs_ore_cost, obs_clay_cost, geode_ore_cost, geode_obs_cost):
    return {
        'ore': {'ore': int(ore_cost)},
        'clay': {'ore': int(clay_cost)},
        'obs': {'ore': int(obs_ore_cost), 'clay': int(obs_clay_cost)},
        'geode': {'ore': int(geode_ore_cost), 'obs': int(geode_obs_cost)}
    }

def find_max_geodes(blueprint_id, costs, time_remaining, production, produced, choices = None):
    if choices is None:
        choices = []
    # if blueprint_id == '2' and choices == ['ore', 'ore', 'clay', 'clay', 'clay', 'clay', 'clay', 'obs', 'obs', 'obs', 'obs', 'obs', 'geode', 'obs', 'geode', 'geode'][:len(choices)]:
    #     print(24 - time_remaining, produced)
    # if len(choices) < 8:
    #     print(production, choices, passes)
    if time_remaining == 0:
        return produced['geode']
    if time_remaining < 0:
        raise ValueError
    
    max_producers = {
        'ore': 0,
        'clay': 0,
        'obs': 0,
        'geode': 99
    }
    for bot in costs:
        for res in costs[bot]:
            max_producers[res] = max(max_producers[res], costs[bot][res])

    if affordable(costs['geode'], produced):
        producable = ['geode']
    else:
        producable = []
        for bot in costs:
            if production[bot] >= max_producers[bot]:
                continue
            for resource in costs[bot]:
                if production[resource] == 0:
                    break
            else:
                producable.append(bot)
    max_result = 0
    for choice in producable[::-1]:
        new_production = production.copy()
        new_produced = produced.copy()
        new_time_remaining = time_remaining
        while not affordable(costs[choice], new_produced):
            for res in new_production:
                new_produced[res] += new_production[res]
            new_time_remaining -= 1
            if new_time_remaining == 0:
                max_result = max(max_result, new_produced['geode'])
                break
        else:
            for res in costs[choice]:
                new_produced[res] -= costs[choice][res]
            for res in new_production:
                new_produced[res] += new_production[res]
            new_production[choice] += 1
            new_time_remaining -= 1
            res = find_max_geodes(blueprint_id, costs, new_time_remaining, new_production, new_produced, choices + [choice])
            if res > max_result:
                max_result = res
            # if time_remaining == 24:
            #     print(max_result)
    return max_result

def solve(inp, debug=False):
    raw_costs = format_input(inp)
    total = 1
    TIME = 32
    for blueprint_id, ore_cost, clay_cost, obs_ore_cost, obs_clay_cost, geode_ore_cost, geode_obs_cost in raw_costs:
        print(f'Checking blueprint {blueprint_id, ore_cost, clay_cost, obs_ore_cost, obs_clay_cost, geode_ore_cost, geode_obs_cost}... ', end='')
        costs = format_costs(ore_cost, clay_cost, obs_ore_cost, obs_clay_cost, geode_ore_cost, geode_obs_cost)
        production = {
        'ore': 1,
        'clay': 0,
        'obs': 0,
        'geode': 0,
        None: 0
        }
        produced = {
            'ore': 0,
            'clay': 0,
            'obs': 0,
            'geode': 0,
            None: 0
        }
        res = find_max_geodes(blueprint_id, costs, TIME, production, produced)
        # quality = int(blueprint_id) * res
        # print(f"Quality: {quality}")
        # total = quality
        print(f"Max geodes: {res}")
        total *= res
    return total

def main(debug = False):
    # print(solve(parse_example(), True))
    return str(solve(parse_input(), debug))
