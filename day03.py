import string
def parse_input():
    with open('day03.txt') as f:
        s = ''.join(f.readlines())
    return s

def find_badge(group: list[str]):
    for c in group[0]:
        if c in group[1] and c in group[2]:
            return string.ascii_letters.index(c) + 1
    raise ValueError('No badge found')

def solve(inp, debug=False):
    """
    >>> solve('''vJrwpWtwJgWrhcsFMMfFFhFp
    ... jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
    ... PmmdzqPrVvPwwTWBwg
    ... wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
    ... ttgJtRGJQctTZtZT
    ... CrZsJsPPZsGzwwsLwLmpwMDw''')
    70
    """
    tot = 0
    group = []
    for line in inp.split('\n'):
        group.append(line.rstrip())
        if len(group) == 3:
            tot += find_badge(group)
            group = []
    return tot

    # PART 1
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