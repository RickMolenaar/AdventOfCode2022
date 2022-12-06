def parse_input():
    with open('day06.txt') as f:
        s = ''.join(f.readlines())
    return s

def parse_example():
    with open('day06example.txt') as f:
        s = ''.join(f.readlines())
    return s

def format_input(inp):
    return inp

def solve(s, debug=False):
    """
    >>> solve(parse_example())
    29
    """
    # for i in range(len(inp)):
    #     if len(set(inp[i:i+14])) == 14:
    #         return i + 14
    return[i for i in range(len(s))if len(set(s[i:i+14]))==14][0]+14