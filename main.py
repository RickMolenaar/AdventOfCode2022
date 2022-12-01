import argparse
import doctest
import importlib

TEMPLATE_FILE = """def parse_input():
    with open('day01.txt') as f:
        s = f.readlines()
    return s

def solve():
    \"\"\"
    >>> solve()
    None
    \"\"\"
    return None
"""

def init(day):
    global __test__, solve, parse_input
    module = importlib.import_module(f"day{day:0>2}")
    solve = module.solve
    parse_input = module.parse_input
    __test__ = {'solve': solve}

def generate(day):
    open(f"day{day:0>2}.txt", "w").close()
    with open(f"day{day:0>2}.py", "w") as f:
        f.write(TEMPLATE_FILE)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--day', help="Which day to run")
    parser.add_argument('-g', '--generate', action='store_true',  help="Whether todays files should be generated")
    args = parser.parse_args()
    if args.day is None:
        import datetime
        args.day = datetime.datetime.today().day
    
    if args.generate:
        generate(args.day)
    else:
        init(args.day)
        if doctest.testmod().failed == 0:
            print(solve(parse_input()))