import argparse
from button import Button

class CrashCalculator:
    def __init__(self, args):
        self.register = args.register
        self.moves = args.moves
        self.target = args.target
        self.buttons = [Button(name) for name in args.buttons]

    def solve(self): # DFS
        # state: (current register, steps left, actions taken)
        dp = [(self.register, self.moves, [])]
        met = set([self.register])
        while dp:
            reg, steps, actions = dp.pop()

            if steps <= 0: continue
            for b in self.buttons:
                new_reg = b.func(reg)
                if new_reg == self.target:
                    return actions + [b.name]
                if new_reg in met: continue
                met.add(new_reg)
                dp.append((new_reg, steps - 1, actions + [b.name]))
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
    cc = CrashCalculator(args)
    print(cc.solve())
