import string
def parse_input():
    with open('day03.txt') as f:
        s = ''.join(f.readlines())
    return s

def solve(inp, debug=False):
    """
    >>> solve('''vJrwpWtwJgWrhcsFMMfFFhFp
    ... jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
    ... PmmdzqPrVvPwwTWBwg
    ... wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
    ... ttgJtRGJQctTZtZT
    ... CrZsJsPPZsGzwwsLwLmpwMDw''')
    157
    """
    tot = 0
    for line in inp.split('\n'):
        line = line.strip()
        first, second = line[:len(line) // 2], line[len(line) // 2:]
        # print(line)
        assert len(first) == len(second)
        first = [c for c in first]
        second = [c for c in second]
        for c in first:
            if c in second:
                tot += string.ascii_letters.index(c) + 1
                break
    return tot