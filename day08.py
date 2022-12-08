def parse_input(file = 'day08.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day08example.txt')

def format_input(inp):
    return [list(map(int, row)) for row in inp]

def solve(inp, debug=False):
    """
    >>> solve(parse_example())
    None
    """
    visible = 0
    best_scenic_score = 1
    inp = format_input(inp)
    for row in range(len(inp)):
        for col in range(len(inp[0])):
            tree = inp[row][col]
            scenic_score = 1
            top = bottom = left = right = 0
            for top in range(1, row + 1):
                new_tree = inp[row - top][col]
                if new_tree >= tree:
                    break
            scenic_score *= top
            # else: 
            #     visible += 1
            #     continue
            for bottom in range(1, len(inp) - row):
                new_tree = inp[row + bottom][col]
                if new_tree >= tree:
                    break
            scenic_score *= bottom
            # else: 
            #     visible += 1
            #     continue
            for left in range(1, col + 1):
                new_tree = inp[row][col - left]
                if new_tree >= tree:
                    break
            scenic_score *= left
            # else: 
            #     visible += 1
            #     continue
            for right in range(1, len(inp[0]) - col):
                new_tree = inp[row][col + right]
                if new_tree >= tree:
                    break
            scenic_score *= right
            # else: 
            #     visible += 1
            #     continue
            best_scenic_score = max(best_scenic_score, scenic_score)
    return best_scenic_score

def main(debug = False):
    return str(solve(parse_example(), debug)) + '\n' + str(solve(parse_input(), debug))
