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
    for i, match in enumerate(s.split('\n')):
        theirs, result = match.split()
        result = ord(result) - ord('X')
        result_score = result * 3
        choice_score = (ord(theirs) + result - ord('A') - 1) % 3 + 1
        # if debug:
        #     print(match, result_score, choice_score)
        tot += result_score + choice_score
    return tot
