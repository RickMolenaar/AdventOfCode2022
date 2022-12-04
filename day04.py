def parse_input():
    with open('day04.txt') as f:
        s = ''.join(f.readlines())
    return s

def solve(inp, debug=False):
    """
    >>> solve('''2-4,6-8
    ... 2-3,4-5
    ... 5-7,7-9
    ... 2-8,3-7
    ... 6-6,4-6
    ... 2-6,4-8
    ... ''')
    4
    """
    tot = 0
    for line in inp.rstrip().split('\n'):
        first, second = tuple(map(lambda p: tuple(map(int, p.split('-'))), line.split(',')))
        # if (first[0] <= second[0] and first[1] >= second[1]) or (first[0] >= second[0] and first[1] <= second[1]):
        #     tot += 1
        if not (first[1] < second[0] or first[0] > second[1]):
            tot += 1
    return tot