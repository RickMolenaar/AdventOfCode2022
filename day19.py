import re

def parse_input(file = 'day19.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day19example.txt')

def format_input(inp):
    costs = []
    for line in inp:
        costs.append(list(re.findall('\d+', line)))
    return costs

def find_max_geodes(blueprint_id, ore_cost, clay_cost, obs_ore_cost, obs_clay_cost, geode_ore_cost, geode_obs_cost):
    pass

def solve(inp, debug=False):
    costs = format_input(inp)
    for blueprint_id, ore_cost, clay_cost, obs_ore_cost, obs_clay_cost, geode_ore_cost, geode_obs_cost in costs:
        pass
    return None

def main(debug = False):
    return str(solve(parse_example(), True)) + '\n' + str(solve(parse_input(), debug))
