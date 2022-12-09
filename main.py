import argparse
import doctest
import importlib

import pywatch

TEMPLATE_FILE = """def parse_input(file = 'day{day:0>2}.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day{day:0>2}example.txt')

def format_input(inp):
    return inp

def solve(inp, debug=False):
    \"\"\"
    >>> solve(parse_example())
    None
    \"\"\"
    inp = format_input(inp)
    return None

def main(debug = False):
    return str(solve(parse_example(), debug)) + '\\n' + str(solve(parse_input(), debug))
"""

def init(day):
    global __test__, solve, parse_input, parse_example
    module = importlib.import_module(f"day{day:0>2}")
    solve = module.solve
    parse_input = module.parse_input
    parse_example = module.parse_example
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
    open(f"day{day:0>2}example.txt", "w").close()

    with open(f"day{day:0>2}.py", "w") as f:
        f.write(TEMPLATE_FILE.format(day = day))

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--day', help="Which day to run")
    parser.add_argument('-g', '--generate', action='store_true',  help="Whether todays files should be generated")
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    if args.day is None:
        import datetime
        args.day = datetime.datetime.today().day
    
    if args.generate:
        generate(args.day)
    else:
        # init(args.day)
        # if doctest.testmod(verbose = args.debug).failed == 0:
        #     print(solve(parse_input(), args.debug))
        day = f'{args.day:0>2}'
        watcher = pywatch.Watcher(f'day{day}.py', 'main', f'day{day}example.txt', f'day{day}.txt')
        watcher.watch()