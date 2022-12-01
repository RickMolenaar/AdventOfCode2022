def parse_input():
    inp = []
    with open('day01.txt') as f:
        ls = []
        for line in f:
            if line != '\n':
                ls.append(int(line))
            else:
                inp.append(ls)
                ls = []
    return inp

def solve(inp: list[list[int]]):
    """
    >>> solve([[1000, 2000, 3000], [4000], [5000, 6000], [7000, 8000, 9000], [10000]])
    45000
    """
    maxes = []
    for l in inp:
        if len(maxes) < 3:
            maxes = sorted(maxes + [sum(l)])
            continue
        if sum(l) > maxes[0]:
            maxes = sorted(maxes[1:] + [sum(l)])
    return sum(maxes)
