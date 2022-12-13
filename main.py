import argparse
import datetime
import importlib
import requests
import time

from bs4 import BeautifulSoup, Tag

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
    inp = format_input(inp)
    return None

def main(debug = False):
    return str(solve(parse_example(), True)) + '\\n' + str(solve(parse_input(), debug))
"""

def init(day: int) -> None:
    global __test__, solve, parse_input, parse_example
    module = importlib.import_module(f"day{day:0>2}")
    solve = module.solve
    parse_input = module.parse_input
    parse_example = module.parse_example
    __test__ = {'solve': solve}

def generate(day: int) -> None:
    if day <= datetime.datetime.today().day:
        input_page = get_page(f"/2022/day/{day}/input")
        if input_page.status_code != 200:
            print(input_page.status_code, input_page.reason)
            open(f"day{day:0>2}.txt", "w").close()
        else:
            with open(f"day{day:0>2}.txt", "w") as f:
                f.write(input_page.text)

        problem_page = get_page(f"/2022/day/{day}")
        if problem_page.status_code != 200:
            print(problem_page.status_code, problem_page.reason)
            open(f"day{day:0>2}.txt", "w").close()
            open(f"day{day:0>2}example.txt", "w").close()
        else:
            problem_page = BeautifulSoup(problem_page.content, features='html.parser')
            part1 = problem_page.find(name='article')
            example_candidates = find_example(part1)
            if len(example_candidates) == 1:
                example = example_candidates[0][1]
                print('Writing example to file:')
                print(example.text)
                with open(f"day{day:0>2}example.txt", "w") as f:
                    f.write(example.text)
            else:
                for candidate in example_candidates:
                    print('Potential example:')
                    print(candidate[0].text)
                    print(candidate[1].text)
                    print('=' * 30)
                open(f"day{day:0>2}example.txt", "w").close()
    else:
        open(f"day{day:0>2}.txt", "w").close()
        open(f"day{day:0>2}example.txt", "w").close()

    with open(f"day{day:0>2}.py", "w") as f:
        f.write(TEMPLATE_FILE.format(day = day))

def get_page(location: str) -> requests.Response:
    with open('session.cookie') as f:
        cookie = f.readline()
    if not location.startswith('/'):
        location = '/' + location
    return requests.get(f'https://adventofcode.com' + location, cookies={'session': cookie})

def find_example(article: Tag) -> list[tuple[str, str]]:
    children = [c for c in list(article.children) if c != '\n']
    candidates = find_example_candidates(children)
    if not candidates:
        candidates = find_example_candidates(children, strict=False)
        if not candidates:
            print('Could not find an example')
    if len(candidates) > 1:
        print('Multiple possible examples found')
    return candidates

def find_example_result(article: Tag) -> list[str]:
    code_elements = article.find_all(name='code')
    return [el for el in code_elements if el.find(name='em')]

def find_example_candidates(elements, strict = True):
    candidates = []
    to_find = 'for example' if strict else 'example'
    for i, el in enumerate(elements):
        if i == len(elements) - 1:
            continue
        if elements[i+1].name == 'pre':
            if to_find in el.text.lower():
                candidates.append((el, elements[i+1]))
    return candidates

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--day', help="Which day to run")
    parser.add_argument('-g', '--generate', action='store_true',  help="Whether todays files should be generated")
    parser.add_argument('-t', '--time', action='store_true')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    if args.day is None:
        day = datetime.datetime.today().day
    else:
        day = int(args.day)
    
    if args.generate:
        generate(day)
    elif args.time:
        module = importlib.import_module(f"day{day:0>2}")
        t0 = time.time()
        print(module.main())
        print(f'Done in {time.time() - t0} ms')
    else:
        # init(args.day)
        # if doctest.testmod(verbose = args.debug).failed == 0:
        #     print(solve(parse_input(), args.debug))
        day = f'{day:0>2}'
        watcher = pywatch.Watcher(f'day{day}.py', 'main', f'day{day}example.txt', f'day{day}.txt')
        watcher.watch()