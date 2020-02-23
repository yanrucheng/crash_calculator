import argparse, warnings
from button import Button
try:
    from gooey import Gooey
except:
    Gooey = lambda x:x # dummy Gooey wrapper

class CalculatorGameState:
    def __init__(self, register, moves, target, button_names, solution=None):
        assert all(isinstance(b, str) for b in button_names), 'You should create game state with button name'
        self.register = register
        self.moves = moves
        self.target = target
        self.buttons = [Button(b) for b in button_names]
        self.solution = solution or []

    def __hash__(self):
        matters = map(str, (self.register, self.target, self.buttons))
        return hash(' '.join(matters))

    def get_successors(self):
        if self.moves <= 0: return
        for b in self.buttons:
            if b.type == 'store': # additional operation provided by 'store'
                button_names = [str(b) if b.type != 'store' else 'store{}'.format(self.register) for b in self.buttons]
                yield CalculatorGameState(self.register, self.moves-1,
                        self.target, button_names, self.solution + ['store'])

            if b.type == 'button_modifier':
                button_names = [str(bu.add(b.num)) for bu in self.buttons]
            else:
                button_names = [*map(str, self.buttons)]
            yield CalculatorGameState(b.func(self.register), self.moves-1,
                    self.target, button_names, self.solution + [str(b)])

    def is_goal(self):
        return self.register == self.target

    def __str__(self):
        return 'Register: {}, Moves: {}, Target: {}, Buttons: {}'.format(
                self.register, self.moves, self.target, ' '.join(map(str, self.buttons)))

    def __repr__(self):
        return str(self)

class Calculator_Solver:
    def __init__(self, register, moves, target, buttons_names):
        self.start = CalculatorGameState(register, moves, target, buttons_names)

    def solve(self): # DFS
        # state: (current register, actions left)
        dp = [self.start]
        steps = {hash(self.start):self.start.moves}
        while dp:
            state = dp.pop()
            for s in state.get_successors():
                if s.is_goal():
                    return s.solution
                if hash(s) in steps and steps[hash(s)] >= s.moves: continue
                steps[hash(s)] = s.moves
                dp.append(s)
        return ['Fail']

@Gooey
def get_args():
    parser = argparse.ArgumentParser(description='Crash Calculator: the Game')
    parser.add_argument('-d', '--debug', action='store_true',
            help='Show warnings from buttons')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-m', '--moves', type=int, required=True,
            help='The moves allowed to use')
    requiredNamed.add_argument('-t', '--target', nargs="*", type=int, required=True,
            help='The target number(s)')
    requiredNamed.add_argument('-r', '--register', type=int, required=True,
            help='The original number in the register')
    requiredNamed.add_argument('-b', '--buttons', nargs="*", type=str, required=True,
            help="Buttons available, E.g. +1 | *2 | 1 | \"<<\" | \"6=>9\"")
    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    not args.debug and warnings.filterwarnings("ignore")

    register, moves, targets, button_names = \
            args.register, args.moves, args.target, args.buttons
    for t in targets:
        cs = Calculator_Solver(register, moves, t, button_names)
        print('Solution for target {}: {}.'.format(t, ', '.join(cs.solve())))
