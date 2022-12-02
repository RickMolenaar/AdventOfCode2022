import argparse
import doctest
import importlib

TEMPLATE_FILE = """def parse_input():
    with open('day{day:0>2}.txt') as f:
        s = f.readlines()
    return s

def solve(inp, debug=False):
    \"\"\"
    >>> solve('''
    ... ''')
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
    if day <= datetime.datetime.today().day:
        import requests
        with open('session.cookie') as f:
            cookie = f.readline()
        page = requests.get(f'https://adventofcode.com/2022/day/{day}/input', cookies={'session': cookie})
        if page.status_code != 200:
            print(page.status_code, page.reason)
            open(f"day{day:0>2}.txt", "w").close()
        else:
            with open(f"day{day:0>2}.txt", "w") as f:
                f.write(page.text)
    else:
        open(f"day{day:0>2}.txt", "w").close()
    with open(f"day{day:0>2}.py", "w") as f:
        f.write(TEMPLATE_FILE.format(day = day))

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
            print(solve(parse_input(), True))