class Monkey:
    def __init__(self, items: list[int], worry_operation: str, test: tuple[int], troop: list['Monkey']):
        self.items = items
        self.worry_operation = worry_operation
        to_divide, true_monkey, false_monkey = test
        self.test = lambda worry: true_monkey if worry % to_divide == 0 else false_monkey
        self.troop = troop
        self.inspect_count = 0

    def progress_round(self):
        # print('\t', self.test(17))
        for old in self.items:
            self.inspect_count += 1
            new_worry = eval(self.worry_operation)
            new_worry = new_worry // 3
            new_monkey = self.test(new_worry)
            if self.troop[new_monkey] == self:
                print(old, self.worry_operation, new_worry, self.test(new_worry))
                for i in range(30):
                    print(i, self.test(i))
                raise ValueError
            self.troop[new_monkey].items.append(new_worry)
        self.items = []

def parse_input(file = 'day11.txt'):
    with open(file) as f:
        s = map(lambda l: l.strip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day11example.txt')

def format_input(inp) -> list[Monkey]:
    troop = []
    for line in inp:
        if not line:
            continue
        if line.startswith('Monkey'):
            if '0' in line:
                continue
            test = (to_divide, true_monkey, false_monkey)
            troop.append(Monkey(items, worry_operation, test, troop))
        elif line.startswith('Starting items'):
            items = list(map(int, line.split(':')[1].split(',')))
        elif line.startswith('Operation'):
            worry_operation = line.split('=')[1]
        elif line.startswith('Test'):
            to_divide = int(line.split()[-1])
        elif line.startswith('If true'):
            true_monkey = int(line.split()[-1])
        elif line.startswith('If false'):
            false_monkey = int(line.split()[-1])
        else:
            raise ValueError(f'Could not read line {line}')
    
    test = (to_divide, true_monkey, false_monkey)
    troop.append(Monkey(items, worry_operation, test, troop))
    return troop

def solve(inp, debug=False):
    troop = format_input(inp)
    for round in range(20):
        for monkey in troop:
            # if debug:
            #     print(round, monkey.items)
            monkey.progress_round()
        # if debug:
        #     print([monkey.inspect_count for monkey in troop])
    
    counts = sorted(monkey.inspect_count for monkey in troop)
    return counts[-1] * counts[-2]

def main(debug = False):
    return str(solve(parse_example(), True)) + '\n' + str(solve(parse_input(), debug))
