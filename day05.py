def parse_input():
    with open('day05.txt') as f:
        s = ''.join(f.readlines())
    return s

def parse_example():
    with open('day05example.txt') as f:
        s = ''.join(f.readlines())
    return s

def format_input(inp):
    stack_def = True
    stacks = []
    moves = []
    for line in inp.split('\n'):
        if stack_def:
            for i, c in enumerate(line):
                if i % 4 == 1:
                    if c == '1':
                        stack_def = False
                        break
                    if len(stacks) < i // 4 + 1:
                        stacks.append([])
                    if c != ' ':
                        stacks[i//4].insert(0, c)
        else:
            if line.startswith("move"):
                words = line.split()
                amount, from_stack, to_stack = map(int, (words[1], words[3], words[5]))
                moves.append((amount, from_stack - 1, to_stack - 1))
    return stacks, moves

def solve(inp, debug=False):
    """
    >>> solve(parse_example(), True)
    'MCD'
    """
    stacks, moves = format_input(inp)
    for amount, from_stack, to_stack in moves:
        # while amount > 0:
        #     stacks[to_stack].append(stacks[from_stack].pop())
        #     amount -= 1
        stacks[to_stack].extend(stacks[from_stack][-amount:])
        stacks[from_stack] = stacks[from_stack][:-amount]
    return ''.join(stack[-1] for stack in stacks)
