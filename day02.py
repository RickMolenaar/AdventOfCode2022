def parse_input():
    with open('day02.txt') as f:
        s = ''.join(f.readlines())[:-1]
    return s

def solve(s, debug=False):
    """
    >>> solve('''A Y
    ... B X
    ... C Z''')
    12
    """
    tot = 0
    for match in enumerate(s.split('\n')):
        theirs, result = match.split()
        result = ord(result) - ord('X')
        result_score = result * 3
        choice_score = (ord(theirs) + result - 1 - ord('A')) % 3 + 1
        tot += result_score + choice_score
    return tot
