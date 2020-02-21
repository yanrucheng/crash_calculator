import argparse
from button import Button

class CrashCalculator:
    def __init__(self, register, moves, target, buttons):
        self.register = register
        self.moves = moves
        self.target = target
        self.buttons = buttons

    def solve(self): # DFS
        # state: (current register, actions left)
        dp = [(self.register, [])]
        d = {self.register: self.moves}
        while dp:
            reg, actions = dp.pop()
            step = d[reg]
            if step <= 0: continue

            for b in self.buttons:
                new_reg = b.func(reg)
                if new_reg == self.target:
                    return actions + [b.name]
                if new_reg in d and d[new_reg] >= step - 1: continue
                d[new_reg] = step - 1
                dp.append((new_reg, actions + [b.name]))
        return ['Fail']

def get_args():
    parser = argparse.ArgumentParser(description='Crash Calculator: the Game')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-m', '--moves', type=int, required=True,
            help='The moves allowed to use')
    requiredNamed.add_argument('-t', '--target', type=int, required=True,
            help='The target number')
    requiredNamed.add_argument('-r', '--register', type=int, required=True,
            help='The original number in the register')
    requiredNamed.add_argument('-b', '--buttons', nargs="*", type=str, required=True,
            help="Buttons available, E.g. +1 | *2 | 1 | \"<<\" | \"6=>9\"")
    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    register, moves, target = args.register, args.moves, args.target
    buttons = [Button(name) for name in args.buttons]
    cc = CrashCalculator(register, moves, target, buttons)
    print(cc.solve())
