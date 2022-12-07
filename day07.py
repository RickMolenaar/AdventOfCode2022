def parse_input(file = 'day07.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day07example.txt')

def format_input(inp):
    directory = {}
    parse_directory(directory, inp[1:])
    return directory

def parse_directory(directory, remaining_lines):
    assert remaining_lines[0] == '$ ls'
    remaining_lines.pop(0)
    while remaining_lines:
        line = remaining_lines.pop(0)
        if line.startswith('$ cd'):
            new_dir = line.split()[-1]
            if new_dir == '..':
                return remaining_lines
            remaining_lines = parse_directory(directory[new_dir], remaining_lines)
            continue
        assert not line.startswith('$')
        filesize, name = line.split()
        if filesize == 'dir':
            directory[name] = {}
        else:
            directory[name] = int(filesize)
    return remaining_lines

def get_size(directory):
    tot = 0
    for k, v in directory.items():
        if type(v) == int:
            tot += v
        else:
            tot += get_size(v)
    return tot

def get_recursive_file_size(directory, max_size, limited_total_size, directory_sizes):
    total_size = 0
    for k, v in directory.items():
        if type(v) == int:
            total_size += v
        else:
            their_size, limited_total_size, directory_sizes = get_recursive_file_size(v, max_size, limited_total_size, directory_sizes)
            total_size += their_size
    if total_size < max_size:
        limited_total_size += total_size
    directory_sizes.append(total_size)
    return total_size, limited_total_size, directory_sizes

def solve(inp, debug=False):
    """
    >>> solve(parse_example())
    24933642
    """
    directory = format_input(inp)
    # return get_recursive_file_size(directory, 100000, 0)[1]
    total_size, _, directory_sizes = get_recursive_file_size(directory, 100000, 0, [])
    missing_size = 30000000 - (70000000 - total_size)
    for size in sorted(directory_sizes):
        if size > missing_size:
            return size
