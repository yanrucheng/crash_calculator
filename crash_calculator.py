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
    parser.add_argument('-moves', type=int, help='Moves allowed to use')
    parser.add_argument('-target', type=int, help='Target number')
    parser.add_argument('-register', type=int, help='Original number in the register')
    parser.add_argument("-buttons", nargs="*", type=str, help="Buttons available, E.g. +1 | *2 | 1 | \"<<\" | \"6=>9\"")
    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    register, moves, target = args.register, args.moves, args.target
    buttons = [Button(name) for name in args.buttons]
    cc = CrashCalculator(register, moves, target, buttons)
    print(cc.solve())
